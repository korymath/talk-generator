import logging
import requests
from typing import List

from talkgenerator import settings
from talkgenerator.datastructures.image_data import ImageData

logging.getLogger("pixabay").setLevel(logging.DEBUG)
logger = logging.getLogger("talkgenerator")


def get_pixabay_session():
    creds = settings.pixabay_auth()
    api_key = creds["pixabay_key"]
    return api_key


def search_horizontal(query):
    return search_photos(query, orientation="horizontal")


def search_vertical(query):
    return search_photos(query, orientation="vertical")


def search_photos(query, orientation="all") -> List[ImageData]:
    api_key = get_pixabay_session()
    logger.debug("pixabay_api_key: {}".format(api_key))
    query = query.replace(' ', '+')
    logger.debug("pixabay.search_photos called with query: {}".format(query))
    url_query = f"https://pixabay.com/api/?key={api_key}&q={query}&image_type=photo&orientation={orientation}"
    logger.debug("pixabay url_query: {}".format(url_query))
    if api_key and url_query:
        results = requests.get(url=url_query)
        logger.debug("request response results: {}".format(results))
        response_data = results.json()
        if results.status_code == 200 and response_data["hits"]:
            images = []
            for photo in response_data["hits"]:
                link_download = photo["largeImageURL"]
                creator = photo["user"] + " (via Pixabay)" if "user" in photo else None
                images.append(ImageData(image_url=link_download, source=creator))
            return images
        else:
            logger.warning(
                'Pixabay could not find results for "{}", which might be due to missing/erroneous access keys'.format(
                    query
                )
            )
    else:
        logger.warning("No active Pixabay session due to missing/wrong credentials.")
