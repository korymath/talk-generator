from random import randint


# Classes that are abstractly responsible for generating powerpoints

class SlideGenerator:
    """ Responsible for providing the slide generator and other attributes, such as its name and weight"""

    @staticmethod
    def constant_weight(weight: int):
        """Class function to create a function that always returns a certain weight"""
        return lambda slide_nr, total_slides: weight

    def __init__(self, generator, weight_function=constant_weight(1), name=None):
        self._generator = generator
        self._weight_function = weight_function
        self._name = name

    def generate(self, presentation, seed):
        """Generate a slide for a given presentation using the given seed."""
        slide = self._generator(presentation, seed)
        # Add information about the generator to the notes
        if slide:
            slide.notes_slide.notes_text_frame.text = str(self) + " / " + seed
        return slide

    #
    def get_weight_for(self, slide_nr, total_slides):
        """The weight of the generator for a particular slide.
        Determines how much chance it has being picked for a particular slide number"""
        return self._weight_function(slide_nr, total_slides)

    def __str__(self):
        name = str(self._generator.__name__)
        if name == '<lambda>':
            name = str(self._name)
        return "SlideGenerator[" + name + "]"


class PresentationSchema:
    """ Class responsible for determining which slide generators to use in a presentation, and how the (topic) seed for
    each slide is generated """

    def __init__(self, powerpoint_creator, seed_generator, slide_generators):
        self._powerpoint_creator = powerpoint_creator
        self._seed_generator = seed_generator
        self._slide_generators = slide_generators

    def generate_presentation(self, topic, num_slides):
        """Generate a presentation about a certain topic with a certain number of slides"""
        # Create new presentation
        presentation = self._powerpoint_creator()
        # Create the topic-for-each-slide generator
        seed_generator = self._seed_generator(topic, num_slides)

        for slide_nr in range(num_slides):
            self._generate_slide(presentation, seed_generator, slide_nr, num_slides, set())

        return presentation

    def _generate_slide(self, presentation, seed_generator, slide_nr, num_slides, prohibited_generators=set()):

        # Generate a topic for the next slide
        seed = seed_generator.generate_seed(slide_nr)

        # Select the slide generator to generate with
        generator = self._select_generator(slide_nr, num_slides, prohibited_generators)

        print('Generating slide {} about {} using {}'.format(slide_nr + 1, seed, generator))
        slide = generator.generate(presentation, seed)

        # Try again if slide is None, and prohibit generator for generating for this topic
        if not bool(slide):
            prohibited_generators.add(generator)

            return self._generate_slide(presentation, seed_generator, slide_nr, num_slides, prohibited_generators)
            # TODO: Remove slide from presentation if there was a slide generated

        return slide

    def _select_generator(self, slide_nr, total_slides, prohibited_generators):
        """Select a generator for a certain slide number"""
        weighted_generators = []
        for i in range(len(self._slide_generators)):
            generator = self._slide_generators[i]
            if generator in prohibited_generators:
                continue
            weighted_generator = generator.get_weight_for(slide_nr, total_slides), generator
            weighted_generators.append(weighted_generator)
        return weighted_random(weighted_generators)


# Helper functions

# From https://stackoverflow.com/questions/14992521/python-weighted-random
def weighted_random(pairs):
    if len(pairs) == 0:
        raise ValueError("Pairs can't be zero")
    total = sum(pair[0] for pair in pairs)
    r = randint(1, total)
    for (weight, value) in pairs:
        r -= weight
        if r <= 0:
            return value
