from functools import lru_cache


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

class SlideGeneratorData:
    """ Responsible for providing the slide generator and other attributes, such as its name and weight"""

    def __init__(self, generator,
                 weight_function=constant_weight(1),
                 retries=5,
                 allowed_repeated_elements=0,
                 tags=None,
                 name=None):
        self._generator = generator
        self._weight_function = weight_function
        self._retries = retries
        self._name = name
        self._allowed_repeated_elements = allowed_repeated_elements
        if not tags:
            tags = set()
        self._tags = tags

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
                    slide.notes_slide.notes_text_frame.text = "Seed: " + presentation_context["seed"] \
                                                              + "\nGenerator: " \
                                                              + str(self) \
                                                              + " \n Context: " \
                                                              + str(presentation_context) \
                                                              + " \n Generated Elements: " \
                                                              + str(generated_elements)
                    return slide, generated_elements

    def get_weight_for(self, slide_nr, total_slides):
        """The weight of the generator for a particular slide.
        Determines how much chance it has being picked for a particular slide number"""
        return self._weight_function(slide_nr, total_slides)

    def get_tags(self):
        return self._tags

    def __str__(self):
        if bool(self._name):
            return str(self._name)
        name = str(self._generator.__name__)
        if name == '<lambda>':
            name = "Unnamed Generator"
        return "SlideGenerator[" + name + "]"


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
