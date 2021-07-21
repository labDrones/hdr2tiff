from osgeo import gdal
import numpy as np

def CreateGeoTiff(outRaster, data, geo_transform, projection):
    driver = gdal.GetDriverByName('GTiff')
    rows, cols, no_bands = data.shape
    DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_Byte)
    DataSet.SetGeoTransform(geo_transform)
    DataSet.SetProjection(projection)

    data = np.moveaxis(data, -1, 0)

    for i, image in enumerate(data, 1):
        DataSet.GetRasterBand(i).WriteArray(image)
    DataSet = None