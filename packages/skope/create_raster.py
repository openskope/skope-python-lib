
import argparse
import osr

from osgeo import gdal
from skope.raster_file import RasterDataType
from skope.raster_file import RasterFile


def create_raster(filename, format='GTiff', origin=(0,0), pixel_size=(1.0, 1.0),
    extent_in_pixels=(1,1), band_count=1, data_type=RasterDataType.BYTE, nodata_value=None) -> RasterFile:

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
    args = parser.parse_args()

    create_raster(
        args.filename,
        pixel_size=(0.0083333,0.0083333),
        extent_in_pixels=(12,12),
        origin=(-114.0, 43.0)
    )