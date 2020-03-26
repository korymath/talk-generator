import logging
from pathlib import Path
from typing import List

from cachier import cachier
from pixabay import Image
from talkgenerator import settings
from talkgenerator.datastructures.image_data import ImageData

logging.getLogger("pixabay").setLevel(logging.DEBUG)
logger = logging.getLogger("talkgenerator")


def get_pixabay_session():
    creds = settings.pixabay_auth()
    api = Image(api_key=creds["pixabay_key"])
    return api


pixabay_session = get_pixabay_session()


def search_horizontal(query):
    return search_photos(query, orientation="horizontal")


@cachier(cache_dir=Path("..", "tmp").absolute())
def search_photos(query, orientation="all") -> List[ImageData]:
    if pixabay_session:
        results = pixabay_session.search(q=query, orientation=orientation)
        if results and results["hits"]:
            images = []
            for photo in results["hits"]:
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
