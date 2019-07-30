import unittest

from talkgenerator.schema.slide_topic_generators import SideTrackingTopicGenerator


class SlideTopicGeneratorsTest(unittest.TestCase):
    def test_conceptnet_sidetracking_standard(self):
        generator = SideTrackingTopicGenerator('cat', 10)
        self.assertTrue(len([seed for seed in generator.all_seeds() if seed is None]) is 0)

    def test_conceptnet_sidetracking_non_existing_topic(self):
        generator = SideTrackingTopicGenerator('nonexistingword-bla-bla', 10)
        self.assertTrue(len([seed for seed in generator.all_seeds() if seed is None]) is 0)

    def test_conceptnet_sidetracking_hard_topic(self):
        generator = SideTrackingTopicGenerator('scratch_furniture', 10)
        print(generator.all_seeds())
        self.assertTrue(len([seed for seed in generator.all_seeds() if seed is None]) is 0)


if __name__ == '__main__':
    unittest.main()
