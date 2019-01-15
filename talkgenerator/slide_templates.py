""" This module helps creating specific type of slides using our template powerpoint using python-pptx """
from talkgenerator.util import generator_util

from talkgenerator.slide import powerpoint_slide_creator


# GENERATORS: Same as the template fillers above, but using generation functions

def generate_full_image_slide(title_generator, image_generator, original_image_size=True):
    return generate_slide(powerpoint_slide_creator.create_full_image_slide,
                          (title_generator, image_generator, lambda x: original_image_size))


def generate_image_slide(title_generator, image_generator, original_image_size=True):
    return generate_slide(powerpoint_slide_creator.create_image_slide,
                          (title_generator, image_generator, lambda x: original_image_size))


def generate_image_slide_tuple(tuple_generator, original_image_size=True):
    def generate(presentation_context, used):
        generated_tuple = tuple_generator(presentation_context)
        generated = generated_tuple[0], generated_tuple[1], original_image_size

        return _generate_if_different_enough(powerpoint_slide_creator.create_image_slide, presentation_context,
                                             generated, used)

    return generate


def generate_title_slide(title_generator, subtitle_generator):
    return generate_slide(powerpoint_slide_creator.create_title_slide, (title_generator, subtitle_generator))


def generate_large_quote_slide(title_generator, text_generator,
                               background_image_generator=generator_util.none_generator):
    return generate_slide(powerpoint_slide_creator.create_large_quote_slide,
                          (title_generator, text_generator, background_image_generator))


def generate_two_column_images_slide(title_generator, caption_1_generator, image_1_generator, caption_2_generator,
                                     image_2_generator):
    return generate_slide(powerpoint_slide_creator.create_two_column_images_slide,
                          (title_generator, caption_1_generator,
                           image_1_generator, caption_2_generator,
                           image_2_generator))


def generate_two_column_images_slide_tuple(title_generator, tuple_1_generator, tuple_2_generator):
    def generate(presentation_context, used):
        generated_tuple_1 = tuple_1_generator(presentation_context)
        generated_tuple_2 = tuple_2_generator(presentation_context)
        generated = title_generator(presentation_context), generated_tuple_1[0], generated_tuple_1[1], \
                    generated_tuple_2[0], generated_tuple_2[1]

        return _generate_if_different_enough(powerpoint_slide_creator.create_two_column_images_slide,
                                             presentation_context, generated, used)

    return generate


def generate_two_column_images_slide_tuple_caption(title_generator, captions_generator, image_1_generator,
                                                   image_2_generator):
    def generate(presentation_context, used):
        generated_tuple = captions_generator(presentation_context)
        generated = title_generator(presentation_context), generated_tuple[0], image_1_generator(
            presentation_context), generated_tuple[1], image_2_generator(presentation_context)
        return _generate_if_different_enough(powerpoint_slide_creator.create_two_column_images_slide,
                                             presentation_context, generated, used)

    return generate


def generate_three_column_images_slide(title_generator, caption_1_generator, image_1_generator, caption_2_generator,
                                       image_2_generator, caption_3_generator, image_3_generator):
    return generate_slide(powerpoint_slide_creator.create_three_column_images_slide,
                          (title_generator, caption_1_generator,
                           image_1_generator, caption_2_generator,
                           image_2_generator, caption_3_generator,
                           image_3_generator))


def generate_three_column_images_slide_tuple(title_generator, tuple_1_generator, tuple_2_generator, tuple_3_generator):
    def generate(presentation_context, used):
        generated_tuple_1 = tuple_1_generator(presentation_context)
        generated_tuple_2 = tuple_2_generator(presentation_context)
        generated_tuple_3 = tuple_3_generator(presentation_context)
        generated = title_generator(presentation_context), generated_tuple_1[0], generated_tuple_1[1], \
                    generated_tuple_2[0], generated_tuple_2[1], \
                    generated_tuple_3[0], generated_tuple_3[1]

        return _generate_if_different_enough(powerpoint_slide_creator.create_three_column_images_slide,
                                             presentation_context, generated, used)

    return generate


def generate_three_column_images_slide_tuple_caption(title_generator, captions_generator, image_1_generator,
                                                     image_2_generator, image_3_generator):
    def generate(presentation_context, used):
        generated_tuple = captions_generator(presentation_context)
        generated = title_generator(presentation_context), generated_tuple[0], image_1_generator(
            presentation_context), generated_tuple[1], image_2_generator(presentation_context), \
                    generated_tuple[2], image_3_generator(presentation_context)
        return _generate_if_different_enough(powerpoint_slide_creator.create_three_column_images_slide,
                                             presentation_context, generated, used)

    return generate


def generate_chart_slide(title_generator, chart_generator):
    return generate_slide(powerpoint_slide_creator.create_chart_slide, (title_generator, chart_generator))


def generate_chart_slide_tuple(chart_generator):
    def generate(presentation_context, used):
        return _generate_if_different_enough(powerpoint_slide_creator.create_chart_slide, presentation_context,
                                             chart_generator(presentation_context), used)

    return generate


# HELPERS

def generate_slide(slide_template, generators):
    def generate(presentation_context, used):
        generated = [content_generator(presentation_context) if content_generator else None for content_generator in
                     generators]
        return _generate_if_different_enough(slide_template, presentation_context, generated, used)

    return generate


def _generate_if_different_enough(slide_template, presentation_context, generated, used):
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


def create_new_powerpoint():
    return powerpoint_slide_creator.create_new_powerpoint()
