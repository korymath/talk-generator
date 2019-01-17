"""
This module represents the abstractions of a presentation schema (responsible for specifying how to generate a
presentation), and slide generators, that have functions for generating slides along with some other metadata.

"""

from talkgenerator.schema.slide_generator_data import _filter_generated_elements

from talkgenerator.util import random_util
from talkgenerator.slide.slide_deck import SlideDeck


class PresentationSchema:
    """ Class responsible for determining which slide generators to use in a presentation, and how the (topic) seed for
    each slide is generated """

    def __init__(self, powerpoint_creator, seed_generator, slide_generators, max_allowed_tags=None):
        self._powerpoint_creator = powerpoint_creator
        self._seed_generator = seed_generator
        self._slide_generators = slide_generators
        if max_allowed_tags is None:
            max_allowed_tags = {}
        self._max_allowed_tags = max_allowed_tags

    def generate_presentation(self, topic, num_slides, presenter=None):
        """Generate a presentation about a certain topic with a certain number of slides"""
        # Create new presentation
        presentation = self._powerpoint_creator()
        slide_deck = SlideDeck(num_slides)

        # Create the topic-for-each-slide generator
        seed_generator = self._seed_generator(topic, num_slides)

        # Create main presentation_context
        main_presentation_context = {
            "presentation": presentation,
            "topic": topic,
            "presenter": presenter
        }

        used_tags = {}

        used_elements = set()
        for slide_nr in range(num_slides):
            # TODO: This could possibly be done in parallel. There might be race conditions with the used_elements set,
            # and the order of slides must still happen in the same order, so the slide_nr should be passed as
            # argument to slide generator's content generator

            # Generate a topic for the next slide
            seed = seed_generator.generate_seed(slide_nr)

            prohibited_generators = self._calculate_prohibited_generators(used_tags, num_slides)

            # Generate the slide
            slide_results = self._generate_slide(
                presentation_context=create_slide_presentation_context(main_presentation_context, seed),
                slide_nr=slide_nr,
                num_slides=num_slides,
                used_elements=used_elements,
                prohibited_generators=prohibited_generators)
            if slide_results:
                # Add new generated content
                slide, generated_elements, slide_generator = slide_results

                slide_deck.add_slide(slide_nr, slide)

                # Add generated items to used_elements list
                generated_elements = set(generated_elements)
                _filter_generated_elements(generated_elements)
                used_elements.update(generated_elements)

                # Add generator tags to used_tags list
                add_tags(used_tags, slide_generator.get_tags())

        slide_deck.to_powerpoint(presentation)

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
            slide_result = generator.generate(presentation_context, used_elements)

            # Try again if slide is None, and prohibit generator for generating for this topic
            if not bool(slide_result):
                print("Failed to generated using:", generator)
                prohibited_generators.add(generator)

                return self._generate_slide(presentation_context=presentation_context,
                                            slide_nr=slide_nr,
                                            num_slides=num_slides,
                                            used_elements=used_elements,
                                            prohibited_generators=prohibited_generators)
                # TODO: Remove slide from presentation if there was a slide generated

            slide, generated_elements = slide_result

            return slide, generated_elements, generator
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

    def _calculate_prohibited_generators(self, used_tags, num_slides):
        prohibited_tags = set()
        for key, value in used_tags.items():
            if key in self._max_allowed_tags:
                max_tag = self._max_allowed_tags[key]

                # Assumes integer maximum
                max_number_of_slides = max_tag

                # If Procentua/Double ratio:
                if 0 < max_tag < 1:
                    max_number_of_slides = int(max_tag * num_slides)

                # Check if currently over the max allowed slides of this tag
                if value >= max_number_of_slides:
                    prohibited_tags.add(key)

        prohibited_generators = set()
        for generator in self._slide_generators:
            if set(generator.get_tags()) & prohibited_tags:
                prohibited_generators.add(generator)

        return prohibited_generators


# Helper functions
def create_slide_presentation_context(main_presentation_context, seed):
    presentation_context = dict(main_presentation_context)
    presentation_context["seed"] = seed
    return presentation_context


def add_tags(used_tags, tags):
    for tag in tags:
        if tag not in used_tags:
            used_tags[tag] = 1
        else:
            used_tags[tag] += 1
