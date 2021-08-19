"""
Light, commonly used, non-specific generators that are helpful shortcuts for creating
certain types of (content) generators
"""
import os
import sys
import random
import logging
import inspect
from typing import Callable, Optional, Dict, Union, Tuple

import requests

from talkgenerator.datastructures.image_data import ImageData
from talkgenerator.util import random_util, os_util

logger = logging.getLogger("talkgenerator")


def fullname(o):
  # o.__module__ + "." + o.__class__.__qualname__ is an example in
  # this context of H.L. Mencken's "neat, plausible, and wrong."
  # Python makes no guarantees as to whether the __module__ special
  # attribute is defined, so we take a more circumspect approach.
  # Alas, the module name is explicitly excluded from __qualname__
  # in Python 3.

  module = o.__class__.__module__
  if module is None or module == str.__class__.__module__:
    return o.__class__.__name__  # Avoid reporting __builtin__
  else:
    return module + '.' + o.__class__.__name__


class Generator(object):
    def __call__(self, seed: str):
        raise NotImplemented(
            str(self) + " has not provided an implementation for the generator"
        )


class PrefixedGenerator(Generator):
    def __init__(self, prefix: str, generator: Generator):
        self._prefix = prefix
        self._generator = generator

    def __call__(self, seed: str):
        return self._generator(self._prefix + " " + seed)


class PrefixedPresentationContextGenerator(Generator):
    def __init__(self, prefix: str, generator):
        self._prefix = prefix
        self._generator = generator

    def __call__(self, presentation_context):
        presentation_context = dict(presentation_context)
        presentation_context["seed"] = self._prefix + " " + presentation_context["seed"]
        return self._generator(presentation_context)


class CombinedGenerator(Generator):
    def __init__(self, *weighted_generators: Tuple[Union[int, float], Generator]):
        self._weighted_generators = weighted_generators

    def __call__(self, seed: Union[str, Dict[str, str]]):
        logger.debug('Calling generator_util.CombinedGenerator')
        current_weighted_generators = list(self._weighted_generators)
        logger.debug("current_weighted_generators: {}".format(current_weighted_generators))
        while len(current_weighted_generators) > 0:
            generator = random_util.weighted_random(current_weighted_generators)
            logger.debug("current generator: {}".format(generator))
            logger.debug("generator seed: {}".format(seed))
            generated = generator(seed)
            logger.debug("generated: {}".format(generated))
            if generated is not None:
                return generated
            _remove_object_from_weighted_list(current_weighted_generators, generator)


def _remove_object_from_weighted_list(current_weighted_generators, generator):
    for i in current_weighted_generators:
        if i and i[1] == generator:
            current_weighted_generators.remove(i)


class MappedGenerator(Generator):
    def __init__(self, generator, *functions):
        self._generator = generator
        self._functions = functions

    def __call__(self, presentation_context):
        # print("MappedGenerator generator using", presentation_context)
        generated = self._generator(presentation_context)
        for func in self._functions:
            generated = func(generated)
        return generated


class TupledGenerator(Generator):
    """ Creates a tuple generator that generates every tuple value independent from the others"""

    def __init__(self, *generators):
        self._generators = generators

    def __call__(self, presentation_context):
        # print("TupledGenerator generator using", presentation_context)
        return tuple(
            [generator(presentation_context) for generator in self._generators]
        )


class InspiredTupleGenerator(Generator):
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


class SeededGenerator(Generator):
    def __init__(self, simple_generator):
        self._simple_generator = simple_generator

    def __call__(self, presentation_context):
        logger.debug('Calling generator_util.SeededGenerator')
        logger.debug('presentation_context: {}'.format(presentation_context))
        logger.debug('self._simple_generator: {}'.format(self._simple_generator))
        return self._simple_generator(presentation_context["seed"])


class UnseededGenerator(Generator):
    def __init__(self, simple_generator):
        self._simple_generator = simple_generator

    def __call__(self, seed):
        presentation_context = {"seed": seed}
        return self._simple_generator(presentation_context)


class NoneGenerator(Generator):
    def __init__(self):
        pass

    def __call__(self, presentation_context):
        return None


class IdentityGenerator(Generator):
    def __init__(self, input_word):
        self._input_word = input_word

    def __call__(self, presentation_context):
        return self._input_word


class TitledIdentityGenerator(Generator):
    def __init__(self, input_word):
        self._input_word = input_word

    def __call__(self, presentation_context):
        if self._input_word:
            return self._input_word.title()


class StaticGenerator(Generator):
    def __init__(self, always_generate_this):
        self._always_generate_this = always_generate_this

    def __call__(self, presentation_context=None):
        return self._always_generate_this


class FromListGenerator(Generator):
    def __init__(self, list_generator):
        self._list_generator = list_generator

    def __call__(self, presentation_context):
        return random_util.choice_optional(self._list_generator(presentation_context))


seeded_identity_generator = SeededGenerator(IdentityGenerator)
seeded_titled_identity_generator = SeededGenerator(TitledIdentityGenerator)


class ExternalImageListGenerator(Generator):
    def __init__(
        self, image_generator, check_image_validness=True, weighted=False,
    ):
        self._image_generator = image_generator
        self._check_image_validness = check_image_validness
        self._weighted = weighted

    def __call__(self, presentation_context) -> Optional[ImageData]:
        logger.debug('Calling generator_util.ExternalImageListGenerator')
        logger.debug('self._image_generator: {}'.format(self._image_generator))
        logger.debug('self._check_image_validness: {}'.format(self._check_image_validness))
        logger.debug('self._weighted: {}'.format(self._weighted))
        logger.debug('module where function def: {}'.format(self._image_generator.__module__))
        logger.debug('****************************************************************')
        images = self._image_generator(presentation_context)
        # logger.debug('images: {}'.format(images))
        logger.debug('****************************************************************')

        while bool(images) and len(images) > 0:
            original_chosen_image = (
                random_util.weighted_random([image for image in images if image[0] > 0])
                if self._weighted
                else random.choice(images)
            )
            if isinstance(original_chosen_image, str):
                chosen_image = ImageData(image_url=original_chosen_image)
            elif isinstance(original_chosen_image, ImageData):
                chosen_image = original_chosen_image
            else:
                logger.warning(
                    "INVALID IMAGE INPUT FOR EXTERNAL IMAGE GENERATOR / "
                    + str(original_chosen_image)
                    + " / "
                    + str(type(original_chosen_image))
                )
                images.remove(original_chosen_image)
                continue

            return chosen_image
        return None


class BackupGenerator(Generator):
    def __init__(self, *generator_list):
        self._generator_list = generator_list

    def __call__(self, context):
        for generator in self._generator_list:
            generated = generator(context)
            if generated:
                return generated


class WeightedGenerator(Generator):
    def __init__(self, weighted_list_creator):
        self._weighted_list_creator = weighted_list_creator

    def __call__(self, argument):
        weighted_list = self._weighted_list_creator(argument)
        if weighted_list:
            return random_util.weighted_random(weighted_list)


class UnweightedGenerator(Generator):
    def __init__(self, weighted_list_creator):
        self._weighted_list_creator = weighted_list_creator

    def __call__(self, argument):
        weighted_list = self._weighted_list_creator(argument)
        if weighted_list:
            return random_util.choice_optional(
                [element[1] for element in weighted_list]
            )


class WalkingGenerator(Generator):
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


class ImageGenerator(Generator):
    def __call__(self, seed: str) -> ImageData:
        raise NotImplementedError("Not implemented image generator")


class UnsourcedImageGenerator(ImageGenerator):
    def __init__(self, image_url_generator: Callable[[str], str]):
        self._image_url_generator = image_url_generator

    def __call__(self, seed: str) -> ImageData:
        return ImageData(image_url=self._image_url_generator(seed))


class RelatedMappingGenerator(Generator):
    def __init__(
        self, related_word_generator: Callable[[str], str], generator: Generator
    ):
        self._related_word_generator = related_word_generator
        self._generator = generator

    def __call__(self, seed: str) -> Optional[str]:
        mapped_seed = self._related_word_generator(seed)
        return self._generator(mapped_seed)
