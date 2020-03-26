import ntpath
import os
import logging
import pathlib
import sys
from functools import lru_cache
from typing import Union

import requests
from PIL import Image
from PIL.Image import DecompressionBombError

# import tempfile
from talkgenerator.datastructures.image_data import ImageData

logger = logging.getLogger("talkgenerator")


def to_actual_file(filename=""):
    """Return the path to the filename specified.
    This is used most often to get the path of data files."""

    util_folder = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(util_folder, filename)


@lru_cache(maxsize=20)
def read_lines(filename):
    actual_file = to_actual_file(filename)
    return [line.rstrip("\n") for line in open(actual_file)]


@lru_cache(maxsize=20)
def open_image(filename):
    try:
        return Image.open(filename)
    except DecompressionBombError:
        return None


_PROHIBITED_IMAGES_DIR = "data/prohibited_images/"


@lru_cache(maxsize=1)
def get_prohibited_images():
    actual_dir = to_actual_file(_PROHIBITED_IMAGES_DIR)
    return list(
        [open_image(os.path.join(actual_dir, url)) for url in os.listdir(actual_dir)]
    )


@lru_cache(maxsize=20)
def is_image(content: Union[str, ImageData]):
    if isinstance(content, ImageData):
        return True
    else:
        return _is_image_path(content)


def _is_image_path(content: str):
    if not bool(content) or bool(content) is content or not content.lower:
        return False
    lower_url = content.lower()
    return (
        ".jpg" in lower_url
        or ".gif" in lower_url
        or ".png" in lower_url
        or ".jpeg" in lower_url
    )


def show_logs(given_logger: logging.Logger):
    given_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    given_logger.addHandler(handler)
