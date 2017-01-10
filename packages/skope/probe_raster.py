
import argparse
import osr

from osgeo import gdal

from skope.raster_file import RasterFile

def print_properties(dataset):
    
    print_row('Format', 
        dataset.format )
    
    print_row('Origin (deg)', '{}, {}'.format(
        dataset.origin_lng, 
        dataset.origin_lat))
    
    print_row('Pixel size (deg)', '{:f} x {:f} (1/{:d} x 1/{:d})'.format(
        dataset.pixel_size_lng,
        dataset.pixel_size_lat, 
        dataset.pixels_per_degree_lng, 
        dataset.pixels_per_degree_lat))
    
    print_row('Raster extent (deg)', '{:f} x {:f}'.format(
        dataset.extent_in_degrees_lng,
        dataset.extent_in_degrees_lat))
    
    print_row('Raster extent (px)', '{} x {}'.format(
        dataset.extent_in_pixels_lng, 
        dataset.extent_in_pixels_lat))
    
    print_row('Number of bands',
        dataset.band_count)
    
    print_row('Block size', '{} x {}'.format(
        dataset.block_size_x, 
        dataset.block_size_y))
    
    print_row('No-data value', 
        dataset.no_data_value)

    print_row('Pixel data type', 
        dataset.data_type_name)

def print_row(label, value):
    print('{} | {}'.format(label.ljust(19), value))

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='file to probe')
    args = parser.parse_args()

    dataset = RasterFile(args.filename)
    print_properties(dataset)