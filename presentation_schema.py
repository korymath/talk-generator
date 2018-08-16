"""
This module represents the abstractions of a presentation schema (responsible for specifying how to generate a
presentation), and slide generators, that have functions for generating slides along with some other metadata.

"""

from functools import lru_cache

import random_util


# WEIGHT FUNCTIONS

def create_peaked_weight(peak_values, weight, other_weight):
    def weight_function(slide_nr, num_slides):
        actual_peak_values = fix_indices(peak_values, num_slides)
        if slide_nr in actual_peak_values:
            return weight
        return other_weight

    return weight_function


@lru_cache(maxsize=30)
def fix_indices(values, num_slides):
    return [value % num_slides if value < 0 else value for value in values]


def constant_weight(weight):
    """Class function to create a function that always returns a certain weight"""
    return lambda slide_nr, total_slides: weight


# Classes that are abstractly responsible for generating powerpoints

class SlideGenerator:
    """ Responsible for providing the slide generator and other attributes, such as its name and weight"""

    def __init__(self, generator, weight_function=constant_weight(1), retries=5, allowed_repeated_elements=0,
                 name=None):
        self._generator = generator
        self._weight_function = weight_function
        self._retries = retries
        self._name = name
        self._allowed_repeated_elements = allowed_repeated_elements

    def generate(self, presentation_context, used_elements):
        """Generate a slide for a given presentation using the given seed."""
        # Try a certain amount of times
        for i in range(self._retries):
            slide_results = self._generator(presentation_context, (used_elements, self._allowed_repeated_elements))
            if slide_results:
                (slide, generated_elements) = slide_results

                # If the generated content is nothing, don't try again
                if _has_not_generated_something(generated_elements):
                    return None

                if slide:
                    # Add notes about the generation
                    slide.notes_slide.notes_text_frame.text = str(self) + " / " + str(
                        presentation_context) + " / " + str(generated_elements)
                    return slide, generated_elements

    #
    def get_weight_for(self, slide_nr, total_slides):
        """The weight of the generator for a particular slide.
        Determines how much chance it has being picked for a particular slide number"""
        return self._weight_function(slide_nr, total_slides)

    def __str__(self):
        if bool(self._name):
            return str(self._name)
        name = str(self._generator.__name__)
        if name == '<lambda>':
            name = "Unnamed Generator"
        return "SlideGenerator[" + name + "]"


class PresentationSchema:
    """ Class responsible for determining which slide generators to use in a presentation, and how the (topic) seed for
    each slide is generated """

    def __init__(self, powerpoint_creator, seed_generator, slide_generators):
        self._powerpoint_creator = powerpoint_creator
        self._seed_generator = seed_generator
        self._slide_generators = slide_generators

    def generate_presentation(self, topic, num_slides, presenter=None):
        """Generate a presentation about a certain topic with a certain number of slides"""
        # Create new presentation
        presentation = self._powerpoint_creator()

        # Create the topic-for-each-slide generator
        seed_generator = self._seed_generator(topic, num_slides)

        # Create main presentation_context
        main_presentation_context = {
            "presentation": presentation,
            "topic": topic,
            "presenter": presenter
        }

        used_elements = set()
        for slide_nr in range(num_slides):
            # TODO: This can be done in parallel. There might be race conditions with the used_elements set,
            # and the order of slides must still happen in the same order, so the slide_nr should be passed as
            # argument to slide generator's content generator

            # Generate a topic for the next slide
            seed = seed_generator.generate_seed(slide_nr)

            # Generate the slide
            slide_results = self._generate_slide(
                create_slide_presentation_context(main_presentation_context, seed),
                slide_nr, num_slides, used_elements, set())
            if slide_results:
                # Add new generated content
                slide, generated_elements = slide_results
                generated_elements = set(generated_elements)
                _filter_generated_elements(generated_elements)
                used_elements.update(generated_elements)

        return presentation

    def _generate_slide(self, presentation_context, slide_nr, num_slides, used_elements=None,
                        prohibited_generators=None):

        # Default arguments: avoid mutable defaults
        if prohibited_generators is None:
            prohibited_generators = set()

        # Select the slide generator to generate with
        generator = self._select_generator(slide_nr, num_slides, prohibited_generators)

        if generator:
            print('\n * Generating slide {} about {} using {} *'.format(
                slide_nr + 1,
                presentation_context["seed"],
                generator))
            slide = generator.generate(presentation_context, used_elements)

            # Try again if slide is None, and prohibit generator for generating for this topic
            if not bool(slide):
                print("Failed to generated using:", generator)
                prohibited_generators.add(generator)

                return self._generate_slide(presentation_context=presentation_context,
                                            slide_nr=slide_nr,
                                            num_slides=num_slides,
                                            used_elements=used_elements,
                                            prohibited_generators=prohibited_generators)
                # TODO: Remove slide from presentation if there was a slide generated

            return slide
        else:
            print("No generator found to generate about ", presentation_context["Presentation"])

    def _select_generator(self, slide_nr, total_slides, prohibited_generators):
        """Select a generator for a certain slide number"""
        weighted_generators = []
        for i in range(len(self._slide_generators)):
            generator = self._slide_generators[i]
            if generator in prohibited_generators:
                continue
            weighted_generator = generator.get_weight_for(slide_nr, total_slides), generator
            weighted_generators.append(weighted_generator)

        if len(weighted_generators) == 0:
            raise ValueError("No generators left to generate slides with!")

        return random_util.weighted_random(weighted_generators)


# Helper functions
def create_slide_presentation_context(main_presentation_context, seed):
    presentation_context = dict(main_presentation_context)
    presentation_context["seed"] = seed
    return presentation_context


def _has_not_generated_something(generated_elements):
    generated_elements = set(generated_elements)
    _filter_generated_elements(generated_elements)
    return len(generated_elements) == 0


def _filter_generated_elements(generated_elements):
    if "" in generated_elements:
        generated_elements.remove("")
    if None in generated_elements:
        generated_elements.remove(None)
    if True in generated_elements:
        generated_elements.remove(True)
    if False in generated_elements:
        generated_elements.remove(False)
