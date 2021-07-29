from spectral import *
import pandas as pd
import os 
import platform

path_sap = "/" if platform.system() != 'Windows' else "\\"

def __check_frame(Fname):
    path = ""
    name = ""
    spt = Fname.split(path_sap)
    name = spt[-1]
    for i in spt[:-1]:
        path = i+path_sap
    del spt
    return True

def __check_raw(Fname):
    return True

def __check_gps(imu = "imu_gps.txt" ):
    # os.path.exists(imu)
    return True

def __check_files(Fname, imu):
    if not os.path.exists(Fname):
        raise Exception("Error don\'t fund file")
    if(not __check_raw(Fname)):
        raise Exception("Miss raw")
    if(not __check_gps(imu)):
        raise Exception("Miss imu_gps")
    if(not __check_frame(Fname)):
        raise Exception("Miss FrameIndex")

    return True




def get_frames(Fname):
    path = ""
    name = ""
    spt = Fname.split(path_sap)
    name = spt[-1]
    for i in spt[:-1]:
        path = i+path_sap
    del spt
    name = path+"frameIndex_"+(name.split('_')[-1].replace(".hdr", ".txt"))
    return pd.read_csv(name, sep="	")


def open(Fname = '', imu = "imu_gps.txt" ):
    if Fname == '':
        raise
    if __check_files(Fname, imu):
        return open_image(Fname), get_frames(Fname)

    return None

