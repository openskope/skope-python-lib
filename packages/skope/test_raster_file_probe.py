import pytest
import raster_file_probe

filename = 'test-1x1x1-byte.tif'

@pytest.fixture
def properties():
    return raster_file_probe.get_dataset_properties(filename)

def test_get_dataset_properties_filename(properties):
    assert filename == properties['filename']

if __name__ == '__main__':
    pytest.main()