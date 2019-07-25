""" Module for interacting with Wikihow """

import logging
from talkgenerator import settings

from pyunsplash import PyUnsplash

# pyunsplash logger defaults to level logging.ERROR
# If you need to change that, use getLogger/setLevel
# on the module logger, like this:
logging.getLogger("pyunsplash").setLevel(logging.DEBUG)


def get_unsplash_session():
    try:
        creds = settings.unsplash_auth()
        # instantiate PyUnsplash object
        api = PyUnsplash(api_key=creds['unsplash_access_key'])
        return api
    except FileNotFoundError:
        print(
            "Warning: No login credentials were found for Unsplash. Please add these credentials file to .env.")

pu = get_unsplash_session()

def search_photos_return_urls(query):
    results = pu.search(type_='photos', query=query)
    image_urls = []
    for photo in results.entries:
        link_download = photo.link_download
        image_urls.append(link_download)
    return image_urls