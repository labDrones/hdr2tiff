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

def get_pixel_len(alt):
    '''
    Returns pixel Nano-Hyperspec pixel len in cm
    '''
    len = 1.5*alt/100
    return len

def cm2degrees(cm):
    G2cm = 0.0000001 #1.11cm
    degree = cm*G2cm/1.11
    return degree


hdr_name  = '100128_voo_11_120m_5ms_2021_07_21_13_10_49\\raw_0.hdr'
imu_gps_name = '100128_voo_11_120m_5ms_2021_07_21_13_10_49\\imu_gps.txt'

# hdr_name  = 't1\\raw_2000.hdr'
# imu_gps_name = 't1\\imu_gps.txt'
imu = pd.read_csv(imu_gps_name, sep="	")

array, img_frames = hdr.open(hdr_name)

bounds = img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].min()].to_dict("records")
bounds += img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].max()].to_dict("records")

print(bounds)

imu = imu.loc[imu['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]

# print(imu.head())

lat = {"Max":imu["Lat"].max(),"Min":imu["Lat"].min() }
lon = {"Max":imu["Lon"].max(),"Min":imu["Lon"].min() }

p1 = (imu["Lat"].max(), imu["Lon"].min())
p2 =( imu["Lat"].min(), imu["Lon"].max())
range_lat = abs(p1[0] - p2[0])
range_lon = abs(p1[1] - p2[1])
print("lat: ", lat)
print("lon: ", lon)

print(range_lat," > ",range_lon , range_lat>range_lon )

# distLon = -1*abs(cm2degrees(array.shape[1]*get_pixel_len(120)))


# x = abs((lon["Min"]+distLon) - lon["Max"])/2

# lon["Max"] = lon["Max"] + x
# lon["Min"] = lon["Min"] - x

# distLat = -1*abs(cm2degrees(array.shape[0]*get_pixel_len(100)))



# y = abs((lat["Min"]+distLat) - lat["Max"])/2

# lat["Max"] = lat["Max"] + y
# lat["Min"] = lat["Min"] - y

# print(x, y)


# print("lat2: ", lat)
# print("lon2: ", lon)


p1 = lonlat2utm.TransformPoint(lat["Min"],lon["Max"] )
p2 = lonlat2utm.TransformPoint(lat["Max"], lon["Min"])
# p1 = lonlat2utm.TransformPoint(lon["Max"], lat["Min"])
# p2 = lonlat2utm.TransformPoint(lon["Min"], lat["Max"])

range_lat = abs(p1[0] - p2[0])
range_lon = abs(p1[1] - p2[1])
print(range_lon,range_lat )
print("p1", p1)
print("p2", p2)

print("old_len:", range_lon/array.shape[1], " new_len:", cm2degrees(get_pixel_len(120)))
# transform = [lon["Max"], cm2degrees(get_pixel_len(120)), 0, lat["Min"], 0, cm2degrees(get_pixel_len(120)) ]
transform = [p1[0], (p2[0]-p1[0])/array.shape[1], 0, p1[1], 0, (p2[1]-p1[1])/array.shape[0] ]
# transform = [imu["Lon"].max(), range_lon/array.shape[1], 0, imu["Lat"].min(), 0, range_lat/array.shape[0] ]
# transform = [imu["Lon"].max(), cm2degrees(get_pixel_len(120)), 0, imu["Lat"].min(), 0,cm2degrees(get_pixel_len(120)) ]



_, _, no_bands = array.shape
print(array)

raster.CreateGeoTiff("teste-4.tiff", array, transform, target.ExportToWkt())
view = imshow(array)
input()