#!/usr/bin/env python

import optparse
from enum import Enum
from osgeo import gdal
from gdalconst import GA_ReadOnly

class RasterDataType(Enum): (UNKNOWN, BYTE, UINT16, INT16, 
                             UINT32, INT32, FLOAT32, FLOAT64, 
                             CINT16, CINT32, CFLOAT32, CFLOAT64) = range(12)

def get_dataset(filename):
    return gdal.Open(filename, GA_ReadOnly)

def get_dataset_properties(filename):
    dataset = get_dataset(filename)
    return get_properties(dataset)

def get_properties(dataset):

    # store given dataset properties
    properties = { 
        'filename': dataset.GetDescription(),
        'metadata': dataset.GetMetadata_Dict(),
        'format': dataset.GetDriver().LongName,
        'projection': dataset.GetProjection(),
        'geotransform': dataset.GetGeoTransform(),
        'extent_in_pixels_lng': dataset.RasterXSize,
        'extent_in_pixels_lat': dataset.RasterYSize,
        'band_count': dataset.RasterCount
    }

    # derive additional dataset properties
    properties['origin_lng'] = properties['geotransform'][0]
    properties['origin_lat'] = properties['geotransform'][3]
    properties['pixel_size_lng'] = abs(properties['geotransform'][1])
    properties['pixel_size_lat'] = abs(properties['geotransform'][5])
    properties['pixels_per_degree_lng'] = int(1.0 / properties['pixel_size_lng'])
    properties['pixels_per_degree_lat'] = int(1.0 / properties['pixel_size_lat'])
    properties['extent_in_degrees_lng'] = properties['extent_in_pixels_lng'] * properties['pixel_size_lng']
    properties['extent_in_degrees_lat'] = properties['extent_in_pixels_lat'] * properties['pixel_size_lat']

    # extract properties of band 1 
    band = dataset.GetRasterBand(1)
    properties['block_size_x'], properties['block_size_y']= band.GetBlockSize()
    properties['no_data_value'] = band.GetNoDataValue()
    properties['data_type'] = RasterDataType(band.DataType)
    properties['data_type_name'] = RasterDataType(band.DataType).name

    # confirm that all bands have identical properties
    for band_index in range(1, properties['band_count']):
        band = dataset.GetRasterBand(band_index)
        if (band.GetBlockSize()[0] != properties['block_size_x'] or
            band.GetBlockSize()[1] != properties['block_size_y'] or
            band.GetNoDataValue() != properties['no_data_value'] or
            RasterDataType(band.DataType) != properties['data_type']):
            println("Bands 1 and " + band_index + " have different properties.")

    return properties


def print_dataset_properties(properties):

    print('Format              {}'
        .format(properties['format']))
    print('Origin (deg)        {} lng, {} lat'
        .format(properties['origin_lng'], properties['origin_lat']))
    print('Pixel size (deg)    {:f} (1/{:d}) lng x {:f} (1/{:d}) lat'
        .format(properties['pixel_size_lng'],  properties['pixels_per_degree_lng'], 
                properties['pixel_size_lat'], properties['pixels_per_degree_lat']))
    print('Raster extent (deg) {:f} lng x {:f} lat'
        .format(properties['extent_in_degrees_lng'], properties['extent_in_degrees_lat']))
    print('Raster extent (px)  {} x {} '
        .format(properties['extent_in_pixels_lng'], properties['extent_in_pixels_lat']))
    print('Number of bands     {}'
        .format(properties['band_count']))
    print('Block size          {} x {}'
        .format(properties['block_size_x'], properties['block_size_y']))
    print('No-data value       {}'
        .format(properties['no_data_value']))
    print('Pixel data type     {}'
        .format(properties['data_type_name']))

#    min = band.GetMinimum()
#    max = band.GetMaximum()
#    if min is None or max is None:
#        (min,max) = band.ComputeRasterMinMax(1)

#    print('Minimum value       {}'.format(min))
#    print('Maximum value       {}'.format(max))


    # band_data = dataset.ReadRaster(xsize=blocksize_x, ysize=1)
    # print(len(band_data))

    # band = dataset.GetRasterBand(2000)

if __name__ == '__main__':
    
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()

    if len(args) != 1:
        print("\n***** ERROR: Required argument path_to_raster_file was not provided *****\n")
        exit()

    dataset_properties = get_dataset_properties(args[0])
    print_dataset_properties(dataset_properties)