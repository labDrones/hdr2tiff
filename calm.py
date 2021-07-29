from spectral.io.spyfile import transform_image
from spectral import imshow
from models import hdr, raster
import pandas as pd
from osgeo import osr
import numpy as np
import glob


source = osr.SpatialReference()
source.ImportFromEPSG(4326)

target = osr.SpatialReference()
target.ImportFromEPSG(32722)

lonlat2utm = osr.CoordinateTransformation(source, target)

def get_pixel_len(alt, fov = 22.1):
    '''
    Returns pixel Nano-Hyperspec pixel len in cm
    '''
    # fov = 22.1
    ifov = (fov/640)*(17.44)*(10**-3)
    len = ifov*alt
    return len


# hdr_name  = '100128_voo_11_120m_5ms_2021_07_21_13_10_49\\raw_0.hdr'
# imu_gps_name = '100128_voo_11_120m_5ms_2021_07_21_13_10_49\\imu_gps.txt'
imu_gps_name = '100128_voo_11_120m_5ms_2021_07_21_13_10_49/imu_gps.txt'

imgs_names = glob.glob("100128_voo_11_120m_5ms_2021_07_21_13_10_49/*.hdr")

hdr_name  = 't1/raw_2000.hdr'
for hdr_name in imgs_names:

    imu = pd.read_csv(imu_gps_name, sep="	")
    try:
        array, img_frames = hdr.open(hdr_name)
    except:
        continue
    
    tiff_name = hdr_name.split("/")[-1].replace("hdr", "tiff")
    print(tiff_name)
    bounds = img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].min()].to_dict("records")
    bounds += img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].max()].to_dict("records")


    imu = imu.loc[imu['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]

    lat = {"Max":imu["Lat"].max(),"Min":imu["Lat"].min() }
    lon = {"Max":imu["Lon"].max(),"Min":imu["Lon"].min() }

    p1 = lonlat2utm.TransformPoint(lat["Min"],lon["Max"] )
    p2 = lonlat2utm.TransformPoint(lat["Max"], lon["Min"])

    lon = {"Max":p2[1],"Min":p1[1] }
    lat = {"Max":p1[0],"Min":p2[0] }

    print("lat", lat)
    print("lon", lon)

    transform = [lat["Min"], get_pixel_len(100), 0, lon["Min"], 0,get_pixel_len(100) ]
    # _, _, no_bands = array.shape
    # print(array)

    raster.CreateGeoTiff(tiff_name, array, transform, target.ExportToWkt())

# view = imshow(array)
# input()