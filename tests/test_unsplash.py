import unittest
from talkgenerator.sources import unsplash


class UnsplashTest(unittest.TestCase):

    def test_unsplash_access(self):
        image_urls = unsplash.search_photos_return_urls('office')
        self.assertTrue(len(image_urls) > 0)


if __name__ == '__main__':
    unittest.main()
