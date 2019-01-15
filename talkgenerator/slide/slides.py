from abc import ABCMeta, abstractmethod
from talkgenerator.slide import powerpoint_slide_creator


class Slide(metaclass=ABCMeta):
    """ Class representing a slide object that could be used to export to Powerpoint pptx or other representations later
    """

    # def __init__(self):
    #     pass

    @property
    @abstractmethod
    def slide_type(self):
        pass

    @abstractmethod
    def create_powerpoint_slide(self, prs):
        """ Should generate a slide in the powerpoint """
        pass


class TitleSlide(Slide):
    def __init__(self, title, subtitle):
        self._title = title
        self._subtitle = subtitle

    def slide_type(self):
        return powerpoint_slide_creator.LAYOUT_TITLE_SLIDE

    def create_powerpoint_slide(self, prs):
        return powerpoint_slide_creator.create_title_slide(prs, self._title, self._subtitle)
