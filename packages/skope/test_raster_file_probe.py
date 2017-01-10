import pytest
import sys

from raster_file import RasterFile

name_of_existing_file = 'test-1x1x1-byte.tif'
name_of_nonexisting_file = 'no_such_file'

@pytest.fixture
def dataset():
    return RasterFile(name_of_existing_file)

def test_init_with_existing_file_succeeds():
    dataset = RasterFile(name_of_existing_file)

def test_init_with_nonexisting_file_raises_exception():
    with pytest.raises(Exception):
        dataset = RasterFile(name_of_nonexisting_file)

def test_get_dataset_filename(dataset):
    assert dataset.filename == name_of_existing_file

if __name__ == '__main__':
    pytest.main()