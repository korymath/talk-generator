import unittest

import goodreads


class GoodReadsTest(unittest.TestCase):
    def test_cat_search(self):
        cat_quotes = goodreads.search_quotes("cat", 5)
        # Check if starts with quote marks
        self.assertEqual('"', cat_quotes[0][0])


if __name__ == '__main__':
    unittest.main()
