from spectral.io.spyfile import transform_image
from spectral import imshow
from models import hdr, raster
import pandas as pd
from osgeo import osr
import numpy as np


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


hdr_name  = '100128_voo_11_120m_5ms_2021_07_21_13_10_49\\raw_0.hdr'
imu_gps_name = '100128_voo_11_120m_5ms_2021_07_21_13_10_49\\imu_gps.txt'

# hdr_name  = 't1\\raw_2000.hdr'
# imu_gps_name = 't1\\imu_gps.txt'
imu = pd.read_csv(imu_gps_name, sep="	")

array, img_frames = hdr.open(hdr_name)

bounds = img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].min()].to_dict("records")
bounds += img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].max()].to_dict("records")


imu = imu.loc[imu['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]

# print(imu.head())

lat = {"Max":imu["Lat"].max(),"Min":imu["Lat"].min() }
lon = {"Max":imu["Lon"].max(),"Min":imu["Lon"].min() }

p1 = lonlat2utm.TransformPoint(lat["Min"],lon["Max"] )
p2 = lonlat2utm.TransformPoint(lat["Max"], lon["Min"])

lon = {"Max":p2[1],"Min":p1[1] }
lat = {"Max":p1[0],"Min":p2[0] }


# range_lon = lon["Max"]-lon["Min"]
# range_lat= lat["Max"]-lat["Min"]
# print("lat", lat)
# print("lon", lon)
# print(range_lon,range_lat, array.shape[0] )
# print(lat["Min"]+(get_pixel_len(100)*640 ))
# dLat = abs(lat["Min"]+(get_pixel_len(100)*array.shape[1])-  lat["Max"])/2
# dlon = abs(lon["Min"]+(get_pixel_len(100)*array.shape[0]) -  lon["Max"])/2

# lat["Min"] = lat["Min"] - dLat
# lat["Max"] = lat["Max"] + dLat

# lon["Min"] = lon["Min"] - dlon
# lon["Max"] = lon["Max"] + dlon

print("lat", lat)
print("lon", lon)

# transform = [lon["Max"], cm2degrees(get_pixel_len(120)), 0, lat["Min"], 0, cm2degrees(get_pixel_len(120)) ]
transform = [lat["Min"], get_pixel_len(100), 0, lon["Min"], 0,get_pixel_len(100) ]
# transform = [p1[0], (p2[0]-p1[0])/array.shape[1], 0, p1[1], 0, (p2[1]-p1[1])/array.shape[0] ]
# transform = [imu["Lon"].max(), range_lon/array.shape[1], 0, imu["Lat"].min(), 0, range_lat/array.shape[0] ]
# transform = [imu["Lon"].max(), cm2degrees(get_pixel_len(120)), 0, imu["Lat"].min(), 0,cm2degrees(get_pixel_len(120)) ]



_, _, no_bands = array.shape
print(array)

raster.CreateGeoTiff("teste-7.tiff", array, transform, target.ExportToWkt())
view = imshow(array)
input()