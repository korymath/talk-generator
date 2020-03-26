import time
import logging
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlencode

import requests
from cachier import cachier

from talkgenerator.util import generator_util, cache_util

URL = "http://api.conceptnet.io/c/en/{}?"

_LOCATION_ARGUMENTS = cache_util.HashableDict(rel="/r/AtLocation", limit=100)
_HASA_ARGUMENTS = cache_util.HashableDict(rel="/r/HasA", limit=200)
_DEFAULT_ARGUMENTS = cache_util.HashableDict(limit=200)

# HELPERS
_PROHIBITED_SEARCH_TERMS = (
    "a",
    "your",
    "my",
    "her",
    "his",
    "its",
    "their",
    "be",
    "an",
    "the",
    "you",
    "are",
)

logger = logging.getLogger("talkgenerator.conceptnet")


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
@cachier(cache_dir=Path("..", "tmp").absolute())
def _get_data(word, arguments=None):
    if not arguments:
        arguments = _DEFAULT_ARGUMENTS
    splitted_word = _remove_prohibited_words(word)
    search_term = "_".join(splitted_word)
    url = URL.format(search_term) + urlencode(arguments, False, "/")
    start = time.perf_counter()
    try:
        result = requests.get(url).json()
    except Exception as e:
        logger.warning("conceptnet _get_data timeout: {}".format(e))
        result = None
    end = time.perf_counter()
    logger.info(
        "Took {} seconds to poll Conceptnet for '{}'".format(str(end - start), word)
    )
    return result


def _get_edges(word, arguments=None):
    data = _get_data(word, arguments)
    if data:
        return data["edges"]


def _get_weight_and_word(edge, word):
    end_label = edge["end"]["label"]
    if not end_label == word:
        return edge["weight"], end_label


def _get_relation_label(edge):
    return edge["rel"]["label"]


def _get_from_relation(word, edges, relation_name):
    return remove_nones(
        [
            _get_weight_and_word(edge, word)
            for edge in edges
            if _get_relation_label(edge) == relation_name
        ]
    )


# EXTRACTING INFO


def is_english(node):
    return node and (not "language" in node or node["language"] == "en")


def is_different_enough_label(edge, word):
    label = edge["label"].lower()
    word_lower = word.lower()
    return not label in word_lower and not word_lower in label


def get_weighted_related_words(word, limit=50):
    edges = _get_edges(word, cache_util.HashableDict(limit=limit))
    starts = [
        (edge["weight"], edge["start"]["label"])
        for edge in edges
        if is_different_enough_label(edge["start"], word) and is_english(edge["start"])
    ]
    ends = [
        (edge["weight"], edge["end"]["label"])
        for edge in edges
        if is_different_enough_label(edge["end"], word) and is_english(edge["end"])
    ]
    result = starts + ends
    return result


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


# Weighted
weighted_location_generator = generator_util.WeightedGenerator(
    get_weighted_related_locations
)
weighted_antonym_generator = generator_util.WeightedGenerator(get_weighted_antonyms)
weighted_related_word_generator = generator_util.WeightedGenerator(
    get_weighted_related_words
)

# Unweighted
unweighted_location_generator = generator_util.UnweightedGenerator(
    get_weighted_related_locations
)
unweighted_antonym_generator = generator_util.UnweightedGenerator(get_weighted_antonyms)
unweighted_related_word_generator = generator_util.UnweightedGenerator(
    get_weighted_related_words
)
