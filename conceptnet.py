from urllib.parse import urlencode

import requests

URL = "http://api.conceptnet.io/c/en/{}?"

_RELATED_LOCATION_ARGUMENTS = {
    "rel": "/r/AtLocation",
    "limit": 100
}
_DEFAULT_ARGUMENTS = {
    "limit": 200
}


# HELPERS

def _get_data(word, arguments=None):
    if not arguments:
        arguments = _DEFAULT_ARGUMENTS
    url = URL.format(word) + urlencode(arguments, False, "/")
    return requests.get(url).json()


def _get_edges(word, arguments=None):
    return _get_data(word, arguments)["edges"]


def _get_weight_and_word(edge):
    return edge["weight"], edge["end"]["label"]


def _get_relation_label(edge):
    return edge["rel"]["label"]


# EXTRACTING INFO

def get_weighted_related_locations(word):
    edges = _get_edges(word, _RELATED_LOCATION_ARGUMENTS)
    locations = [_get_weight_and_word(edge) for edge in edges if _get_relation_label(edge) == "AtLocation"]
    return locations


print(get_weighted_related_locations("cat"))
