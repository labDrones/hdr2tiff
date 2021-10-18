from logging import setLoggerClass
from numpy import add
from osgeo import osr, gdal
from spectral import *
import pandas as pd
import os 
import platform
import glob
# from raster import Raster
def is_decreasing(imu, col):
    return not round(imu.iloc[0][col], 7) > round(imu.iloc[500][col],7)

def get_pixel_len(alt, fov):
    '''
    Returns pixel Nano-Hyperspec pixel len in cm
    '''
    # fov = 22.1
    ifov = (fov/640)*(17.44)*(10**-3)
    len = ifov*alt
    return len

path_sap = "/"  #if platform.system() != 'Windows' else ' \\'
    # source = osr.SpatialReference()
    # source.ImportFromEPSG(4326)

    # target = osr.SpatialReference()
    # target.ImportFromEPSG(32722)
class HDR:
    def __init__(self) -> None:
        pass
    def __bounds(self, frames, imu) -> list:
        bounds = frames.loc[frames["Frame#"] == frames["Frame#"].min()].to_dict("records")
        bounds += frames.loc[frames["Frame#"] == frames["Frame#"].max()].to_dict("records")
        return imu.loc[imu['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]
        

    def make_transform(self, bounds, frames, imu, pixel_len) -> list:
        source = osr.SpatialReference()
        source.ImportFromEPSG(4326)
        target = osr.SpatialReference()
        target.ImportFromEPSG(32722)
        lonlat2utm = osr.CoordinateTransformation(source, target)


        p1 = lonlat2utm.TransformPoint(imu["Lat"].max() ,imu["Lon"].max() )
        p2 = lonlat2utm.TransformPoint(imu["Lat"].min() ,imu["Lon"].min() )

        lon = {"Max":p1[1],"Min":p2[1] }
        lat = {"Max":p1[0],"Min":p2[0] }

        lon_decreasing = 1 if is_decreasing(imu, "Lat") else -1
        lat_decreasing = 1 if is_decreasing(imu, "Lon") else -1
        boundary = {}
        boundary["lat"] = lat["Min"] if lat_decreasing > 0 else lat["Max"]
        boundary["lon"] = lon["Min"] if lon_decreasing > 0 else lon["Max"]
        
        return [boundary["lat"], lat_decreasing*pixel_len,0 , boundary["lon"],0 , lon_decreasing*pixel_len ]

    def totiff(self, out:str) -> bool:
        pass

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


    def get_rasterizes(self) -> list:
        print(self.path+path_sap+"*.hdr")
        files = glob.glob(self.path+path_sap+"*.hdr")
        ok = []
        for file in files:
            if self.check_file(file):
                ok.append(file)

        if not self.check_imu():
            print("CU")
            return []
            
        return ok 
    
    def make_tiff_of(self, name:str, bands:list) -> bool:

        return False
    
    def get_waves_indexs(self, intervals:list) -> list:
        return [()]
    
    def __check_frame(self, Fname:str) -> bool:
        name = ""
        name = Fname.split(path_sap)[-1]
        name = self.path+path_sap+"frameIndex_"+(name.split('_')[-1].replace(".hdr", ".txt"))
        return os.path.exists(name) 

    def __check_raw(self, Fname:str)-> bool:
        return os.path.exists(Fname.replace(".hdr", ""))

    def set_imu(self, path:str)-> None:
        self.imu = path

    def check_imu(self):
        return os.path.exists(self.imu)

    def check_file(self,  Fname:str) -> bool:
        
        if not os.path.exists(Fname):
            print("s")
            return False
            raise Exception("Error don\'t found file")
        if(not self.__check_raw(Fname)):
            print("s1")
            return False
            raise Exception("Miss raw")
        if(not self.__check_frame(Fname)):
            print("s2")
            return False
            raise Exception("Miss FrameIndex")
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

