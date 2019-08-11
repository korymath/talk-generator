import random
import unittest

from talkgenerator.schema.content_generator_structures import create_tracery_generator


class SpecificTextGeneratorTest(unittest.TestCase):
    def setUp(self):
        random.seed(1)

    def _tracery_tester(
        self, file_location, grammar_element="origin", print_generations=False
    ):
        number_of_generations = 100
        default_arguments = {
            "seed": "house",
            "presenter": "A. Nonymous",
            "topic": "house",
        }
        talk_title_generator = create_tracery_generator(file_location, grammar_element)
        generations = [
            talk_title_generator(default_arguments)
            for _ in range(0, number_of_generations)
        ]
        if print_generations:
            print("\n".join(generations))
        self.assertEqual(len(generations), number_of_generations)

    def test_talk_title_generator(self):
        self._tracery_tester("data/text-templates/talk_title.json")

    def test_talk_subtitle_generator(self):
        self._tracery_tester("data/text-templates/talk_subtitle.json", "job", True)


if __name__ == "__main__":
    unittest.main()
