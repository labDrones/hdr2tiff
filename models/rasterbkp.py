from spectral import image
from osgeo import gdal
import numpy as np

def CreateGeoTiff(outRaster, data, geo_transform, projection):
    driver = gdal.GetDriverByName('GTiff')
    rows, cols, no_bands = data.shape
    print("bands:", no_bands)
    DataSet = driver.Create(outRaster, cols, rows, no_bands, gdal.GDT_UInt16)
    DataSet.SetGeoTransform(geo_transform)
    DataSet.SetProjection(projection)

    # data = np.moveaxis(data, -1, 0)

    for i  in range(no_bands):
        image = np.squeeze(data[:,:, i], axis=(2,))
        # print(i)
        DataSet.GetRasterBand(i+1).WriteArray(image)
    DataSet = None