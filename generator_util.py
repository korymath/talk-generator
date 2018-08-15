import random

import requests

import os_util
import random_util


# == TRIVIAL GENERATORS ==

def create_seeded_generator(simple_generator):
    return lambda presentation_context: simple_generator(presentation_context["seed"])


def none_generator(_):
    return None


def identity_generator(input_word):
    return input_word


def create_static_generator(always_generate_this):
    return lambda _: always_generate_this


def create_none_generator():
    return lambda _: None


def create_from_list_generator(list_generator):
    return lambda input: random_util.choice_optional(list_generator(input))


def create_from_external_image_list_generator(image_url_generator, file_name_generator):
    def generate_from_image_list(presentation_context):
        images = image_url_generator(presentation_context)
        while len(images) > 0:
            chosen_image_url = random.choice(images)
            downloaded_url = file_name_generator(chosen_image_url)
            try:
                os_util.download_image(chosen_image_url, downloaded_url)
                return downloaded_url
            except PermissionError:
                print("Permission error when downloading", chosen_image_url)
            except requests.exceptions.MissingSchema:
                print("Missing schema for image ", chosen_image_url)
            except OSError:
                print("Non existing image for: ", chosen_image_url)
            images.remove(chosen_image_url)
        return None

    return generate_from_image_list


def create_backup_generator(*generator_list):
    def generate(context):
        for generator in generator_list:
            generated = generator(context)
            if generated:
                return generated

    return generate


def combined_generator(weighted_generators):
    def generate(seed):
        current_weighted_generators = list(weighted_generators)
        while len(current_weighted_generators) > 0:
            generator = random_util.weighted_random(current_weighted_generators)
            generated = generator(seed)
            if generated is not None:
                return generated
            _remove_object_from_weighted_list(current_weighted_generators, generator)

    return generate


def _remove_object_from_weighted_list(current_weighted_generators, generator):
    for i in current_weighted_generators:
        if i and i[1] == generator:
            current_weighted_generators.remove(i)


seeded_identity_generator = create_seeded_generator(identity_generator)
