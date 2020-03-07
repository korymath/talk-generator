import unittest
from talkgenerator.sources import unsplash


class UnsplashTest(unittest.TestCase):
    def test_unsplash_access(self):
        images = unsplash.search_photos("office", ignore_cache=True)
        self.assertTrue(len(images) > 0)
        sources = [image.get_source() for image in images]
        self.assertTrue(len(sources) > 0)


if __name__ == "__main__":
    unittest.main()
