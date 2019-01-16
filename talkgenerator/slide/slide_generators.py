from abc import ABCMeta, abstractmethod


class SlideGenerator(metaclass=ABCMeta):
    """ Generating Slide objects using a list of generators """

    def __init__(self, slide_content_generator):
        """ The given content_providers is a function that when called,
        generates all of the arguments for the slide creator"""
        self._slide_content_generator = slide_content_generator

    @property
    @abstractmethod
    def slide_type(self):
        """ The function converting it to a Slide object """
        pass

    @classmethod
    def of(cls, *generators):
        return cls(
            lambda presentation_context: [content_generator(presentation_context)
                                          if content_generator
                                          else None
                                          for content_generator in generators])

    def generate_slide(self, presentation_context, used):
        """ Generates the slide using the given generators """
        generated = self._slide_content_generator(presentation_context)
        if is_different_enough(generated, used):
            return self.slide_type(*generated), generated


# HELPERS


def is_different_enough(generated, used):
    if generated:
        (used_elements, allowed_repeated_elements) = used
        intersection = set(generated) & used_elements
        return allowed_repeated_elements >= len(intersection)
    return False
