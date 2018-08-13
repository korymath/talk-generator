""" Module for interacting with Wikihow """
import re
from functools import lru_cache

import inflect
import requests
from bs4 import BeautifulSoup


def wikihow_action_to_action(wikihow_title):
    index_of_to = wikihow_title.find('to')
    action = wikihow_title[index_of_to + 3:]
    action = _remove_between_brackets(action)
    return action


def _remove_between_brackets(sentence):
    while True:
        s_new = re.sub(r'\([^\(]*?\)', r'', sentence)
        if s_new == sentence:
            break
        sentence = s_new
    return sentence


@lru_cache(maxsize=20)
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
                filter(lambda x: not x.startswith("Category"),
                       map(lambda x: x.get_text(), actions_elements))))

    return actions
