
import argparse
import osr

from osgeo import gdal
from skope.raster_file import RasterDataType
from skope.raster_file import RasterFile

DEFAULT_ORIGIN = [0,0]
DEFAULT_EXTENT_PIXELS = [1,1]
DEFAULT_BAND_COUNT=1
DEFAULT_PIXEL_SIZE = [1.0,1.0]
DEFAULT_DATA_TYPE = RasterDataType.BYTE
DEFAULT_FORMAT = 'GTiff'
DEFAULT_NODATA_VALUE=None

def create_raster(
        filename, 
        format=DEFAULT_FORMAT, 
        origin=DEFAULT_ORIGIN, 
        pixel_size=DEFAULT_PIXEL_SIZE,
        extent_in_pixels=DEFAULT_EXTENT_PIXELS, 
        band_count=DEFAULT_BAND_COUNT, 
        data_type=DEFAULT_DATA_TYPE, 
        nodata_value=DEFAULT_NODATA_VALUE) -> RasterFile:

    origin_lng, origin_lat = origin

    pixel_size_lng, pixel_size_lat = pixel_size
    extent_in_pixels_lng, extent_in_pixels_lat = extent_in_pixels

    driver = gdal.GetDriverByName(format)
    dataset = driver.Create(filename, extent_in_pixels_lng, extent_in_pixels_lat, band_count, data_type.value)
    dataset.SetGeoTransform([origin_lng, pixel_size_lng, 0, origin_lat, 0, -pixel_size_lat])
    srs = osr.SpatialReference()
    srs.SetUTM(11, 1)
    srs.SetWellKnownGeogCS('NAD27')
    dataset.SetProjection(srs.ExportToWkt())

    return RasterFile(dataset=dataset)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='file to create')
    parser.add_argument('--format', nargs=1, default=DEFAULT_FORMAT, help='raster file format')
    parser.add_argument('--origin', nargs=2, type=float, default=DEFAULT_ORIGIN, help='coordinates of origin')
    parser.add_argument('--pixels', nargs=2, type=int, default=DEFAULT_EXTENT_PIXELS, help='dimensions in pixels')
    parser.add_argument('--pixelsize', nargs=2, type=float, default=DEFAULT_PIXEL_SIZE, help='size of pixels')
    parser.add_argument('--bandcount', nargs=1, type=int, default=DEFAULT_BAND_COUNT, help='number of bands')
    parser.add_argument('--nodata', nargs=1, type=float, default=DEFAULT_NODATA_VALUE, help='value for pixels with no data')
    parser.add_argument('--datatype', nargs=1, default=DEFAULT_DATA_TYPE, help='type of each pixel')

    args = parser.parse_args()

    create_raster(
        args.filename,
        format=args.format,
        origin=args.origin,
        pixel_size=args.pixelsize,
        extent_in_pixels=args.pixels,
        band_count=args.bandcount,
        nodata_value=args.nodata
    )
