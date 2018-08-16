import unittest
from unittest import mock
import random

import run


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        random.seed(1)

    def test_google_images(self):
        self.assertTrue(bool(run.generate_full_screen_google_image({"seed": "cat"})))

    def test_main(self):
        arguments = mock.Mock()
        arguments.configure_mock(topic='cat')
        arguments.configure_mock(num_slides=10)
        arguments.configure_mock(schema='default')
        arguments.configure_mock(output_folder="./test_output/")
        arguments.configure_mock(open_ppt=False)
        arguments.configure_mock(save_ppt=True)
        ppt = run.main(arguments)

        self.assertEqual(10, len(ppt.slides))


if __name__ == '__main__':
    unittest.main()
