from run import *


def test_some_imports():
    assert bool(random)
    assert bool(slide_templates)
    assert bool(presentation_schema)


def test_get_definitions():
    definitions = get_definitions('dog')
    assert len(definitions) == 8


def test_get_synonyms():
    synonyms = get_synonyms('dog')
    assert len(synonyms) == 30
