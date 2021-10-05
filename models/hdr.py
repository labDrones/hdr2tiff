from spectral import *
import pandas as pd
import os 
import platform
from raster import Raster

path_sap = "/" if platform.system() != 'Windows' else ' \\'


class Fly:
    def __init__(self, path:str, alt: float, lens: float) -> None:
        self.path = path
        self.alt = alt
        self.lens = lens
        self.focal = self.lens2focal(lens)
    
    def lens2focal(self, lens)->float:
        focal = {4.8: 50.7, 
                8: 32.2,
                12: 21.1,
                17:15.3,
                23: 12.0,
                35: 7.8}
        return focal[lens]


    def get_rasterizes(self) -> list:
        return []
    
    def make_tiff_of(self, name:str, bands:list) -> bool:
        return False
    
    def get_waves_indexs(self, intervals:list) -> list:
        return [()]
    
    def __check_frame(self, Fname:str) -> bool:
        name = ""
        name = Fname.split(path_sap)[-1]
        name = self.path+"frameIndex_"+(name.split('_')[-1].replace(".hdr", ".txt"))
        return os.path.isfile(name) 

    def __check_raw(self, Fname:str)-> bool:
        return os.path.isfile(Fname.replace(".hdr", ""))

    def __check_gps(dir, imu = "imu_gps.txt" ):
        return os.path.exists(dir+path_sap+imu)

    def __check_file(self,  Fname:str, imu:str) -> bool:
        
        if not os.path.exists(Fname):
            return False
            raise Exception("Error don\'t found file")
        if(not self.__check_raw(Fname)):
            return False
            raise Exception("Miss raw")
        if(not self.__check_gps(imu)):
            return False
            raise Exception("Miss imu_gps")
        if(not self.__check_frame(Fname)):
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

