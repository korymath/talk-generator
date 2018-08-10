import unittest

import language_util


class LanguageUtilTest(unittest.TestCase):
    def test_get_definitions(self):
        definitions = language_util.get_definitions('dog')
        self.assertEqual(len(definitions), 8)

    def test_get_synonyms(self):
        synonyms = language_util.get_synonyms('dog')
        self.assertEqual(30, len(synonyms))

    def test_to_plural(self):
        self.assertEqual("cats", language_util.to_plural("cat"))
        self.assertEqual("cats", language_util.to_plural("cats"))

    def test_to_singular(self):
        self.assertEqual("cat", language_util.to_singular("cat"))
        self.assertEqual("cat", language_util.to_singular("cats"))


if __name__ == '__main__':
    unittest.main()
