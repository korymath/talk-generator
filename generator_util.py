
# == TRIVIAL GENERATORS ==

def seeded_generator(simple_generator):
    return lambda presentation_context: simple_generator(presentation_context["seed"])


def none_generator(_):
    return None


def identity_generator(input_word):
    return input_word


def create_static_generator(always_generate_this):
    return lambda _: always_generate_this


def create_none_generator():
    return lambda _: None


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


seeded_identity_generator = seeded_generator(identity_generator)
