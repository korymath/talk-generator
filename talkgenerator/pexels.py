import logging

from cachier import cachier
from pexels_api import API
from talkgenerator import settings


logging.getLogger("pexels").setLevel(logging.DEBUG)
logger = logging.getLogger("talkgenerator")


def get_pexels_session():
    creds = settings.pexels_auth()
    api = API(creds["pexels_key"])
    return api


pexels_session = get_pexels_session()


@cachier(cache_dir="../.cache")
def search_photos_return_urls(query):
    if pexels_session:
        results = pexels_session.search(query)
        if results and results["photos"]:
            image_urls = []
            for photo in results["photos"]:
                link_download = photo["url"]
                image_urls.append(link_download)
            return image_urls
        else:
            logger.warning(
                'pexels could not find results for "{}", which might be due to missing/erroneous access keys'
            )
    else:
        logger.warning("No active pexels session due to missing/wrong credentials.")
