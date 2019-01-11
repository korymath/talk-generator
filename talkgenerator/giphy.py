import safygiphy
import os
from talkgenerator import os_util

giphy = safygiphy.Giphy()


def get_related_giphy(seed_word):
    if bool(seed_word):
        response = giphy.random(tag=seed_word)
    else:
        response = giphy.random()

    if bool(response):
        data = response.get('data')
        if bool(data):
            images = data.get('images')
            original = images.get('original')
            giphy_url = original.get('url')
            gif_name = os.path.basename(os.path.dirname(giphy_url))
            image_url = '../downloads/giphy/' + str(seed_word) + "/" + gif_name + ".gif"
            os_util.download_image(giphy_url, image_url)
            return image_url

