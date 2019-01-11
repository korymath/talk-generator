import unittest
from talk_generator import wikihow


class MyTestCase(unittest.TestCase):

    def test_wrong_wikihow_links_regression_test(self):
        actions = wikihow.get_related_wikihow_actions_basic_search("cat")
        self.assertFalse("articles from wikiHow" in actions)


if __name__ == '__main__':
    unittest.main()
