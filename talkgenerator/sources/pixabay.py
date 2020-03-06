import logging

from cachier import cachier
from pixabay import Image
from talkgenerator import settings


logging.getLogger("pixabay").setLevel(logging.DEBUG)
logger = logging.getLogger("talkgenerator")


def get_pixabay_session():
    creds = settings.pixabay_auth()
    api = Image(api_key=creds["pixabay_key"])
    return api


pixabay_session = get_pixabay_session()


@cachier(cache_dir="../.cache")
def search_photos_return_urls(query):
    if pixabay_session:
        results = pixabay_session.search(q=query)
        if results and results["hits"]:
            image_urls = []
            for photo in results["hits"]:
                link_download = photo["largeImageURL"]
                image_urls.append(link_download)
            return image_urls
        else:
            logger.warning(
                'Pixabay could not find results for "{}", which might be due to missing/erroneous access keys'
            )
    else:
        logger.warning("No active Pixabay session due to missing/wrong credentials.")
