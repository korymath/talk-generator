import random
import unittest
from unittest import mock

from talkgenerator.schema import slide_schemas
from talkgenerator import generator
from talkgenerator.slide import powerpoint_slide_creator
from talkgenerator.util import os_util


class TestTalkGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(1)
        self.default_args = mock.Mock()
        self.default_args.configure_mock(topic="cat")
        self.default_args.configure_mock(num_slides=3)
        self.default_args.configure_mock(schema="default")
        self.default_args.configure_mock(title=None)
        self.default_args.configure_mock(parallel=False)
        self.default_args.configure_mock(
            output_folder=os_util.to_actual_file("../output/test/")
        )
        self.default_args.configure_mock(open_ppt=False)
        self.default_args.configure_mock(save_ppt=True)
        self.default_args.configure_mock(int_seed=123)

    def test_multiple_topics(self):
        self.default_args.configure_mock(topic="cat, dog, bread, house")
        self.default_args.configure_mock(num_slides=6)
        ppt, _, _ = generator.generate_presentation_using_cli_arguments(
            self.default_args
        )
        self.assertEqual(6, len(ppt.slides))


if __name__ == "__main__":
    unittest.main()


