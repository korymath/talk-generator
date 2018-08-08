import unittest

import language_util


class LanguageUtilTest(unittest.TestCase):
    def test_get_definitions(self):
        definitions = language_util.get_definitions('dog')
        self.assertEqual(len(definitions), 8)

    def test_get_synonyms(self):
        synonyms = language_util.get_synonyms('dog')
        self.assertEqual(30, len(synonyms))


if __name__ == '__main__':
    unittest.main()
