"""
Light, commonly used, non-specific generators that are helpful shortcuts for creating
certain types of (content) generators
"""

import random

import requests

from talkgenerator.util import random_util, os_util


class CombinedGenerator(object):
    def __init__(self, *weighted_generators):
        self._weighted_generators = weighted_generators

    def __call__(self, seed):
        current_weighted_generators = list(self._weighted_generators)
        while len(current_weighted_generators) > 0:
            # print("combined generator using", current_weighted_generators)
            generator = random_util.weighted_random(current_weighted_generators)
            generated = generator(seed)
            if generated is not None:
                return generated
            _remove_object_from_weighted_list(current_weighted_generators, generator)


def _remove_object_from_weighted_list(current_weighted_generators, generator):
    for i in current_weighted_generators:
        if i and i[1] == generator:
            current_weighted_generators.remove(i)


class MappedGenerator(object):
    def __init__(self, generator, *functions):
        self._generator = generator
        self._functions = functions

    def __call__(self, presentation_context):
        # print("MappedGenerator generator using", presentation_context)
        generated = self._generator(presentation_context)
        for func in self._functions:
            generated = func(generated)
        return generated


class TupledGenerator(object):
    """ Creates a tuple generator that generates every tuple value independent from the others"""

    def __init__(self, *generators):
        self._generators = generators

    def __call__(self, presentation_context):
        # print("TupledGenerator generator using", presentation_context)
        return tuple([generator(presentation_context) for generator in self._generators])


class InspiredTupleGenerator(object):
    """ The second generator will get the generator 1 as input, outputting the tuple """

    def __init__(self, generator_1, generator_2):
        self._generator_1 = generator_1
        self._generator_2 = generator_2

    def __call__(self, presentation_context):
        # print("InspiredTupleGenerator generator using", presentation_context)
        gen_1 = self._generator_1(presentation_context)
        gen_2 = self._generator_2(gen_1)
        return gen_1, gen_2


# == TRIVIAL GENERATORS ==

class SeededGenerator(object):
    def __init__(self, simple_generator):
        self._simple_generator = simple_generator

    def __call__(self, presentation_context):
        return self._simple_generator(presentation_context["seed"])


class NoneGenerator(object):
    def __init__(self):
        pass

    def __call__(self, presentation_context):
        return None


class IdentityGenerator(object):
    def __init__(self, input_word):
        self._input_word = input_word

    def __call__(self, presentation_context):
        return self._input_word


class TitledIdentityGenerator(object):
    def __init__(self, input_word):
        self._input_word = input_word

    def __call__(self, presentation_context):
        if self._input_word:
            return self._input_word.title()


class StaticGenerator(object):
    def __init__(self, always_generate_this):
        self._always_generate_this = always_generate_this

    def __call__(self, presentation_context=None):
        return self._always_generate_this


class FromListGenerator(object):
    def __init__(self, list_generator):
        self._list_generator = list_generator

    def __call__(self, presentation_context):
        return random_util.choice_optional(self._list_generator(presentation_context))


class InvalidImagesRemoverGenerator(object):
    def __init__(self, list_generator):
        self._list_generator = list_generator

    def __call__(self, presentation_context):
        return [item for item in self._list_generator(presentation_context) if
                os_util.is_image(item) and os_util.is_valid_image(item)]


seeded_identity_generator = SeededGenerator(IdentityGenerator)
seeded_titled_identity_generator = SeededGenerator(TitledIdentityGenerator)


class ExternalImageListGenerator(object):
    def __init__(self, image_url_generator, file_name_generator, check_image_validness=True, weighted=False):
        self._image_url_generator = image_url_generator
        self._file_name_generator = file_name_generator
        self._check_image_validness = check_image_validness
        self._weighted = weighted

    def __call__(self, presentation_context):
        images = self._image_url_generator(presentation_context)
        while bool(images) and len(images) > 0:
            chosen_image_url = random_util.weighted_random(images) if self._weighted else random.choice(images)
            downloaded_url = self._file_name_generator(chosen_image_url)
            try:
                if not self._check_image_validness or os_util.is_image(chosen_image_url):
                    os_util.download_image(chosen_image_url, downloaded_url)
                    if os_util.is_valid_image(downloaded_url):
                        return downloaded_url
                else:
                    print("Not a image url", chosen_image_url)
            except PermissionError:
                print("Permission error when downloading", chosen_image_url)
            except requests.exceptions.MissingSchema:
                print("Missing schema for image ", chosen_image_url)
            except OSError:
                print("Non existing image for: ", chosen_image_url)
            images.remove(chosen_image_url)
        return None


class BackupGenerator(object):
    def __init__(self, *generator_list):
        self._generator_list = generator_list

    def __call__(self, context):
        for generator in self._generator_list:
            generated = generator(context)
            if generated:
                return generated


class WeightedGenerator(object):
    def __init__(self, weighted_list_creator):
        self._weighted_list_creator = weighted_list_creator

    def __call__(self, argument):
        weighted_list = self._weighted_list_creator(argument)
        if weighted_list:
            return random_util.weighted_random(weighted_list)


class UnweightedGenerator(object):
    def __init__(self, weighted_list_creator):
        self._weighted_list_creator = weighted_list_creator

    def __call__(self, argument):
        weighted_list = self._weighted_list_creator(argument)
        if weighted_list:
            return random_util.choice_optional([element[1] for element in weighted_list])


class WalkingGenerator(object):
    """ This type of generator uses its output as input for a next step, taking concepts a few steps away """

    def __init__(self, inner_generator, steps):
        self._inner_generator = inner_generator
        self._steps = steps

    def __call__(self, seed):
        history = set()
        history.add(seed)
        current = seed
        for i in range(self._steps):
            generated = self._inner_generator(current)
            if generated:
                current = generated
                history.add(current)

        return current
