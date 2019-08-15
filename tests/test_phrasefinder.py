import unittest

from talkgenerator.sources import phrasefinder


class PhraseFinderTest(unittest.TestCase):
    def test_phrasefinder_absolute_frequency(self):
        self.assertEqual(7506109, phrasefinder.get_absolute_frequency("cat"))

    def test_phrasefinder_absolute_frequency_any_casing(self):
        self.assertEqual(
            10307263, phrasefinder.get_absolute_frequency_any_casing("cat")
        )

    def test_phrasefinder_rarest_word(self):
        self.assertEqual("cat", phrasefinder.get_rarest_word("Why I love my cat"))
        self.assertEqual(
            "Peace", phrasefinder.get_rarest_word("Peace is what I want most")
        )


if __name__ == "__main__":
    unittest.main()
