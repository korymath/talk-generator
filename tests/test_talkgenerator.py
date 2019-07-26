import unittest
from unittest import mock
import random

from talkgenerator import utils
from talkgenerator.util import os_util
from talkgenerator.schema import schemas


class TestTalkGenerator(unittest.TestCase):

    def setUp(self):
        random.seed(1)

    def test_google_images(self):
        self.assertTrue(bool(schemas.generate_full_screen_google_image({"seed": "cat"})))

    def test_main(self):
        args = mock.Mock()
        args.configure_mock(topic='cat')
        args.configure_mock(num_slides=3)
        args.configure_mock(schema='test')
        args.configure_mock(parallel=False)
        args.configure_mock(output_folder=os_util.to_actual_file("output/test/"))
        args.configure_mock(open_ppt=False)
        args.configure_mock(save_ppt=True)
        ppt, slide_deck = utils.generate_talk(args)

        self.assertEqual(3, len(ppt.slides))

    def test_parallel(self):
        args = mock.Mock()
        args.configure_mock(topic='dog')
        args.configure_mock(num_slides=3)
        args.configure_mock(schema='test')
        args.configure_mock(parallel=True)
        args.configure_mock(output_folder=os_util.to_actual_file("output/test/"))
        args.configure_mock(open_ppt=False)
        args.configure_mock(save_ppt=True)
        ppt, slide_deck = utils.generate_talk(args)

        self.assertEqual(3, len(ppt.slides))


if __name__ == '__main__':
    unittest.main()
