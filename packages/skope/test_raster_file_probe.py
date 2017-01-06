import pytest
from raster_file import RasterFile

filename = 'test-1x1x1-byte.tif'

@pytest.fixture
def properties():
    return RasterFile(filename).properties

def test_get_dataset_properties_filename(properties):
    assert filename == properties['filename']

if __name__ == '__main__':
    pytest.main()