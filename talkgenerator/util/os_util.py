import ntpath
import os
import logging
import pathlib
import sys
import traceback
from functools import lru_cache
from typing import Union

import requests
from PIL import Image
from PIL.Image import DecompressionBombError

# import tempfile
from schema.image_generator import ImageData

logger = logging.getLogger("talkgenerator")


def download_image(from_url, to_url):
    """Download image from url to path."""
    # Create the parent folder if it doesn't exist
    dir_path = pathlib.Path(os.path.dirname(to_url))
    dir_path.mkdir(parents=True, exist_ok=True)
    # tempfile.mkdtemp(dir=dir_path)

    # Download
    f = open(to_url, "wb")
    # f = tempfile.NamedTemporaryFile('wb', dir=to_url)
    f.write(requests.get(from_url, allow_redirects=True).content)
    f.close()


def get_file_name(url):
    return ntpath.basename(url)


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
        return _is_image_path(content.get_image_url())
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


@lru_cache(maxsize=20)
def is_valid_image(image_url):
    try:
        im = open_image(os.path.normpath(image_url))
        if not im or im in get_prohibited_images():
            logger.warning("Image denied because on blacklist:" + image_url)
            return False
    except (OSError, SyntaxError) as e:
        # traceback.print_exc(file=sys.stdout)
        logger.error("The image format is not valid for: {}".format(e))
        return False

    return True


def show_logs(given_logger: object) -> object:
    given_logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    given_logger.addHandler(handler)
