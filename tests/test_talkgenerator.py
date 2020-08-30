import random
import logging
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
        self.default_args.configure_mock(parallel=True)
        self.default_args.configure_mock(
            output_folder=os_util.to_actual_file("../output/test/")
        )
        self.default_args.configure_mock(open_ppt=False)
        self.default_args.configure_mock(save_ppt=True)
        self.default_args.configure_mock(int_seed=123)

    def test_serial(self):
        self.default_args.configure_mock(parallel=False)
        ppt, _, _ = generator.generate_presentation_using_cli_arguments(
            self.default_args
        )

        self.assertEqual(3, len(ppt.slides))

    def test_to_dictionary(self):
        _, slide_deck, _ = generator.generate_presentation(
            schema="default",
            slides=3,
            topic="cat",
            title=None,
            presenter=None,
            parallel=True,
            int_seed=123,
            save_ppt=False,
            open_ppt=False,
            print_logs=False,
        )
        slides_dict = slide_deck.to_slide_deck_dictionary()
        logging.info(slides_dict)
        self.assertIsNotNone(slides_dict)

    def test_all_slide_generators(self):
        basic_presentation_context = {
            "topic": "dog",
            "seed": "cat",
            "presenter": "An O. Nymous",
            "title": "Mock title",
        }

        presentation = powerpoint_slide_creator.create_new_powerpoint()

        for slide_generator in slide_schemas.all_slide_generators:
            logging.info("Testing Slide Generator: {}".format(slide_generator))
            random.seed(123)
            slide, _ = slide_generator.generate(
                basic_presentation_context, []
            )
            slide.create_powerpoint_slide(presentation)


if __name__ == "__main__":
    unittest.main()
