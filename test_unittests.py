from run import *
import text_generator
import wikihow


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


def test_not_using_unusable_template():
    """ Tests if the generator is not raising an error when variables are missing to generate, and only uses other
    generator """
    possible_templates = ["This is {adjective}", "This is {noun}"]
    templated_text_generator = text_generator.TemplatedTextGenerator(templates_list=possible_templates)
    for _ in range(100):
        assert "This is possible" == templated_text_generator.generate({"adjective": "possible"});
    for _ in range(100):
        assert "This is a test" == templated_text_generator.generate({"noun": "a test"});


def test_all_possible_outcomes():
    possible_templates = ["This is {adjective}", "This is {noun}"]
    templated_text_generator = text_generator.TemplatedTextGenerator(templates_list=possible_templates)
    expected = {"This is possible", "This is a test"}
    all_generations = set()
    for _ in range(10000):
        if all_generations == expected:
            break
        all_generations.add(templated_text_generator.generate({"adjective": "possible", "noun": "a test"}))

    assert expected == all_generations


def test_wrong_wikihow_links_regression_test():
    actions = wikihow.get_related_wikihow_actions("cat")
    assert not "articles from wikiHow" in actions


test_some_imports()
test_get_definitions()
test_get_synonyms()
test_variable_extraction()
test_not_using_unusable_template()
test_all_possible_outcomes()
test_wrong_wikihow_links_regression_test()
