# -*- coding: utf-8 -*-
"""NLTK downloading with SSL handling
"""

import ssl
import nltk


try:
    _create_unverified_https_context = ssl._create_unverified_context  # pylint: disable=protected-access
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context  # pylint: disable=protected-access


if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')
    nltk.download('pros_cons')
    nltk.download('reuters')
