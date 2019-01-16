from abc import ABCMeta, abstractmethod


class SlideGenerator(metaclass=ABCMeta):
    """ Generating Slide objects using a list of generators """

    def __init__(self, content_providers):
        """ The given content_providers is a function that when called,
        generates all of the arguments for the slide creator"""
        self._content_providers = content_providers

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

    def generate_slide(self, prs):
        """ Generates the slide using the given generators """

        # def generate(presentation_context, used):
        #     generated = [content_generator(presentation_context) if content_generator else None for content_generator in
        #                  generators]
        #     return _generate_if_different_enough(slide_template, presentation_context, generated, used)
        #
        # return generate
        # return self.slide_type(prs, **self._arguments)

# HELPERS

def generate_slide(slide_template, generators):
    def generate(presentation_context, used):
        generated = [content_generator(presentation_context) if content_generator else None for content_generator in
                     generators]
        return generate_if_different_enough(slide_template, presentation_context, generated, used)

    return generate


def generate_if_different_enough(slide_template, presentation_context, generated, used):
    if _is_different_enough(generated, used):
        return slide_template(get_presentation(presentation_context), *generated), generated


def get_presentation(presentation_context):
    return presentation_context["presentation"]


def _is_different_enough(generated, used):
    if generated:
        (used_elements, allowed_repeated_elements) = used
        intersection = set(generated) & used_elements
        return allowed_repeated_elements >= len(intersection)
    return False


