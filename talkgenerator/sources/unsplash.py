""" Module for interacting with Wikihow """

import logging
from json import JSONDecodeError
from pathlib import Path
from typing import List

from cachier import cachier
from pyunsplash import PyUnsplash

from talkgenerator.datastructures.image_data import ImageData
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


def _map_to_image_data(photo):
    link_download = photo.link_download
    creator_user = photo.body["user"]
    creator_name = None
    if creator_user:
        creator_name = creator_user["name"] + " (Unsplash)"
    return ImageData(image_url=link_download, source=creator_name)


@cachier(cache_dir=Path("..", "tmp").absolute())
def search_photos_return_urls(query):
    return [im.get_image_url() for im in search_photos(query)]


def random(_=None):
    try:
        random_image = unsplash_session.photos(type_="random")
        image_url = random_image.body["links"]["download"]
        creator_name = random_image.body["user"]["name"]
        return ImageData(image_url=image_url, source=creator_name)
    except JSONDecodeError:
        logger.warning("Couldn't get random Unsplash image")
        return None


def random_as_list(_=None):
    result = random(_)
    if result:
        return [result]
    else:
        return []


@cachier(cache_dir=Path("..", "tmp").absolute())
def search_photos(query) -> List[ImageData]:
    if unsplash_session:
        results = unsplash_session.search(type_="photos", query=query)
        if results and results.body:
            images = []
            for photo in results.entries:
                images.append(_map_to_image_data(photo))
            return images
        else:
            logger.warning(
                'Unsplash could not find results for "{}", which might be due to missing/erroneous access keys'.format(
                    query
                )
            )
    else:
        logger.warning("No active Unsplash session due to missing/wrong credentials.")
