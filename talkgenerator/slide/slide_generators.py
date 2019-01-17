from abc import ABCMeta, abstractmethod
from talkgenerator.slide import slides


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
        return cls(combine_generators(*generators))

    def generate_slide(self, presentation_context, used) -> (slides.Slide, list):
        """ Generates the slide using the given generators """
        generated = self._slide_content_generator(presentation_context)
        if is_different_enough(generated, used):
            return self.slide_type(*generated), generated

    def generate_ppt_slide(self, presentation_context, used):
        # Temporary function: TODO remove me
        result = self.generate_slide(presentation_context, used)
        if result:
            return result[0].create_powerpoint_slide(presentation_context["presentation"]), result[1]


class TitleSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, subtitle_generator):
        return cls(combine_generators(title_generator, subtitle_generator))

    @property
    def slide_type(self):
        return slides.TitleSlide


class LarqeQuoteSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, text_generator, background_image_generator):
        return cls(combine_generators(title_generator, text_generator, background_image_generator))

    @property
    def slide_type(self):
        return slides.LarqeQuoteSlide


class ImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, image_generator=None, original_image_size=True):
        return cls(combine_generators(title_generator, image_generator, lambda void: original_image_size))

    @classmethod
    def of_tupled_captioned_image(cls, tuple_1_generator, original_image_size=True):
        def generate(presentation_context):
            generated_tuple_1 = tuple_1_generator(presentation_context)
            return generated_tuple_1[0], generated_tuple_1[1]

        return cls(generate)

    @property
    def slide_type(self):
        return slides.ImageSlide


class FullImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, image_generator=None, original_image_size=True):
        return cls(combine_generators(title_generator, image_generator, lambda void: original_image_size))

    @property
    def slide_type(self):
        return slides.FullImageSlide


class TwoColumnImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, caption_1_generator, image_or_text_1_generator, caption_2_generator,
           image_or_text_2_generator, original_image_size=True):
        return cls(
            combine_generators(title_generator, caption_1_generator, image_or_text_1_generator, caption_2_generator,
                               image_or_text_2_generator, lambda void: original_image_size))

    @classmethod
    def of_tupled_captioned_images(cls, title_generator, tuple_1_generator, tuple_2_generator,
                                   original_image_size=True):
        def generate(presentation_context):
            generated_tuple_1 = tuple_1_generator(presentation_context)
            generated_tuple_2 = tuple_2_generator(presentation_context)
            return title_generator(presentation_context), generated_tuple_1[0], generated_tuple_1[1], generated_tuple_2[
                0], generated_tuple_2[1], original_image_size

        return cls(generate)

    @classmethod
    def of_images_and_tupled_captions(cls, title_generator, captions_generator, image_1_generator,
                                      image_2_generator, original_image_size=True):
        def generate(presentation_context):
            generated_tuple = captions_generator(presentation_context)
            return title_generator(presentation_context), generated_tuple[0], image_1_generator(
                presentation_context), generated_tuple[1], image_2_generator(presentation_context), original_image_size

        return cls(generate)

    @property
    def slide_type(self):
        return slides.TwoColumnImageSlide


class ThreeColumnImageSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, caption_1_generator, image_or_text_1_generator, caption_2_generator,
           image_or_text_2_generator, caption_3_generator,
           image_or_text_3_generator, original_image_size=True):
        return cls(
            combine_generators(title_generator, caption_1_generator, image_or_text_1_generator, caption_2_generator,
                               image_or_text_2_generator, caption_3_generator,
                               image_or_text_3_generator, lambda void: original_image_size))

    @classmethod
    def of_tupled_captioned_images(cls, title_generator, tuple_1_generator, tuple_2_generator, tuple_3_generator,
                                   original_image_size=True):
        def generate(presentation_context):
            generated_tuple_1 = tuple_1_generator(presentation_context)
            generated_tuple_2 = tuple_2_generator(presentation_context)
            generated_tuple_3 = tuple_3_generator(presentation_context)
            return title_generator(presentation_context), generated_tuple_1[0], generated_tuple_1[1], generated_tuple_2[
                0], generated_tuple_2[1], generated_tuple_3[0], generated_tuple_3[1], original_image_size

        return cls(generate)

    @classmethod
    def of_images_and_tupled_captions(cls, title_generator, captions_generator, image_1_generator,
                                      image_2_generator, image_3_generator, original_image_size=True):
        def generate(presentation_context):
            generated_tuple = captions_generator(presentation_context)
            return title_generator(presentation_context), generated_tuple[0], image_1_generator(
                presentation_context), generated_tuple[1], image_2_generator(presentation_context), generated_tuple[
                       2], image_3_generator(presentation_context), original_image_size

        return cls(generate)

    @property
    def slide_type(self):
        return slides.ThreeColumnImageSlide


class ChartSlideGenerator(SlideGenerator):
    def __init__(self, slide_content_generator):
        super().__init__(slide_content_generator)

    @classmethod
    def of(cls, title_generator, chart_type_generator, chart_data_generator, chart_modifier=None):
        return cls(
            combine_generators(title_generator, chart_type_generator, chart_data_generator,
                               lambda void: chart_modifier))

    @property
    def slide_type(self):
        return slides.ChartSlide


# HELPERS
def combine_generators(*generators):
    return lambda presentation_context: [content_generator(presentation_context)
                                         if content_generator
                                         else None
                                         for content_generator in generators]


def is_different_enough(generated, used):
    if generated:
        (used_elements, allowed_repeated_elements) = used
        intersection = set(generated) & used_elements
        return allowed_repeated_elements >= len(intersection)
    return False
