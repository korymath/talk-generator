""" Module for interacting with Wikihow """

import logging
from pathlib import Path

from cachier import cachier
from pyunsplash import PyUnsplash

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
    if unsplash_session:
        results = unsplash_session.search(type_="photos", query=query)
        if results and results.body:
            image_urls = []
            for photo in results.entries:
                link_download = photo.link_download
                image_urls.append(link_download)
            return image_urls
        else:
            logger.warning(
                'Unsplash could not find results for "{}", which might be due to missing/erroneous access keys'
            )
    else:
        logger.warning("No active Unsplash session due to missing/wrong credentials.")
