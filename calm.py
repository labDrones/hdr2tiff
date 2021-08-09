from logging import Handler
from spectral.io.spyfile import transform_image
from spectral import imshow
from models import hdr, raster
import pandas as pd
from osgeo import osr
import json
import numpy as np
import glob

from tkinter import filedialog
from tkinter import *

import matplotlib.pyplot as  plt
import matplotlib.patches as mpatches

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

def is_decreasing(imu, col):
    first = imu.to_dict("records")[:500]
    # if first[0]['Roll'] >   0:
    return not round(first[0][col], 7) > round(first[-1][col],7)
    # return not (round(first[0][col], 7) > round(first[-1][col], 7))
    
root = Tk()
root.withdraw()
base_dir = filedialog.askdirectory()
# base_dir = '100128_voo_11_120m_5ms_2021_07_21_13_10_49'
base_dir = base_dir.replace("/", "\\")
imu_gps_name = base_dir+'\\imu_gps.txt'

imgs_names = glob.glob(base_dir+"\\*.hdr")

imu_base = pd.read_csv(imu_gps_name, sep="	")
lat = []
lon = []
# with open('100128_voo_11_120m_5ms_2021_07_21_13_10_49\\gpsMonitor.json') as json_file:
#     data = json.load(json_file)
#     for i, cord in enumerate(data['polygons'][0]["array"]):
#         if i%2 == 0:
#             lon.append(cord)
#         else:
#             lat.append(cord)
#         print(i, cord)

fig, ax = plt.subplots()
leged = []
for hdr_name in imgs_names:
    try:
        array, img_frames = hdr.open(hdr_name)
    except:
        continue
    
    tiff_name = hdr_name.split("/")[-1].replace("hdr", "tiff")
    print(tiff_name)
    bounds = img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].min()].to_dict("records")
    bounds += img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].max()].to_dict("records")


    imu = imu_base.loc[imu_base['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]
    p = ax.plot(imu["Lat"], imu["Lon"])
    # imu.to_excel(tiff_name.replace("tiff", "xlsx"))
    view = imshow(array, title=tiff_name)
    # input("ok?")

    pt = lonlat2utm.TransformPoint(imu.iloc[0]["Lat"] ,imu.iloc[0]["Lon"] )
    p1 = lonlat2utm.TransformPoint(imu["Lat"].max() ,imu["Lon"].max() )
    p2 = lonlat2utm.TransformPoint(imu["Lat"].min() ,imu["Lon"].min() )

    lon = {"Max":p1[1],"Min":p2[1] }
    lat = {"Max":p1[0],"Min":p2[0] }
    
    print("lat", lat)
    print("pt", pt)
    print("lon", lon)
    lon_decreasing = 1 if is_decreasing(imu, "Lat") else -1
    lat_decreasing = 1 if is_decreasing(imu, "Lon") else -1
    print(lat_decreasing, lon_decreasing, get_pixel_len(100))
    boundary = {}
    boundary["lat"] = lat["Min"] if lat_decreasing > 0 else lat["Max"]
    boundary["lon"] = lon["Min"] if lon_decreasing > 0 else lon["Max"]
    # boundary["lat"] =   pt[0] #+ -1*lat_decreasing*get_pixel_len(100)*320
    # boundary["lon"] = pt[1] #+ -1*lon_decreasing*get_pixel_len(100)*320
    print(boundary)
    transform = [boundary["lat"], lat_decreasing*get_pixel_len(100),0 , boundary["lon"],0 , lon_decreasing*get_pixel_len(100) ]
    print("transform",transform)
    leged.append(mpatches.Patch(color=p[0].get_color(), label=tiff_name))
    raster.CreateGeoTiff(tiff_name, array, transform, target.ExportToWkt())


ax.legend(handles=leged)
plt.show()
input("ok?")
# view = imshow(array)
# input()