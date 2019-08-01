import unittest

from talkgenerator.sources import phrasefinder


class PhraseFinderTest(unittest.TestCase):

    def test_phrasefinder_absolute_frequency(self):
        result = phrasefinder.get_absolute_frequency('cat')
        self.assertTrue(result == 7506109)


if __name__ == '__main__':
    unittest.main()
