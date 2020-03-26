import unittest

from talkgenerator.schema.content_generator_structures import RedditImageSearcher


class RedditTest(unittest.TestCase):
    def test_reddit_simple(self):
        images = RedditImageSearcher("memes")("cat")
        self.assertTrue(len(images) > 0)
        sources = [
            image.get_source() for image in images if image.get_source() is not None
        ]
        self.assertTrue(len(sources) > 0)


if __name__ == "__main__":
    unittest.main()
