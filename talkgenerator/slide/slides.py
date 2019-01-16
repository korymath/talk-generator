from abc import ABCMeta, abstractmethod
from talkgenerator.slide import powerpoint_slide_creator


class Slide(metaclass=ABCMeta):
    """ Class representing a slide object that could be used to export to Powerpoint pptx or other representations later
    """

    # def __init__(self):
    #     pass

    @property
    @abstractmethod
    def ppt_slide_creator(self):
        """ The function converting it to powerpoint"""
        pass

    @property
    @abstractmethod
    def arguments(self):
        pass

    def create_powerpoint_slide(self, prs):
        """ Should generate a slide in the powerpoint """
        return self.ppt_slide_creator(prs, **self.arguments)


class TitleSlide(Slide):
    def __init__(self, title, subtitle):
        self._title = title
        self._subtitle = subtitle

    @property
    def ppt_slide_creator(self):
        return powerpoint_slide_creator.create_title_slide

    @property
    def arguments(self):
        return {
            'title': self._title,
            'subtitle': self._subtitle
        }
