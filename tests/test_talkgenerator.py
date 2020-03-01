import random
import unittest
from unittest import mock

from talkgenerator import utils
from talkgenerator.slide import powerpoint_slide_creator
from talkgenerator.util import os_util
from talkgenerator.schema import schemas


class TestTalkGenerator(unittest.TestCase):
    def setUp(self):
        random.seed(1)

    # def test_google_images(self):
    # """ Google image search is broken """
    # image = schemas.generate_full_screen_google_image({"seed": "cat"})
    # print(image)
    # self.assertTrue(
    #     bool(image)
    # )

    def test_serial(self):
        args = mock.Mock()
        args.configure_mock(topic="cat")
        args.configure_mock(num_slides=3)
        args.configure_mock(schema="default")
        args.configure_mock(title=None)
        args.configure_mock(parallel=False)
        args.configure_mock(output_folder=os_util.to_actual_file("output/test/"))
        args.configure_mock(open_ppt=False)
        args.configure_mock(save_ppt=True)
        ppt, slide_deck = utils.generate_talk(args)

        self.assertEqual(3, len(ppt.slides))

    def test_parallel(self):
        args = mock.Mock()
        args.configure_mock(topic="dog")
        args.configure_mock(num_slides=3)
        args.configure_mock(title=None)
        args.configure_mock(schema="default")
        args.configure_mock(parallel=True)
        args.configure_mock(output_folder=os_util.to_actual_file("output/test/"))
        args.configure_mock(open_ppt=False)
        args.configure_mock(save_ppt=True)
        ppt, slide_deck = utils.generate_talk(args)

        self.assertEqual(3, len(ppt.slides))

    def test_multiple_topics(self):
        args = mock.Mock()
        args.configure_mock(topic="cat, dog, bread, house")
        args.configure_mock(num_slides=6)
        args.configure_mock(title=None)
        args.configure_mock(schema="default")
        args.configure_mock(parallel=True)
        args.configure_mock(output_folder=os_util.to_actual_file("output/test/"))
        args.configure_mock(open_ppt=False)
        args.configure_mock(save_ppt=True)
        ppt, slide_deck = utils.generate_talk(args)

        self.assertEqual(6, len(ppt.slides))

    def test_all_slide_generators(self):
        basic_presentation_context = {
            "topic": "dog",
            "seed": "cat",
            "presenter": "An O. Nymous",
            "title": "Mock title",
        }

        presentation = powerpoint_slide_creator.create_new_powerpoint()

        for slide_generator in schemas.all_slide_generators:
            print("Testing Slide Generator", slide_generator)
            slide, generated_elements = slide_generator.generate(
                basic_presentation_context, []
            )
            slide.create_powerpoint_slide(presentation)


if __name__ == "__main__":
    unittest.main()
