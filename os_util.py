import os
import pathlib
import ntpath

import requests


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


def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]
