import unittest

from talkgenerator.schema.slide_topic_generators import SideTrackingTopicGenerator
from talkgenerator.sources import conceptnet


class ConceptNetTest(unittest.TestCase):
    def test_conceptnet_standard(self):
        related_words = conceptnet.get_weighted_related_words('cat', 10)
        self.assertTrue(len(related_words) is 10)

    def test_conceptnet_multiword(self):
        related_words = conceptnet.get_weighted_related_words('my lap', 10)
        self.assertTrue(len(related_words) > 0)


if __name__ == '__main__':
    unittest.main()
