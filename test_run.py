import unittest

from run import *


class TestStringMethods(unittest.TestCase):

    def test_some_imports(self):
        self.assertTrue(bool(random))
        self.assertTrue(bool(slide_templates))
        self.assertTrue(bool(presentation_schema))


if __name__ == '__main__':
    unittest.main()
