import unittest
from talkgenerator.sources import unsplash

class MyTestCase(unittest.TestCase):

    def test_unsplash_access(self):
        image_urls = unsplash.search_photos_return_urls('office')
        print(len(image_urls))
        self.assertTrue(len(image_urls) > 0)


if __name__ == '__main__':
    unittest.main()
