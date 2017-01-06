#!/usr/bin/env python

import optparse
import sys

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
        self.properties = { 
            'filename': self.dataset.GetDescription(),
            'metadata': self.dataset.GetMetadata_Dict(),
            'format': self.dataset.GetDriver().LongName,
            'projection': self.dataset.GetProjection(),
            'geotransform': self.dataset.GetGeoTransform(),
            'extent_in_pixels_lng': self.dataset.RasterXSize,
            'extent_in_pixels_lat': self.dataset.RasterYSize,
            'band_count': self.dataset.RasterCount
        }

        # derive additional dataset properties
        self.properties['origin_lng'] = self.properties['geotransform'][0]
        self.properties['origin_lat'] = self.properties['geotransform'][3]
        self.properties['pixel_size_lng'] = abs(self.properties['geotransform'][1])
        self.properties['pixel_size_lat'] = abs(self.properties['geotransform'][5])
        self.properties['pixels_per_degree_lng'] = int(1.0 / self.properties['pixel_size_lng'])
        self.properties['pixels_per_degree_lat'] = int(1.0 / self.properties['pixel_size_lat'])
        self.properties['extent_in_degrees_lng'] = self.properties['extent_in_pixels_lng'] * self.properties['pixel_size_lng']
        self.properties['extent_in_degrees_lat'] = self.properties['extent_in_pixels_lat'] * self.properties['pixel_size_lat']

        # extract self.properties of band 1 
        band = self.dataset.GetRasterBand(1)
        self.properties['block_size_x'], self.properties['block_size_y']= band.GetBlockSize()
        self.properties['no_data_value'] = band.GetNoDataValue()
        self.properties['data_type'] = RasterDataType(band.DataType)
        self.properties['data_type_name'] = RasterDataType(band.DataType).name

        # confirm that all bands have identical self.properties
        for band_index in range(1, self.properties['band_count']):
            band = self.dataset.GetRasterBand(band_index)
            if (band.GetBlockSize()[0] != self.properties['block_size_x'] or
                band.GetBlockSize()[1] != self.properties['block_size_y'] or
                band.GetNoDataValue() != self.properties['no_data_value'] or
                RasterDataType(band.DataType) != self.properties['data_type']):
                println("Bands 1 and " + band_index + " have different self.properties.")


    def print_properties(self):

        print('Format              {}'
            .format(self.properties['format']))
        print('Origin (deg)        {} lng, {} lat'
            .format(self.properties['origin_lng'], self.properties['origin_lat']))
        print('Pixel size (deg)    {:f} (1/{:d}) lng x {:f} (1/{:d}) lat'
            .format(self.properties['pixel_size_lng'],  self.properties['pixels_per_degree_lng'], 
                    self.properties['pixel_size_lat'], self.properties['pixels_per_degree_lat']))
        print('Raster extent (deg) {:f} lng x {:f} lat'
            .format(self.properties['extent_in_degrees_lng'], self.properties['extent_in_degrees_lat']))
        print('Raster extent (px)  {} x {} '
            .format(self.properties['extent_in_pixels_lng'], self.properties['extent_in_pixels_lat']))
        print('Number of bands     {}'
            .format(self.properties['band_count']))
        print('Block size          {} x {}'
            .format(self.properties['block_size_x'], self.properties['block_size_y']))
        print('No-data value       {}'
            .format(self.properties['no_data_value']))
        print('Pixel data type     {}'
            .format(self.properties['data_type_name']))

    #    min = band.GetMinimum()
    #    max = band.GetMaximum()
    #    if min is None or max is None:
    #        (min,max) = band.ComputeRasterMinMax(1)

    #    print('Minimum value       {}'.format(min))
    #    print('Maximum value       {}'.format(max))


        # band_data = self.dataset.ReadRaster(xsize=blocksize_x, ysize=1)
        # print(len(band_data))

        # band = self.dataset.GetRasterBand(2000)

if __name__ == '__main__':
    
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()

    if len(args) != 1:
        print("\n***** ERROR: Required argument path_to_raster_file was not provided *****\n")
        exit()

    dataset = RasterFile(args[0])
    dataset.print_properties()