
import argparse
import osr

from osgeo import gdal

from skope.raster_file import RasterFile

def print_properties(dataset):
    print('Format              {}'.format(dataset.format))
    print('Origin (deg)        {} lng, {} lat'.format(dataset.origin_lng, dataset.origin_lat))
    print('Pixel size (deg)    {:f} (1/{:d}) lng x {:f} (1/{:d}) lat'
        .format(dataset.pixel_size_lng, dataset.pixels_per_degree_lng, 
                dataset.pixel_size_lat, dataset.pixels_per_degree_lat))
    print('Raster extent (deg) {:f} lng x {:f} lat'
        .format(dataset.extent_in_degrees_lng, dataset.extent_in_degrees_lat))
    print('Raster extent (px)  {} x {} '
        .format(dataset.extent_in_pixels_lng, dataset.extent_in_pixels_lat))
    print('Number of bands     {}'.format(dataset.band_count))
    print('Block size          {} x {}'.format(dataset.block_size_x, dataset.block_size_y))
    print('No-data value       {}'.format(dataset.no_data_value))
    print('Pixel data type     {}'.format(dataset.data_type_name))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='file to probe')
    args = parser.parse_args()

    dataset = RasterFile(args.filename)
    print_properties(dataset)