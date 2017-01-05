#!/usr/bin/env python

from osgeo import gdal
import osr

format = "GTiff"
driver = gdal.GetDriverByName( format )
metadata = driver.GetMetadata()
print(gdal.DCAP_CREATE)
gdal_dcap_create = metadata.get(gdal.DCAP_CREATE)
print(gdal_dcap_create)

filename = "test-1x1x1-byte.tif"
dataset = driver.Create(filename, 1, 1, 1, gdal.GDT_Byte)
dataset.SetGeoTransform( [ 444720, 30, 0, 3751320, 0, -30 ] )

srs = osr.SpatialReference()
srs.SetUTM(11, 1)
srs.SetWellKnownGeogCS('NAD27')
dataset.SetProjection(srs.ExportToWkt())