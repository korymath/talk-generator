from run import *


def test_imports():
    assert INCHES_TO_EMU == 914400


def test_get_definitions():
    definitions = get_definitions('dog')
    assert len(definitions) == 8


def test_get_synonyms():
    synonyms = get_synonyms('dog')
    assert len(synonyms) == 30
