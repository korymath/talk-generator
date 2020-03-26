from functools import lru_cache
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from cachier import cachier

from talkgenerator.util import scraper_util

quote_search_url = (
    "https://www.goodreads.com/search?page={}&q={"
    "}&search%5Bsource%5D=goodreads&search_type=quotes&tab=quotes "
)


@lru_cache(maxsize=20)
@cachier(cache_dir=Path("..", "tmp").absolute())
def _search_quotes_page(search_term, page):
    url = quote_search_url.format(page, search_term.replace(" ", "+"))
    try:
        page = requests.get(url, timeout=5)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
        return None
    if page:
        soup = BeautifulSoup(page.content, "html.parser")
        # Replace breaks with new lines
        for br in soup.find_all("br"):
            br.replace_with("\n")

        # Extract the right text parts
        quote_elements = soup.find_all("div", class_="quoteText")
        quotes = [
            " ".join([part.strip() for part in quote.get_text().split("—")][0:-1])
            for quote in quote_elements
        ]

        return quotes


search_quotes = scraper_util.create_page_scraper(_search_quotes_page)
