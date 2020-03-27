import random
from functools import lru_cache
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from cachier import cachier

from talkgenerator.util import scraper_util

_MAX_RANDOM_PAGE = 150
_SEARCH_URL = (
    "https://www.shitpostbot.com/gallery/sourceimages?query={"
    "}&review_state=accepted&order=total_rating&direction=DESC&page={} "
)


def _search_shitpostbot_page(search_term, page):
    return [element[1] for element in _search_shitpostbot_page_rated(search_term, page)]


@lru_cache(maxsize=20)
@cachier(cache_dir=Path("..", "tmp").absolute())
def _search_shitpostbot_page_rated(search_term, page):
    url = _SEARCH_URL.format(search_term, page, search_term.replace(" ", "+"))
    page = requests.get(url)
    if page:
        soup = BeautifulSoup(page.content, "html.parser")

        post_entries = soup.find_all("div", class_="col-md-4")
        image_urls = []
        for entry in post_entries:
            # Check if author doesn't have the search term (False positive)
            user = (
                entry.find("div", class_="caption")
                .find_all("p")[1]
                .find("a")
                .get_text()
            )
            if bool(search_term) and search_term in user:
                continue

            # Get real image url
            image_url = entry.find("img").get("src")
            image_url = _get_source_image(image_url)
            rating_div = entry.find("span", class_="rating")
            rating = int(rating_div.text if rating_div else 1)
            if rating > 0:
                image_urls.append((rating, image_url))

        return image_urls


source_image_prefix = "https://www.shitpostbot.com/img/sourceimages/"


def _get_source_image(image_url):
    image_url = image_url.replace("%2F", "/")
    last_slash_idx = image_url.rfind("/")
    image_file_name = image_url[last_slash_idx + 1 :]
    return source_image_prefix + image_file_name


def get_random_images(_):
    images = _search_shitpostbot_page("", random.choice(range(_MAX_RANDOM_PAGE)))
    return images


def get_random_images_rated(_):
    images = _search_shitpostbot_page_rated("", random.choice(range(_MAX_RANDOM_PAGE)))
    return images


_search_image_function = scraper_util.create_page_scraper(_search_shitpostbot_page)
_search_image_function_rated = scraper_util.create_page_scraper(
    _search_shitpostbot_page_rated
)


def search_images(search_term, number=50):
    return _search_image_function(search_term, number)


def search_images_rated(search_term, number=50):
    return _search_image_function_rated(search_term, number)
