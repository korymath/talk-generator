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


def titled_identity_generator(input_word):
    if input_word:
        return input_word.title()


def create_static_generator(always_generate_this):
    return lambda _: always_generate_this


def create_none_generator():
    return lambda _: None


seeded_identity_generator = create_seeded_generator(identity_generator)
seeded_titled_identity_generator = create_seeded_generator(titled_identity_generator)


def create_from_list_generator(list_generator):
    return lambda inp: random_util.choice_optional(list_generator(inp))


def remove_invalid_images_from_generator(list_generator):
    return lambda inp: [item for item in list_generator(inp) if os_util.is_image(item) and os_util.is_valid_image(item)]


def create_from_external_image_list_generator(image_url_generator, file_name_generator):
    def generate_from_image_list(presentation_context):
        images = image_url_generator(presentation_context)
        while bool(images) and len(images) > 0:
            chosen_image_url = random.choice(images)
            downloaded_url = file_name_generator(chosen_image_url)
            try:
                if os_util.is_image(chosen_image_url):
                    os_util.download_image(chosen_image_url, downloaded_url)
                    if os_util.is_valid_image(downloaded_url):
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


def combined_generator(*weighted_generators):
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


def apply_function_to_generator(generator, *functions):
    def generate(presentation_context):
        generated = generator(presentation_context)
        for func in functions:
            generated = func(generated)
        return generated

    return generate


def create_tupled_generator(*generators):
    """ Creates a tuple generator that generates every tuple value independent from the others"""
    return lambda x: tuple([generator(x) for generator in generators])


def create_inspired_tuple_generator(generator_1, generator_2):
    """ The second generator will get the generator 1 as input, outputting the tuple """

    def generate_tuple(presentation_context):
        gen_1 = generator_1(presentation_context)
        gen_2 = generator_2(gen_1)
        return gen_1, gen_2

    return generate_tuple


def create_weighted_generator(weighted_list_creator):
    def generate(argument):
        weighted_list = weighted_list_creator(argument)
        if weighted_list:
            return random_util.weighted_random(weighted_list)

    return generate


def create_walking_generator(inner_generator, steps):
    """ This type of generator uses its output as input for a next step, taking concepts a few steps away """

    def generate(seed):
        history = set()
        history.add(seed)
        current = seed
        for i in range(steps):
            generated = inner_generator(current)
            if generated:
                current = generated
                history.add(current)
                print(i, current)

        return current

    return generate
