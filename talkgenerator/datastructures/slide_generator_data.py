from functools import lru_cache


# WEIGHT FUNCTIONS
# def create_peaked_weight(peak_values, weight, other_weight):
#     def weight_function(slide_nr, num_slides):
#         actual_peak_values = fix_indices(peak_values, num_slides)
#         if slide_nr in actual_peak_values:
#             return weight
#         return other_weight
#
#     return weight_function
from typing import Collection, Union, Set, Callable, Tuple

from talkgenerator.datastructures.image_data import ImageData


class PeakedWeight(object):
    def __init__(
        self, peak_values: Tuple[int, ...], weight: float, other_weight: float
    ):
        self._peak_values = peak_values
        self._weight = weight
        self._other_weight = other_weight

    def __call__(self, slide_nr: int, num_slides: int):
        actual_peak_values = fix_indices(self._peak_values, num_slides)
        if slide_nr in actual_peak_values:
            return self._weight
        return self._other_weight


@lru_cache(maxsize=30)
def fix_indices(values: Collection[int], num_slides: int):
    return [value % num_slides if value < 0 else value for value in values]


class ConstantWeightFunction(object):
    def __init__(self, weight):
        self._weight = weight

    def __call__(self, slide_nr, total_slides):
        return self._weight


# Classes that are abstractly responsible for generating powerpoints


class SlideGeneratorData:
    """ Responsible for providing the slide generator and other attributes, such as its name and weight"""

    def __init__(
        self,
        generator,
        weight_function: Callable[[int, int], float] = ConstantWeightFunction(1),
        retries: int = 5,
        allowed_repeated_elements: int = 0,
        tags=None,
        name=None,
    ):
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
            slide_results = self._generator.generate_slide(
                presentation_context, (used_elements, self._allowed_repeated_elements)
            )
            if slide_results:
                (slide, generated_elements) = slide_results

                # If the generated content is nothing, don't try again
                if _has_not_generated_something(generated_elements):
                    return None

                if slide:
                    # Add notes about the generation
                    slide.set_note(
                        "Seed: "
                        + presentation_context["seed"]
                        + "\nGenerator: "
                        + str(self)
                        + " \n Context: "
                        + str(presentation_context)
                        + " \n Generated Elements: "
                        + str(generated_elements)
                    )

                    # Add all sources of generated elements
                    for generated_element in generated_elements:
                        if isinstance(generated_element, ImageData):
                            slide.add_source(generated_element.get_source())

                    return slide, generated_elements

    def get_weight_for(self, slide_nr: int, total_slides: int) -> float:
        """The weight of the generator for a particular slide.
        Determines how much chance it has being picked for a particular slide number"""
        return self._weight_function(slide_nr, total_slides)

    def get_allowed_repeated_elements(self) -> int:
        return self._allowed_repeated_elements

    def get_tags(self) -> Set[str]:
        return self._tags

    def __str__(self):
        if bool(self._name):
            return str(self._name)
        name = str(self._generator.__name__)
        if name == "<lambda>":
            name = "Unnamed Generator"
        return "SlideGenerator[" + name + "]"


def _has_not_generated_something(generated_elements) -> bool:
    generated_elements = set(generated_elements)
    _filter_generated_elements(generated_elements)
    return len(generated_elements) == 0


def _filter_generated_elements(generated_elements: Set[Union[str, bool, None]]):
    if "" in generated_elements:
        generated_elements.remove("")
    if None in generated_elements:
        generated_elements.remove(None)
    if True in generated_elements:
        generated_elements.remove(True)
    if False in generated_elements:
        generated_elements.remove(False)
