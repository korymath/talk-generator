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


def create_log_in_session(username, password):
    log_in_credentials = {"wpName": username, "wpPassword": password}
    session = requests.session()
    session.post(_LOG_IN_URL, log_in_credentials, log_in_credentials)
    return session


def get_wikihow_session():
    try:
        wikihow_credentials = json.load(open("./data/auth/wikihow.json"))
        if "session" in wikihow_credentials.keys():
            print("Found Wikihow Session object in credentials, skipping loggin in")
            return wikihow_credentials["session"]
        return create_log_in_session(**wikihow_credentials)
    except FileNotFoundError:
        print(
            "Warning: No login credentials were found for Wikihow, the program might not run as it's supposed to."
            "Please add these credentials file to /data/auth/wikihow.json, having a 'username' and 'password' field")


wikihow_session = get_wikihow_session()


def remove_how_to(wikihow_title):
    index_of_to = wikihow_title.find('to')
    return wikihow_title[index_of_to + 3:]


def clean_wikihow_action(action):
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


@lru_cache(maxsize=20)
def advanced_search_wikihow(search_words):
    session = get_wikihow_session()
    if session:
        url = _ADVANCED_SEARCH_URL.format(search_words.replace(' ', '+'))
        resp = session.get(url, allow_redirects=True)
        if "Login Required - wikiHow" in str(resp.content):
            print("WARNING: Invalid log in on Wikihow!")
        return resp
    return None


def get_related_wikihow_actions_basic_search(seed_word):
    page = basic_search_wikihow(seed_word)
    # Try again but with plural if nothing is found
    if not page:
        page = basic_search_wikihow(inflect.engine().plural(seed_word))

    soup = BeautifulSoup(page.content, 'html.parser')
    actions_elements = soup.find_all('a', class_='result_link')
    actions = [clean_wikihow_action(remove_how_to(x.get_text())) for x in actions_elements if
               x is not None and not x.get_text().startswith("Category")]
    return actions


def get_related_wikihow_actions_advanced_search(seed_word):
    page = advanced_search_wikihow(seed_word)
    # Try again but with plural if nothing is found
    if not page:
        page = advanced_search_wikihow(inflect.engine().plural(seed_word))
    if page:
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup)
        actions_elements = soup.find_all('div', class_='mw-search-result-heading')
        actions = [clean_wikihow_action(x.find("a")["title"]) for x in actions_elements]
        return actions
    return []


def get_related_wikihow_actions(seed_word):
    """ Uses the advanced search unless it doesn't return anything """
    actions = get_related_wikihow_actions_advanced_search(seed_word)
    if actions:
        return actions
    return get_related_wikihow_actions_basic_search(seed_word)
