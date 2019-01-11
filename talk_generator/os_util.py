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


@lru_cache(maxsize=20)
def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]


@lru_cache(maxsize=20)
def open_image(file):
    return Image.open(file)


_PROHIBITED_IMAGES_DIR = "../data/images/prohibited/"


@lru_cache(maxsize=1)
def getProhibitedImages():
    return list(
            [open_image(_PROHIBITED_IMAGES_DIR + url) for url in os.listdir(_PROHIBITED_IMAGES_DIR)])


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
        if im in getProhibitedImages():
            print(image_url, " IS DENIED")
            return False
    except OSError as e:
        print(e)
        return False

    return True
