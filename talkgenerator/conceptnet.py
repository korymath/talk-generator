from functools import lru_cache
from urllib.parse import urlencode

import requests

from talkgenerator import cache_util
from talkgenerator import generator_util
# import time

URL = "http://api.conceptnet.io/c/en/{}?"

_LOCATION_ARGUMENTS = cache_util.HashableDict(
    rel="/r/AtLocation",
    limit=100
)
_HASA_ARGUMENTS = cache_util.HashableDict(
    rel="/r/HasA",
    limit=200
)
_DEFAULT_ARGUMENTS = cache_util.HashableDict(
    limit=200
)

# HELPERS
_PROHIBITED_SEARCH_TERMS = "a", "your", "my", "her", "his", "its", "their", "be", "an", "the", "you", "are"


# Helpers
def _remove_prohibited_words(word):
    return [part for part in word.split(" ") if part not in _PROHIBITED_SEARCH_TERMS]


def normalise(word):
    return " ".join(_remove_prohibited_words(word)).lower()


def remove_duplicates(entries):
    if entries:
        checked = set()
        result = []
        for entry in entries:
            if entry:
                key = entry[1]
                if key in checked:
                    continue
                checked.add(key)
                result.append(entry)
        return result


def remove_containing(entries, prohibited_word):
    if entries:
        result = []
        for entry in entries:
            if entry:
                key = entry[1]
                if prohibited_word in key:
                    continue
                result.append(entry)
        return result


def remove_nones(entries):
    if entries:
        result = []
        for entry in entries:
            if entry:
                result.append(entry)
        return result
    return []


# RETRIEVING DATA

@lru_cache(maxsize=20)
def _get_data(word, arguments=None):
    if not arguments:
        arguments = _DEFAULT_ARGUMENTS
    splitted_word = _remove_prohibited_words(word)
    search_term = "_".join(splitted_word)
    url = URL.format(search_term) + urlencode(arguments, False, "/")
    # start = time.perf_counter()
    result = requests.get(url).json()
    # end = time.perf_counter()
    # print("Took {} seconds to poll conceptnet".format(str(end-start)))
    return result


def _get_edges(word, arguments=None):
    return _get_data(word, arguments)["edges"]


def _get_weight_and_word(edge, word):
    end_label = edge["end"]["label"]
    if not end_label == word:
        return edge["weight"], end_label


def _get_relation_label(edge):
    return edge["rel"]["label"]


def _get_from_relation(word, edges, relation_name):
    return remove_nones(
        [_get_weight_and_word(edge, word) for edge in edges if _get_relation_label(edge) == relation_name])


# EXTRACTING INFO

def get_weighted_related_words(word, limit=50):
    edges = _get_edges(word, cache_util.HashableDict(limit=limit))
    return [(edge["weight"], edge["end"]["label"]) for edge in edges if edge["end"]["label"] != word]


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


# pp.pprint(get_weighted_related_words("cat", 45))

# Weighted
weighted_location_generator = generator_util.create_weighted_generator(get_weighted_related_locations)
weighted_antonym_generator = generator_util.create_weighted_generator(get_weighted_antonyms)
weighted_related_word_generator = generator_util.create_weighted_generator(get_weighted_related_words)

# Unweighted
unweighted_location_generator = generator_util.create_unweighted_generator(get_weighted_related_locations)
unweighted_antonym_generator = generator_util.create_unweighted_generator(get_weighted_antonyms)
unweighted_related_word_generator = generator_util.create_unweighted_generator(get_weighted_related_words)
