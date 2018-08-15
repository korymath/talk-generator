import random
from functools import lru_cache

import requests
from bs4 import BeautifulSoup

import scraper_util

search_url = "https://www.shitpostbot.com/gallery/sourceimages?query={" \
             "}&review_state=accepted&order=total_rating&direction=DESC&page={} "


@lru_cache(maxsize=20)
def _search_shitpostbot_page(search_term, page):
    url = search_url.format(search_term, page, search_term.replace(' ', '+'))
    page = requests.get(url)
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')

        post_entries = soup.find_all('div', class_='col-md-4')
        image_urls = []
        for entry in post_entries:
            # Check if author doesn't have the search term (False positive)
            user = entry.find("div", class_="caption").find_all("p")[1].find("a").get_text()
            if search_term in user:
                continue

            # Get real image url
            image_url = entry.find("img").get("src")
            image_url = _get_source_image(image_url)
            image_urls.append(image_url)

        print(image_urls)
        return image_urls


source_image_prefix = "https://www.shitpostbot.com/img/sourceimages/"


def _get_source_image(image_url):
    image_url = image_url.replace("%2F", "/")
    last_slash_idx = image_url.rfind("/")
    image_file_name = image_url[last_slash_idx + 1:]
    return source_image_prefix + image_file_name


def get_random_image(_):
    return random.choice(_search_shitpostbot_page("", random.choice(range(150))))


_search_image_function = scraper_util.create_page_scraper(_search_shitpostbot_page)


def search_images(search_term, amount=50):
    return _search_image_function(search_term,amount)
