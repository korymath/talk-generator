import logging
from abc import ABCMeta, abstractmethod
from random import random

from talkgenerator.slide import powerpoint_slide_creator

logger = logging.getLogger("talkgenerator")


class Slide(metaclass=ABCMeta):
    """ Class representing a slide object that could be used to export to Powerpoint pptx or other representations later
    """

    def __init__(self, arguments):
        self._arguments = arguments
        self._note = ""
        self._sources = []

    def add_source(self, source: str):
        if source is not None:
            self._sources.append(source)

    def set_note(self, note: str):
        self._note = note

    @property
    @abstractmethod
    def ppt_slide_creator(self):
        """ The function converting it to powerpoint"""
        pass

    def create_powerpoint_slide(self, prs):
        """ Should generate a slide in the powerpoint """
        ppt_slide = self.ppt_slide_creator(prs, **self._arguments)
        try:
            if ppt_slide:
                ppt_slide.notes_slide.notes_text_frame.text = self._note

                if len(self._sources):
                    powerpoint_slide_creator.add_sources_note(ppt_slide, self._sources)

        except AttributeError as e:
            logger.error("attribute error on create slide {}".format(e))
        return ppt_slide


class TitleSlide(Slide):
    def __init__(self, title, subtitle):
        super().__init__({"title": title, "subtitle": subtitle})

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_title_slide


class LarqeQuoteSlide(Slide):
    def __init__(self, title, text, background_image=None):
        super().__init__(
            {"title": title, "text": text, "background_image": background_image}
        )

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_large_quote_slide


class ImageSlide(Slide):
    def __init__(self, title=None, image_url=None, original_image_size=True):
        super().__init__(
            {
                "title": title,
                "image_url": image_url,
                "original_image_size": original_image_size,
            }
        )

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_image_slide


class FullImageSlide(Slide):
    def __init__(self, title=None, image_url=None, original_image_size=True):
        super().__init__(
            {
                "title": title,
                "image_url": image_url,
                "original_image_size": original_image_size,
            }
        )

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_full_image_slide


class TwoColumnImageSlide(Slide):
    def __init__(
        self,
        title=None,
        caption_1=None,
        image_or_text_1=None,
        caption_2=None,
        image_or_text_2=None,
        original_image_size=True,
    ):
        super().__init__(
            {
                "title": title,
                "caption_1": caption_1,
                "image_or_text_1": image_or_text_1,
                "caption_2": caption_2,
                "image_or_text_2": image_or_text_2,
                "original_image_size": original_image_size,
            }
        )

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_two_column_images_slide


class ThreeColumnImageSlide(Slide):
    def __init__(
        self,
        title=None,
        caption_1=None,
        image_or_text_1=None,
        caption_2=None,
        image_or_text_2=None,
        caption_3=None,
        image_or_text_3=None,
        original_image_size=True,
    ):
        super().__init__(
            {
                "title": title,
                "caption_1": caption_1,
                "image_or_text_1": image_or_text_1,
                "caption_2": caption_2,
                "image_or_text_2": image_or_text_2,
                "caption_3": caption_3,
                "image_or_text_3": image_or_text_3,
                "original_image_size": original_image_size,
            }
        )

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_three_column_images_slide


class ChartSlide(Slide):
    def __init__(self, title, chart_type, chart_data, chart_modifier=None):
        super().__init__(
            {
                "title": title,
                "chart_type": chart_type,
                "chart_data": chart_data,
                "chart_modifier": chart_modifier,
            }
        )

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_chart_slide
