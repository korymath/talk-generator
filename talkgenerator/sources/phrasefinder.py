import requests

URL = "https://api.phrasefinder.io/search?corpus=eng-us&query={}&nmax=1"


def _search(word):
    word.replace(' ', '%20')
    url = URL.format(word)
    result = requests.get(url).json()
    if result:
        return result['phrases']


def _get_absolute_frequencies(word):
    pf_results = _search(word)
    absolute_frequencies = []
    for word_count in pf_results:
        word = word_count['tks'][0]['tt']
        count = word_count['mc']
        absolute_frequencies.append((word, count))
    return absolute_frequencies


def get_absolute_frequency(word):
    absolute_frequencies = _get_absolute_frequencies(word)
    absolute_frequency = list(filter(lambda word_count: word_count[0] == word, absolute_frequencies))
    if len(absolute_frequency) == 1:
        return absolute_frequency[0][1]
