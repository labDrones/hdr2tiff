from logging import setLoggerClass
import numpy as np
from osgeo import osr, gdal
import spectral as spy
import pandas as pd
import os 
import platform
import glob
from dataclasses import dataclass
# from raster import Raster
def is_decreasing(imu, col):
    return not round(imu.iloc[0][col], 7) > round(imu.iloc[500][col],7)

@dataclass
class Band:
    num: int
    wave: float 

path_sap = "/"  
class HDR:
    def __init__(self, m: spy.SpyFile, pixel_len: float, frames: pd.DataFrame, imu: pd.DataFrame, EPSG_in: int = 4326, EPSG_out: int = 32722 ) -> None:
        self.m: spy.SpyFile = m
        self.frames: pd.DataFrame = self.__get_frames(frames, imu)
        self.pixel_len: float = pixel_len
        self.source = osr.SpatialReference()
        self.source.ImportFromEPSG(EPSG_in)
        self.target = osr.SpatialReference()
        self.target.ImportFromEPSG(EPSG_out)
    def __format__(self, format_spec: str) -> str:
        pass
    def __get_frames(self, frames: pd.DataFrame, imu: pd.DataFrame) -> list:
        bounds = frames.loc[frames["Frame#"] == frames["Frame#"].min()].to_dict("records")
        bounds += frames.loc[frames["Frame#"] == frames["Frame#"].max()].to_dict("records")
        return imu.loc[imu['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]
        

    def __make_transform(self) -> list:
        lonlat2utm = osr.CoordinateTransformation(self.source, self.target)
        p1 = lonlat2utm.TransformPoint(self.frames["Lat"].max() ,self.frames["Lon"].max() )
        p2 = lonlat2utm.TransformPoint(self.frames["Lat"].min() ,self.frames["Lon"].min() )
        lon = {"Max":p1[1],"Min":p2[1] }
        lat = {"Max":p1[0],"Min":p2[0] }
        lon_decreasing = 1 if self.frames["Lat"].is_monotonic_decreasing else -1
        lat_decreasing = 1 if self.frames["Lon"].is_monotonic_decreasing else -1
        boundary = {}
        boundary["lat"] = lat["Min"] if lat_decreasing > 0 else lat["Max"]
        boundary["lon"] = lon["Min"] if lon_decreasing > 0 else lon["Max"]
        
        return [boundary["lat"], lat_decreasing*self.pixel_len,0 , boundary["lon"],0 , lon_decreasing*self.pixel_len ]

    def totiff(self, out:str, bands: list = []) -> bool:
        transform = self.__make_transform()
        try:
            driver = gdal.GetDriverByName('GTiff')
            if len(bands) > 0:
                rows, cols, _  = self.m.shape
            else:
                rows, cols, no_bands = self.m.shape
                bands = range(no_bands)

            DataSet = driver.Create(out, cols, rows, no_bands, gdal.GDT_UInt16)
            DataSet.SetGeoTransform(transform)
            DataSet.SetProjection(self.target)
            
            for band  in bands:
                i = band.num
                image = np.squeeze(self.m[:,:, i], axis=(2,))
                DataSet.GetRasterBand(i+1).SetDescription(str(band.wave))
                DataSet.GetRasterBand(i+1).WriteArray(image)

            DataSet = None
            return True
        except:
            return False


class Fly:
    def __init__(self, path:str, alt: float, lens: float, imu:str = '') -> None:
        self.path = path
        self.imu = self.path+path_sap+ "imu_gps.txt" if imu == '' else imu
        self.alt = alt
        self.lens = lens
        self.wave_indexs = [()]
        self.focal = self.lens2focal(lens)
    
    def lens2focal(self, lens:float)->float:
        focal = {4.8: 50.7, 
                8: 32.2,
                12: 21.1,
                17:15.3,
                23: 12.0,
                35: 7.8}
        return focal[lens]

    def pixel_len(self) -> float:
        ifov = (self.focal/640)*(17.44)*(10**-3)
        len = ifov*self.alt
        return len

    def get_rasterizes(self) -> list:
        if not self.__check_imu():
            return []
        files = glob.glob(self.path+path_sap+"*.hdr")
        ok = []
        for file in files:
            if self.check_file(file):
                ok.append(file)
        return ok 
    
    def make_tiff_of(self, name:str, out:str = '',bands:list = []) -> bool:
        img : spy.SpyFile = spy.open_image(name)
        frames: pd.DataFrame = self.get_frame(name)
        imu: pd.DataFrame = pd.read_csv(self.imu, sep="	")
        hdr = HDR(img, self.pixel_len(), frames, imu)
        if out == '':
            out = name.split("/")[-1].replace("hdr", "tiff")
        if bands == []:
            img.bands.centers[:5]
            _, _, no_bands = img.shape
            bands = range(no_bands)
            
        return hdr.totiff(out)
    
    def get_waves(self, name:str) -> list:
        wavelens  = spy.io.envi.open(name).bands.centers
        bands = []
        for i, b in enumerate(wavelens):
            band = Band(i, float(round(b, 2)))
            bands.append(band)
        return bands
    
    def reduce_intervals(self, intervals:list) ->list:
        sub_intervals = []
        i = 0 
        while i < len(intervals)-1:
            if intervals[i][-1] <= intervals[i+1][0]:
                new_interval = (intervals[i][0], intervals[i+1][-1])
                sub_intervals.append(new_interval)
                i += 1
            else:  
                new_interval = (intervals[i][0], intervals[i][-1])
                sub_intervals.append(new_interval)
            
            i += 1

        if i == len(intervals):
            new_interval = (intervals[i][0], intervals[i][-1])
            sub_intervals.append(new_interval)
                
        sub_intervals.sort(key = lambda x:x[0])
        
        if len(sub_intervals) == len(intervals):
            return intervals

        return self.reduce_intervals(sub_intervals)
            
    def __get_grops(self, bands:list, interval_ex:str)->list:
        bigger = bands[-1].wave
        minor = 0 
        betweens = []
        once = []
        for expression in interval_ex.split(','):
            if "<" in expression:
                num = float(expression.replace("<",""))
                if bigger < num:
                    bigger = num
            elif ">" in expression:
                num = float(expression.replace(">",""))
                if minor > num:
                    minor = num
            elif "-" in expression:
                nums = set([float(i) for i in expression.split("-")[0,-1]].sort())
                betweens.append(nums)
            else:
                num = float(expression)
                once.append(num)
        return (bigger, minor, betweens, once)

    def get_bands_by_intervals(self, bands:list, interval_ex:str ) -> list:
        # <, >, -
        bigger, minor, betweens, once = self.__get_grops(bands, interval_ex)
        
        betweens.sort(key = lambda x: x[0])

        betweens = self.reduce_intervals(betweens)

        minor = minor if minor < bigger else bigger
        bigger = bigger if bigger > minor else minor

        if betweens[0][0] >= minor: 
            betweens.clear()

        if len(betweens) != 0 and betweens[-1][-1] <= bigger: 
            betweens.clear()
        



            
        return []

    def get_frame(self, hdr_name: str) -> pd.DataFrame:
        Fname = hdr_name.split(path_sap)[-1]
        Fname = self.path+path_sap+"frameIndex_"+(hdr_name.split('_')[-1].replace(".hdr", ".txt"))
        return pd.read_csv(Fname, sep="	")

    def __check_frame(self, Fname:str) -> bool:
        name = ""
        name = Fname.split(path_sap)[-1]
        name = self.path+path_sap+"frameIndex_"+(name.split('_')[-1].replace(".hdr", ".txt"))
        return os.path.exists(name) 

    def __check_raw(self, Fname:str)-> bool:
        return os.path.exists(Fname.replace(".hdr", ""))

    def set_imu(self, path:str)-> bool:
        self.imu = path
        return self.__check_imu()

    def __check_imu(self):
        return os.path.exists(self.imu)

    def check_file(self,  Fname:str) -> bool:
        
        if not os.path.exists(Fname):
            return False
        if(not self.__check_raw(Fname)):
            return False
        if(not self.__check_frame(Fname)):
            return False
        return True




# def get_frames(Fname):
#     path = ""
#     name = ""
#     spt = Fname.split(path_sap)
#     name = spt[-1]
#     for i in spt[:-1]:
#         path += i+path_sap
#     del spt
#     name = path+"frameIndex_"+(name.split('_')[-1].replace(".hdr", ".txt"))
#     return pd.read_csv(name, sep="	")


# def open(Fname = '', imu = "imu_gps.txt" ):
#     if Fname == '':
#         raise
#     if __check_files(Fname, imu):
#         return open_image(Fname), get_frames(Fname)

#     return None

