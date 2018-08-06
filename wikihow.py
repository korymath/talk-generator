""" Module for interacting with Wikihow """
import inflect
import requests
from bs4 import BeautifulSoup

def wikihow_action_to_action(wikihow_title):
    index_of_to = wikihow_title.find('to')
    return wikihow_title[index_of_to + 3:]


def search_wikihow(search_words):
    return requests.get(
        'https://en.wikihow.com/wikiHowTo?search='
        + search_words.replace(' ', '+'))


def get_related_wikihow_actions(seed_word):
    page = search_wikihow(seed_word)
    # Try again but with plural if nothing is found
    if not page:
        page = search_wikihow(inflect.engine().plural(seed_word))

    soup = BeautifulSoup(page.content, 'html.parser')
    actions_elements = soup.find_all('a', class_='result_link')
    actions = \
        list(
            map(wikihow_action_to_action,
                map(lambda x: x.get_text(), actions_elements)))

    return actions
