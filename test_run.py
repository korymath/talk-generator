import unittest

from run import *


class TestStringMethods(unittest.TestCase):

    def test_some_imports(self):
        self.assertTrue(bool(random))
        self.assertTrue(bool(slide_templates))
        self.assertTrue(bool(presentation_schema))

    def test_google_images(self):
        self.assertTrue(bool(get_related_google_image({"seed": "cat"})))


if __name__ == '__main__':
    unittest.main()
