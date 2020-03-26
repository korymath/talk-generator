from json import JSONDecodeError
from pathlib import Path

import requests
from cachier import cachier

from talkgenerator.util import language_util

URL = "https://api.phrasefinder.io/search?corpus=eng-us&query={}&nmax=1"


@cachier(cache_dir=Path("..", "tmp").absolute())
def _search(word):
    word.replace(" ", "%20")
    url = URL.format(word)
    try:
        result = requests.get(url)
        result = result.json()
        if result:
            return result["phrases"]
    except JSONDecodeError:
        return None


def _get_absolute_frequencies(word):
    pf_results = _search(word)
    if pf_results:
        absolute_frequencies = []
        for word_count in pf_results:
            word = word_count["tks"][0]["tt"]
            count = word_count["mc"]
            absolute_frequencies.append((word, count))
        return absolute_frequencies


def get_absolute_frequency(word):
    absolute_frequencies = _get_absolute_frequencies(word)
    absolute_frequency = list(
        filter(lambda word_count: word_count[0] == word, absolute_frequencies)
    )
    if len(absolute_frequency) == 1:
        return absolute_frequency[0][1]


def get_absolute_frequency_any_casing(word):
    absolute_frequencies = _get_absolute_frequencies(word)
    if absolute_frequencies:
        return sum(map(lambda word_count: word_count[1], absolute_frequencies))


def get_rarest_word(sentence):
    words = [
        language_util.replace_non_alphabetical_characters(word)
        for word in sentence.split(" ")
    ]
    words = filter(lambda word: word is not None and len(word.strip()) > 0, words)

    min_word = None
    min_freq = -1
    for word in words:
        freq = get_absolute_frequency_any_casing(word)
        if freq is not None and (min_freq == -1 or freq < min_freq):
            min_word = word
            min_freq = freq
    return min_word
    # return min(words, key=lambda word: get_absolute_frequency_any_casing(word))
