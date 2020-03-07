""" Module for interacting with Wikihow """

import logging
from pathlib import Path
from typing import List

from cachier import cachier
from pyunsplash import PyUnsplash

from util.image_data import ImageData
from talkgenerator import settings

# pyunsplash logger defaults to level logging.ERROR
# If you need to change that, use getLogger/setLevel
# on the module logger, like this:
logging.getLogger("pyunsplash").setLevel(logging.DEBUG)
logger = logging.getLogger("talkgenerator")


def get_unsplash_session():
    creds = settings.unsplash_auth()
    # instantiate PyUnsplash object
    api = PyUnsplash(api_key=creds["unsplash_access_key"])
    return api


unsplash_session = get_unsplash_session()


@cachier(cache_dir=Path("..", ".cache").absolute())
def search_photos_return_urls(query):
    return [im.get_image_url() for im in search_photos(query)]


@cachier(cache_dir=Path("..", ".cache").absolute())
def search_photos(query) -> List[ImageData]:
    if unsplash_session:
        results = unsplash_session.search(type_="photos", query=query)
        if results and results.body:
            images = []
            for photo in results.entries:
                link_download = photo.link_download
                creator_user = photo.body["user"]
                creator_name = None
                if creator_user:
                    creator_name = creator_user['name'] + ' (Unsplash)'
                images.append(ImageData(image_url=link_download, source=creator_name))
            return images
        else:
            logger.warning(
                'Unsplash could not find results for "{}", which might be due to missing/erroneous access keys'
            )
    else:
        logger.warning("No active Unsplash session due to missing/wrong credentials.")
