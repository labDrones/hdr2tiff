# from spectral import *

# from osgeo import gdal

# img = open_image('t1\\raw_3552.hdr')
# # img2 = open_image('t1\\raw_9680.hdr')
# iew = imshow(img, (29, 19, 9))
# # iew = imshow(img2, (29, 19, 9))
# print(img.shape)
# # print(img2.shape)
# teste = input("")

from os import sep
from models import hdr
import pandas as pd



hdr_name  = 't1\\raw_2000.hdr'
imu_gps_name = 't1\imu_gps.txt'
imu = pd.read_csv(imu_gps_name, sep="	")

array, img_frames = hdr.open(hdr_name)

bounds = img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].min()].to_dict("records")
bounds += img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].max()].to_dict("records")

print(bounds)

imu = imu.loc[imu['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]

print(imu.head())

p1 = (imu["Lat"].max(), imu["Lon"].min())
p2 =( imu["Lat"].min(), imu["Lon"].max())

print("lat: ", p1)
print("lon: ", p2)


