from run import *
import text_generator


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


def test_variable_extraction():
    assert ["test", "adjective"] == text_generator.get_format_variables("this {test} is going {adjective}")
    assert ["test"] == text_generator.get_format_variables("this {test} is testing for {} empty")
    assert [] == text_generator.get_format_variables("this test only has {} some {} empty names")


test_some_imports()
test_get_definitions()
test_get_synonyms()
test_variable_extraction()
