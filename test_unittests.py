import unittest

import text_generator
import wikihow
from run import *


class TestStringMethods(unittest.TestCase):

    def test_some_imports(self):
        self.assertTrue(bool(random))
        self.assertTrue(bool(slide_templates))
        self.assertTrue(bool(presentation_schema))


    def test_wrong_wikihow_links_regression_test(self):
        actions = wikihow.get_related_wikihow_actions("cat")
        self.assertFalse("articles from wikiHow" in actions)


if __name__ == '__main__':
    unittest.main()
