import ntpath
import os
import pathlib
from functools import lru_cache

import requests
from PIL import Image


def download_image(from_url, to_url):
    """Download image from url to path."""
    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(to_url)).mkdir(parents=True, exist_ok=True)

    # Download
    f = open(to_url, 'wb')
    f.write(requests.get(from_url).content)
    f.close()


def get_file_name(url):
    return ntpath.basename(url)


def to_actual_file(file):
    # if file.startswith('..'):
    this_folder = os.path.dirname(os.path.abspath(__file__))
    # folder = this_folder
    # while file.startswith('../'):
    #     folder = os.path.dirname(folder)
    #     file = file[3:]
    # actual_file = os.path.join(folder, file)
    actual_file = os.path.join(this_folder, file)
    return actual_file
    # return file


@lru_cache(maxsize=20)
def read_lines(file):
    actual_file = to_actual_file(file)
    return [line.rstrip('\n') for line in open(actual_file)]


@lru_cache(maxsize=20)
def open_image(file):
    return Image.open(file)


_PROHIBITED_IMAGES_DIR = "../data/images/prohibited/"


@lru_cache(maxsize=1)
def get_prohibited_images():
    actual_dir = to_actual_file(_PROHIBITED_IMAGES_DIR)
    return list(
        [open_image(actual_dir + url) for url in os.listdir(actual_dir)])


@lru_cache(maxsize=20)
def is_image(content):
    if not bool(content):
        return False
    lower_url = content.lower()
    return ".jpg" in lower_url or ".gif" in lower_url or ".png" in lower_url or ".jpeg" in lower_url


@lru_cache(maxsize=20)
def is_valid_image(image_url):
    try:
        im = open_image(image_url)
        if im in get_prohibited_images():
            print(image_url, " IS DENIED")
            return False
    except OSError as e:
        print(e)
        return False

    return True
