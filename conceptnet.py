import pprint as pp
from urllib.parse import urlencode

import requests

URL = "http://api.conceptnet.io/c/en/{}?"

_LOCATION_ARGUMENTS = {
    "rel": "/r/AtLocation",
    "limit": 100
}
_HASA_ARGUMENTS = {
    "rel": "/r/HasA",
    "limit": 200
}
_DEFAULT_ARGUMENTS = {
    "limit": 200
}


# HELPERS
_PROHIBITED_SEARCH_TERMS = "a", "your", "my", "her", "his", "be"

def _get_data(word, arguments=None):
    if not arguments:
        arguments = _DEFAULT_ARGUMENTS
    splitted_word = [part for part in word.split(" ") if part not in _PROHIBITED_SEARCH_TERMS]
    search_term = "_".join(splitted_word)
    url = URL.format(search_term) + urlencode(arguments, False, "/")
    return requests.get(url).json()


def _get_edges(word, arguments=None):
    return _get_data(word, arguments)["edges"]


def _get_weight_and_word(edge, word):
    end_label = edge["end"]["label"]
    if not end_label == word:
        return edge["weight"], end_label


def _get_relation_label(edge):
    return edge["rel"]["label"]


def _get_from_relation(word, edges, relation_name):
    return [_get_weight_and_word(edge, word) for edge in edges if _get_relation_label(edge) == relation_name]


# EXTRACTING INFO

def get_weighted_words(word, limit=50):
    edges = _get_edges(word, {"limit": limit})
    return [edge["end"]["label"] for edge in edges if edge["end"]["label"] != word]


def get_weighted_related_locations(word):
    edges = _get_edges(word, _LOCATION_ARGUMENTS)
    return _get_from_relation(word, edges, "AtLocation")


def get_weighted_has(word):
    edges = _get_edges(word, _HASA_ARGUMENTS)
    return _get_from_relation(word, edges, "HasA")


def get_weighted_properties(word):
    edges = _get_edges(word)
    return _get_from_relation(word, edges, "HasProperty")


def get_weighted_antonyms(word):
    edges = _get_edges(word)
    return _get_from_relation(word, edges, "Antonym")


pp.pprint(get_weighted_words("cat", 45))
