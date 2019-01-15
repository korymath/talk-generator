from abc import ABCMeta, abstractmethod


class Slide(metaclass=ABCMeta):
    """ Class representing a slide object that could be used to export to Powerpoint pptx or other representations later
    """

    def __init__(self):
        # ...
        pass

    @property
    @abstractmethod
    def slide_type(self):
        pass

    @abstractmethod
    def create_powerpoint_slide(self, prs):
        """ Should generate a slide in the powerpoint """
        pass


