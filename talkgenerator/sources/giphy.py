import os
from pathlib import Path

import safygiphy
from cachier import cachier

from talkgenerator.util import os_util
from util.image_data import ImageData

giphy_connection = safygiphy.Giphy()


def get_related_giphy(seed_word):
    if bool(seed_word):
        response = giphy_connection.random(tag=seed_word)
    else:
        response = giphy_connection.random()

    if bool(response):
        data = response.get("data")
        if bool(data):
            creator = data['username'] if "username" in data and len(data["username"].strip()) > 0 else None
            images = data.get("images")
            original = images.get("original")
            giphy_url = original.get("url")
            gif_name = os.path.basename(os.path.dirname(giphy_url))
            filename = "downloads/giphy/" + str(seed_word) + "/" + gif_name + ".gif"
            image_url = os_util.to_actual_file(filename)
            os_util.download_image(giphy_url, image_url)
            return ImageData(image_url=image_url, source=creator)


def get_random_giphy(_):
    return get_related_giphy(None)
