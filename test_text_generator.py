import unittest
import text_generator

class TextGeneratorTest(unittest.TestCase):

    def test_variable_extraction(self):
        self.assertEqual(["test", "adjective"],
                         text_generator.get_format_variables("this {test} is going {adjective}"))
        self.assertEqual(["test"], text_generator.get_format_variables("this {test} is testing for {} empty"))
        self.assertEqual([], text_generator.get_format_variables("this test only has {} some {} empty names"))

    def test_not_using_unusable_template(self):
        """ Tests if the generator is not raising an error when variables are missing to generate, and only uses other
        generator """
        possible_templates = ["This is {adjective}", "This is {noun}"]
        templated_text_generator = text_generator.TemplatedTextGenerator(templates_list=possible_templates)
        for _ in range(100):
            self.assertEqual("This is possible", templated_text_generator.generate({"adjective": "possible"}));
        for _ in range(100):
            self.assertEqual("This is a test", templated_text_generator.generate({"noun": "a test"}));

    def test_all_possible_outcomes(self):
        possible_templates = ["This is {adjective}", "This is {noun}"]
        templated_text_generator = text_generator.TemplatedTextGenerator(templates_list=possible_templates)
        expected = {"This is possible", "This is a test"}
        all_generations = set()
        for _ in range(10000):
            if all_generations == expected:
                break
            all_generations.add(templated_text_generator.generate({"adjective": "possible", "noun": "a test"}))

        self.assertEqual(expected, all_generations)


if __name__ == '__main__':
    unittest.main()
