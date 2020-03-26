import logging
from pathlib import Path
from typing import List

from cachier import cachier
from pexels_api import API
from talkgenerator import settings
from talkgenerator.datastructures.image_data import ImageData

logging.getLogger("pexels").setLevel(logging.DEBUG)
logger = logging.getLogger("talkgenerator")


def get_pexels_session():
    creds = settings.pexels_auth()
    api = API(creds["pexels_key"])
    return api


pexels_session = get_pexels_session()


@cachier(cache_dir=Path("..", "tmp").absolute())
def _search_pexels(query):
    return pexels_session.search(query)


def search_photos(query) -> List[ImageData]:
    if pexels_session:
        results = _search_pexels(query)
        if results and results["photos"]:
            images = []
            for photo in results["photos"]:
                source = photo["src"]
                # link_download = (
                #     source["large"]
                #     if "large" in source
                #     else (source["original"] if "original" in source else photo["url"])
                # )
                link_download = source["original"]
                creator = (
                    (photo["photographer"] + " (via Pexels)")
                    if "photographer" in photo
                    else None
                )
                images.append(ImageData(image_url=link_download, source=creator))
            return images
        else:
            logger.warning(
                'pexels could not find results for "{}", which might be due to missing/erroneous access keys'.format(
                    query
                )
            )
    else:
        logger.warning("No active pexels session due to missing/wrong credentials.")
