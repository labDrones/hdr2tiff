
import sys 
from . import hdr
import pandas as pd
from osgeo import osr, gdal
import glob
import numpy as np
from tkinter import filedialog
from tkinter import *

import matplotlib.pyplot as  plt
import matplotlib.patches as mpatches



class Raster:
    def __init__(self) -> None:
        pass

def CreateGeoTiff(outRaster, data, geo_transform, projection, bands = []):
    driver = gdal.GetDriverByName('GTiff')
    if len(bands) > 0:
        rows, cols, _  = data.shape
    else:
        rows, cols, no_bands = data.shape
        bands = range(no_bands)

    DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_UInt16)
    DataSet.SetGeoTransform(geo_transform)
    DataSet.SetProjection(projection)
    
    for i  in bands:
        image = np.squeeze(data[:,:, i], axis=(2,))
        # print(i)
        DataSet.GetRasterBand(i+1).WriteArray(image)
    DataSet = None

def get_pixel_len(alt, fov):
    '''
    Returns pixel Nano-Hyperspec pixel len in cm
    '''
    # fov = 22.1
    ifov = (fov/640)*(17.44)*(10**-3)
    len = ifov*alt
    return len

def is_decreasing(imu, col):
    return not round(imu.iloc[0][col], 7) > round(imu.iloc[500][col],7)
    

def get_tiffs(base_dir, voo_alt= 100, fov = 22.1):
    source = osr.SpatialReference()
    source.ImportFromEPSG(4326)

    target = osr.SpatialReference()
    target.ImportFromEPSG(32722)

    lonlat2utm = osr.CoordinateTransformation(source, target)
    base_dir = base_dir.replace("/", "\\")
    imu_gps_name = base_dir+'\\imu_gps.txt'

    imgs_names = glob.glob(base_dir+"\\*.hdr")

    imu_base = pd.read_csv(imu_gps_name, sep="	")
    for hdr_name in imgs_names:
        try:
            array, img_frames = hdr.open(hdr_name)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            continue
        
        tiff_name = hdr_name.split("/")[-1].replace("hdr", "tiff")
        bounds = img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].min()].to_dict("records")
        bounds += img_frames.loc[img_frames["Frame#"] == img_frames["Frame#"].max()].to_dict("records")


        imu = imu_base.loc[imu_base['Timestamp'].between( bounds[0]["Timestamp"],bounds[-1]["Timestamp"])]
        p1 = lonlat2utm.TransformPoint(imu["Lat"].max() ,imu["Lon"].max() )
        p2 = lonlat2utm.TransformPoint(imu["Lat"].min() ,imu["Lon"].min() )

        lon = {"Max":p1[1],"Min":p2[1] }
        lat = {"Max":p1[0],"Min":p2[0] }

        lon_decreasing = 1 if is_decreasing(imu, "Lat") else -1
        lat_decreasing = 1 if is_decreasing(imu, "Lon") else -1
        boundary = {}
        boundary["lat"] = lat["Min"] if lat_decreasing > 0 else lat["Max"]
        boundary["lon"] = lon["Min"] if lon_decreasing > 0 else lon["Max"]
        transform = [boundary["lat"], lat_decreasing*get_pixel_len(voo_alt, fov),0 , boundary["lon"],0 , lon_decreasing*get_pixel_len(voo_alt, fov) ]

        # leged.append(mpatches.Patch(color=p[0].get_color(), label=tiff_name))
        CreateGeoTiff(tiff_name, array, transform, target.ExportToWkt())