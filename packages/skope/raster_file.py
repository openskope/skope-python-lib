#!/usr/bin/env python

import osr

from enum import Enum
from osgeo import gdal
from gdalconst import GA_ReadOnly

class RasterDataType(Enum): (UNKNOWN, BYTE, UINT16, INT16, 
                             UINT32, INT32, FLOAT32, FLOAT64, 
                             CINT16, CINT32, CFLOAT32, CFLOAT64) = range(12)

class RasterFile:

    def __init__(self, filename=None, dataset=None):
        
        if dataset is not None:
            self.dataset = dataset
        else:
            self.dataset = gdal.Open(filename, GA_ReadOnly)
            if self.dataset is None:
                raise Exception ("Could not open raster file: " + filename)
            
        # store given dataset properties
        self.filename = self.dataset.GetDescription()

        self.metadata = self.dataset.GetMetadata_Dict()
        self.format = self.dataset.GetDriver().LongName
        self.projection = self.dataset.GetProjection()
        self.geotransform = self.dataset.GetGeoTransform()
        self.extent_in_pixels_lng = self.dataset.RasterXSize
        self.extent_in_pixels_lat = self.dataset.RasterYSize
        self.band_count = self.dataset.RasterCount

        # derive additional dataset properties
        self.origin_lng = self.geotransform[0]
        self.origin_lat = self.geotransform[3]
        self.pixel_size_lng = abs(self.geotransform[1])
        self.pixel_size_lat = abs(self.geotransform[5])
        self.pixels_per_degree_lng = int(1.0/self.pixel_size_lng)
        self.pixels_per_degree_lat = int(1.0/self.pixel_size_lat)
        self.extent_in_degrees_lng = self.extent_in_pixels_lng * self.pixel_size_lng
        self.extent_in_degrees_lat = self.extent_in_pixels_lat * self.pixel_size_lat

        # extract properties of band 1 
        band = self.dataset.GetRasterBand(1)
        self.block_size_x, self.block_size_y = band.GetBlockSize()
        self.no_data_value = band.GetNoDataValue()
        self.data_type = RasterDataType(band.DataType)
        self.data_type_name = RasterDataType(band.DataType).name

        # confirm that all bands have identical self.properties
        for band_index in range(1, self.band_count):
            band = self.dataset.GetRasterBand(band_index)
            if (band.GetBlockSize()[0] != self.block_size_x or
                band.GetBlockSize()[1] != self.block_size_y or
                band.GetNoDataValue() != self.no_data_value or
                RasterDataType(band.DataType) != self.data_type):
                    print('Bands 1 and {} have different properties.'.format(band_index))



    #    min = band.GetMinimum()
    #    max = band.GetMaximum()
    #    if min is None or max is None:
    #        (min,max) = band.ComputeRasterMinMax(1)

    #    print('Minimum value       {}'.format(min))
    #    print('Maximum value       {}'.format(max))


        # band_data = self.dataset.ReadRaster(xsize=blocksize_x, ysize=1)
        # print(len(band_data))

        # band = self.dataset.GetRasterBand(2000)