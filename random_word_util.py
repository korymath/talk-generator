from random_util import choice_optional
import nltk

WORDS = nltk.Text(nltk.corpus.wordnet.words()) # Get text from wordnet

def random_word():
    return choice_optional(WORDS)
