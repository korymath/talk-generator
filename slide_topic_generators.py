import math
import random

import numpy

import language_util


# == TOPIC GENERATORS ==

class IdentityTopicGenerator:
    """ Generates always the given topic as the seed for each slide """

    def __init__(self, topic, _):
        self._topic = topic

    def generate_seed(self, _):
        return self._topic


# TODO Other topic generators
'''=> We might need to think of a better way of finding topics for slides other than just plain synonyms. Usually, 
talks have some sort temporal linearity, building up to something, whereas currently in our system the order of the 
slide seeds doesn't matter. It might for example be interesting to try to make small loops around related concepts 
and try to come back to the main topic as seed every ~3 seeds, e.g. using Wikipedia links, conceptnet relations or 
other means, similar to the classic Harold impro format opener Cloverleaf. e.g. spaghetti -> Italy -> hills -> 
holidays -> restaurant -> spaghetti -> rasta hair -> reggea -> munchies -> spaghetti. Although this example might be 
a bit extreme varied, it will ensure that the talker just doesn't have to talk about this one topic and its synonyms, 
but can also deviate and make little stories. '''


class SynonymTopicGenerator:
    """ Generates a bunch of related words (e.g. synonyms) of a word to generate topics for a presentation"""

    def __init__(self, topic, number_of_slides):
        self._topic = topic
        self._slides_nr = number_of_slides
        synonyms = language_util.get_synonyms(topic)
        # seeds.extend(get_relations(topic))

        # Check if enough generated
        if len(synonyms) < number_of_slides:
            # If nothing: big problem!
            if len(synonyms) == 0:
                synonyms = [topic]

            # Now fill the seeds up with repeating topics
            number_of_repeats = int(math.ceil(number_of_slides / len(synonyms)))
            synonyms = numpy.tile(synonyms, number_of_repeats)

        # Take random `number_of_slides` elements
        random.shuffle(synonyms)
        self._seeds = synonyms[0: number_of_slides]

    def generate_seed(self, slide_nr):
        return self._seeds[slide_nr]
