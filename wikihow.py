""" Module for interacting with Wikihow """
import json
import re
from functools import lru_cache

import inflect
import requests
from bs4 import BeautifulSoup

_LOG_IN_URL = "https://www.wikihow.com/index.php?title=Special:UserLogin&action=submitlogin&type=login"
_ADVANCED_SEARCH_URL = "https://www.wikihow.com/index.php?title=Special%3ASearch&profile=default&search={}" \
                       "&fulltext=Search&ss=relevance&so=desc&ffriy=1&ffrin=1&fft=ffta&fftsi=&profile=default"
_SESSION_COOKIE_NAME = "wiki_shared_session"


def log_in(username, password):
    log_in_credentials={"wpName": username, "wpPassword": password}
    res = requests.post(_LOG_IN_URL, None, log_in_credentials)
    log_in_cookie = res.cookies[_SESSION_COOKIE_NAME]

    return log_in_cookie


def get_wikihow_session():
    try:
        wikihow_credentials = json.load(open("./data/auth/wikihow.json"))
        if "session" in wikihow_credentials.keys():
            print("Found Wikihow Session object in credentials, skipping loggin in")
            return wikihow_credentials["session"]
        return log_in(**wikihow_credentials)
    except FileNotFoundError:
        print(
            "Warning: No login credentials were found for Wikihow, the program might not run as it's supposed to."
            "Please add these credentials file to /data/auth/wikihow.json, having a 'username' and 'password' field")


wikihow_session = get_wikihow_session()


def wikihow_action_to_action(wikihow_title):
    index_of_to = wikihow_title.find('to')
    action = wikihow_title[index_of_to + 3:]
    action = _remove_between_brackets(action)
    action = _remove_trademarks(action)
    return action


def _remove_between_brackets(sentence):
    while True:
        s_new = re.sub(r'\([^(]*?\)', r'', sentence)
        if s_new == sentence:
            break
        sentence = s_new
    return sentence


def _remove_trademarks(action):
    if " - wikihow.com" in action:
        return re.sub(" - wikihow.com", "", action)
    return action


@lru_cache(maxsize=20)
def basic_search_wikihow(search_words):
    return requests.get(
        'https://en.wikihow.com/wikiHowTo?search='
        + search_words.replace(' ', '+'))


def get_related_wikihow_actions_basic_search(seed_word):
    page = basic_search_wikihow(seed_word)
    # Try again but with plural if nothing is found
    if not page:
        page = basic_search_wikihow(inflect.engine().plural(seed_word))

    soup = BeautifulSoup(page.content, 'html.parser')
    actions_elements = soup.find_all('a', class_='result_link')
    actions = [wikihow_action_to_action(x.get_text()) for x in actions_elements if
                 x is not None and not x.get_text().startswith("Category")]

    return actions
