import unittest
from talkgenerator.sources import unsplash, pixabay


class PixabayTest(unittest.TestCase):
    def test_pixabay_access(self):
        image_urls = pixabay.search_photos_return_urls("office")
        print(image_urls)
        self.assertTrue(len(image_urls) > 0)


if __name__ == "__main__":
    unittest.main()
