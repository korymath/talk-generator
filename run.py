import pickle
import random
import pathlib
import os.path
import inflect
import argparse
import requests
import safygiphy
import math
import numpy
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import wordnet as wn
from py_thesaurus import Thesaurus
from google_images_download import google_images_download

# Own classes:
import slide_templates
import text_generator
from presentation_schema import PresentationSchema, SlideGenerator


class IdentityTopicGenerator:
    """ Generates always the given topic as the seed for each slide """

    def __init__(self, topic, _):
        self._topic = topic

    def generate_seed(self, _):
        return self._topic


class SynonymTopicGenerator:
    """ Generates a bunch of related words (e.g. synonyms) of a word to generate topics for a presentation"""

    def __init__(self, topic, number_of_slides):
        self._topic = topic
        self._slides_nr = number_of_slides
        synonyms = get_synonyms(topic)
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


# HELPER FUNCTIONS
def _save_presentation_to_pptx(topic, prs):
    """Save the talk."""
    fp = './output/' + topic + '.pptx'
    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(fp)).mkdir(parents=True, exist_ok=True)
    prs.save(fp)
    print('Saved talk to {}'.format(fp))
    return True


def download_image(from_url, to_url):
    """Download image from url to path."""
    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(to_url)).mkdir(parents=True, exist_ok=True)

    # Download
    f = open(to_url, 'wb')
    f.write(requests.get(from_url).content)
    f.close()


def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]


# CONTENT GENERATORS
# These functions generate content, sometimes related to given arguments

def get_definitions(word):
    """Get definitions of a given topic word."""
    print('******************************************')
    # Get definition
    word_senses = wn.synsets(word)
    definitions = {}
    for ss in word_senses:
        definitions[ss.name()] = ss.definition()
    print('{} definitions for "{}"'.format(len(definitions), word))
    return definitions


def get_synonyms(word):
    """Get all synonyms for a given word."""
    print('******************************************')
    word_senses = wn.synsets(word)
    all_synonyms = []
    for ss in word_senses:
        all_synonyms.extend(
            [x.lower().replace('_', ' ') for x in ss.lemma_names()])
    all_synonyms.append(word)
    all_synonyms = list(set(all_synonyms))
    # print('{} synonyms for "{}"'.format(len(all_synonyms), word))
    return all_synonyms


def get_relations(word):
    """Get relations to given definitions."""
    rels = {}
    all_rel_forms = []
    all_perts = []
    all_ants = []

    word_senses = wn.synsets(word)
    for ss in word_senses:
        ss_name = ss.name()
        rels[ss_name] = {}
        for lem in ss.lemmas():
            lem_name = lem.name()
            rels[ss_name][lem_name] = {}
            rel_forms = [x.name() for x in lem.derivationally_related_forms()]
            rels[ss_name][lem_name]['related_forms'] = rel_forms
            all_rel_forms.extend(rel_forms)

            perts = [x.name() for x in lem.pertainyms()]
            rels[ss_name][lem_name]['pertainyms'] = perts
            all_perts.extend(perts)

            ants = [x.name() for x in lem.antonyms()]
            rels[ss_name][lem_name]['antonyms'] = ants
            all_ants.extend(ants)

    print('******************************************')
    print('{} derivationally related forms'.format(len(all_rel_forms)))
    print('******************************************')
    print('{} pertainyms'.format(len(all_perts)))
    print('******************************************')
    print('{} antonyms'.format(len(all_ants)))
    return rels


def get_images(synonyms, num_images):
    """Get images, first search locally then Google Image Search."""
    all_paths = {}
    if num_images > 0:
        for word in synonyms:
            all_paths[word] = get_google_images(word, num_images)

    return all_paths


def get_google_images(word, num_images=1):
    lp = 'downloads/' + word + '/'
    paths = _get_google_image_cached(word, num_images, lp)

    # If no local images, search on Google Image Search
    if len(paths) == 0:
        # Get related images at 16x9 aspect ratio
        response = google_images_download.googleimagesdownload()
        arguments = {
            'keywords': word,
            'limit': num_images,
            'print_urls': True,
            'exact_size': '1600,900',
        }
        # passing the arguments to the function
        paths_dict = response.download(arguments)
        for value in paths_dict.values():
            paths.extend(value)

        # printing absolute paths of the downloaded images
        print('paths of images', paths)
    return paths


def _get_google_image_cached(word, num_image, lp):
    paths = []
    try:
        local_files = [lp + f for f in listdir(lp) if isfile(join(lp,
                                                                  f))]
        paths = local_files
    except FileNotFoundError:
        paths = []

    if len(paths) > 0:
        print('{} local images on {} found'.format(len(paths), word))

    if len(paths) > num_image:
        return paths


# GENERATORS
def generate_powerpoint_title(seed):
    """Returns a template title from a source list."""
    chosen_synonym_plural = inflect.engine().plural(seed)
    synonym_templates = read_lines('data/text-templates/titles.txt')
    chosen_template = random.choice(synonym_templates)
    return chosen_template.format(chosen_synonym_plural.title())


def get_related_giphy(seed_word):
    giphy = safygiphy.Giphy()
    response = giphy.random(tag=seed_word)
    if bool(response):
        data = response.get('data')
        if bool(data):
            images = data.get('images')
            original = images.get('original')
            giphy_url = original.get('url')
            gif_name = os.path.basename(os.path.dirname(giphy_url))
            image_url = 'downloads/' + seed_word + '/gifs/' + gif_name + ".gif"
            download_image(giphy_url, image_url)
            return image_url


def wikihow_action_to_action(wikihow_title):
    index_of_to = wikihow_title.find('to')
    return wikihow_title[index_of_to + 3:]


def search_wikihow(search_words):
    return requests.get(
        'https://en.wikihow.com/wikiHowTo?search='
        + search_words.replace(' ', '+'))


def get_related_wikihow_actions(seed_word):
    page = search_wikihow(seed_word)
    # Try again but with plural if nothing is found
    if not page:
        page = search_wikihow(inflect.engine().plural(seed_word))

    soup = BeautifulSoup(page.content, 'html.parser')
    actions_elements = soup.find_all('a', class_='result_link')
    actions = \
        list(
            map(wikihow_action_to_action,
                map(lambda x: x.get_text(), actions_elements)))

    return actions


def get_random_inspirobot_image(_):
    # Generate a random url to access inspirobot
    dd = str(random.randint(1, 73)).zfill(2)
    nnnn = random.randint(0, 9998)
    inspirobot_url = ('http://generated.inspirobot.me/'
                      '0{}/aXm{}xjU.jpg').format(dd, nnnn)

    # Download the image
    image_url = 'downloads/inspirobot/{}-{}.jpg'.format(dd, nnnn)
    download_image(inspirobot_url, image_url)

    return image_url


# FULL SLIDES GENERATORS:
# These are functions that create slides with certain (generated) content

def get_related_google_image(seed_word):
    # Get all image paths
    # img_paths = args.all_paths.get(word)
    img_paths = get_google_images(seed_word, 1)
    if img_paths:
        # Pick one of the images
        img_path = random.choice(img_paths)
        return img_path


bold_statement_templated_generator = text_generator.TemplatedTextGenerator('data/text-templates/bold-statements.txt')


def generate_wikihow_bold_statement(seed):
    related_actions = get_related_wikihow_actions(seed)
    # TODO: Sometimes "Articles Form Wikihow" is being scraped as an action, this is a bug
    if related_actions:
        action = random.choice(related_actions)
        template_values = {'action': action.title(),
                           # TODO: Make a scraper that scrapes a step related to this action on wikihow.
                           # TODO: Fix action_infinitive
                           'action_infinitive': action.title(),
                           'step': 'Do Whatever You Like',
                           'topic': seed,
                           # TODO: Use datamuse or conceptnet or some other mechanism of finding a related location
                           'location': 'Here'}
        life_lesson = bold_statement_templated_generator.generate(template_values)

        # Turn into image slide
        return life_lesson


# COMPILATION

def compile_talk_to_raw_data(arguments):
    """Save the raw data that has been harvested."""
    with open('output/' + arguments.topic.replace(' ', '_') + '.pkl', 'wb') as fh:
        pickle.dump(arguments, fh, protocol=pickle.HIGHEST_PROTOCOL)
        print('Pickle saved to output/' + arguments.topic.replace(' ', '_') + '.pkl')


# MAIN

def main(arguments):
    """Make a talk with the given topic."""
    # Print status details
    print('******************************************')
    print("Making {} slide talk on: {}".format(arguments.num_slides, arguments.topic))

    # Parse topic string to parts-of-speech
    # text = nltk.word_tokenize(args.topic)
    # print('******************************************')
    # print('tokenized text: ', text)
    # print('pos tag text: ', nltk.pos_tag(text))

    # Parse the actual topic subject from the parts-of-speech
    # topic_string = args.topic

    # Get definitions
    # args.definitions = get_definitions(topic_string)
    # Get relations
    # args.relations = get_relations(topic_string)
    # Get synonyms
    # args.synonyms = get_synonyms(topic_string)
    # Get related actions
    # args.actions = get_related_wikihow_actions(topic_string)
    # Get a title
    # args.title = generate_powerpoint_title(args.synonyms)
    # For each synonym download num_images
    # args.all_paths = get_images(args.synonyms, args.num_images)

    # Compile and save the presentation to data
    compile_talk_to_raw_data(arguments)

    # Compile and save the presentation to PPTX
    # compile_talk_to_pptx(args)
    schema = get_schema(args.schema)
    presentation = schema.generate_presentation(arguments.topic, arguments.num_slides)

    # Save presentation
    _save_presentation_to_pptx(arguments.topic, presentation)


def none_generator(_):
    return None


def identity_generator(input_word):
    return input_word


def create_static_image_generator(image):
    return lambda _: image


def create_double_image_captions(_):
    lines = read_lines("./data/text-templates/double-captions.txt")
    line = random.choice(lines)
    parts = line.split("|")
    return parts[0], parts[1]


# This object holds all the information about how to generate the presentation
presentation_schema = PresentationSchema(
    # Basic powerpoint generator
    slide_templates.create_new_powerpoint,
    # Topic per slide generator
    lambda topic, num_slides: SynonymTopicGenerator(topic, num_slides),

    # Slide generators
    [SlideGenerator(slide_templates.generate_title_slide(generate_powerpoint_title),
                    # Make title slides only happen as first slide
                    # TODO probably better to create cleaner way of forcing positional slides
                    weight_function=lambda slide_nr, total_slides:
                    100000 if slide_nr == 0 else 0,
                    name="Title slide"),
     SlideGenerator(slide_templates.generate_full_image_slide(identity_generator, get_related_giphy), name="Giphy"),
     SlideGenerator(slide_templates.generate_full_image_slide(none_generator, get_random_inspirobot_image),
                    name="Inspirobot"),
     SlideGenerator(slide_templates.generate_large_quote_slide(generate_wikihow_bold_statement),
                    name="Wikihow Bold Statement"),
     SlideGenerator(slide_templates.generate_full_image_slide(identity_generator, get_related_google_image),
                    name="Google Images"),
     SlideGenerator(
         slide_templates.generate_two_column_images_slide_tuple_caption(identity_generator,
                                                                        create_double_image_captions,
                                                                        get_related_giphy,
                                                                        get_related_giphy),
         name="Two Captions Giphy")
     ]
)

test_schema = PresentationSchema(
    # Basic powerpoint generator
    slide_templates.create_new_powerpoint,
    # Topic per slide generator
    lambda topic, num_slides: IdentityTopicGenerator(topic, num_slides),

    # Slide generators

    [
        SlideGenerator(slide_templates.generate_image_slide(none_generator, get_random_inspirobot_image),
                       name="Inspirobot"),
    ]
)

schemas = {
    "default": presentation_schema,
    "test": test_schema
}


def get_schema(name):
    return schemas[name]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', help="Topic of presentation.",
                        default='bagels', type=str)
    parser.add_argument('--num_images', help="Number of images per synonym.",
                        default=1,
                        type=int)  # TODO(Kory): is this still a useful parameter? We should probably remove it
    parser.add_argument('--num_slides', help="Number of slides to create.",
                        default=3, type=int)
    parser.add_argument('--schema', help="The presentation schema to generate the presentation with",
                        default="default", type=str)
    args = parser.parse_args()
    main(args)
