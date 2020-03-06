import unittest

from talkgenerator import pexels


class PexelsTest(unittest.TestCase):
    def test_pexels_access(self):
        image_urls = pexels.search_photos_return_urls("office")
        print(image_urls)
        self.assertTrue(len(image_urls) > 0)


if __name__ == "__main__":
    unittest.main()
