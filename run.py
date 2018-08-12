import argparse
import math
import ntpath
import os.path
import pathlib
import random
from functools import lru_cache
from os import listdir
from os.path import isfile, join

import numpy
import requests
import safygiphy
from google_images_download import google_images_download

import goodreads
# Own modules:
import language_util
import random_util
import reddit
import slide_templates
import text_generator
import wikihow
from presentation_schema import PresentationSchema, SlideGenerator, constant_weight, create_peaked_weight

MAX_PRESENTATION_SAVE_TRIES = 100


# == HELPER FUNCTIONS ==
def _save_presentation_to_pptx(output_folder, file_name, prs, index=0):
    """Save the talk."""
    if index > MAX_PRESENTATION_SAVE_TRIES:
        return None

    suffix = "_" + str(index) if index > 0 else ""
    fp = os.path.join(output_folder, str(file_name) + str(suffix) + ".pptx")
    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(fp)).mkdir(parents=True, exist_ok=True)
    try:
        prs.save(fp)
        print('Saved talk to {}'.format(fp))
        return fp
    except PermissionError:
        index += 1
        return _save_presentation_to_pptx(output_folder, file_name, prs, index)


def download_image(from_url, to_url):
    """Download image from url to path."""
    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(to_url)).mkdir(parents=True, exist_ok=True)

    # Download
    f = open(to_url, 'wb')
    f.write(requests.get(from_url).content)
    f.close()


def get_file_name(url):
    return ntpath.basename(url)


def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]


# == MAIN ==

def main(arguments):
    """Make a talk with the given topic."""
    # Print status details
    print('******************************************')
    print("Making {} slide talk on: {}".format(arguments.num_slides, arguments.topic))

    # Retrieve the schema to generate the presentation with
    schema = get_schema(args.schema)

    # Generate random presenter name if no presenter name given
    if not arguments.presenter:
        arguments.presenter = full_name_generator()

    # Generate the presentation object
    presentation = schema.generate_presentation(topic=arguments.topic,
                                                num_slides=arguments.num_slides,
                                                presenter=arguments.presenter)

    # Save presentation
    presentation_file = _save_presentation_to_pptx(arguments.output_folder, arguments.topic, presentation)
    if args.open_file and presentation_file is not None:
        path = os.path.realpath(presentation_file)
        os.startfile(path)


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


# == CONTENT GENERATORS ==
# These functions generate content, sometimes related to given arguments

def get_google_images(presentation_context, num_images=1):
    word = presentation_context["seed"]
    lp = 'downloads/' + word + '/'
    paths = _get_google_image_cached(word, num_images, lp)

    # If no local images, search on Google Image Search
    if not bool(paths) or len(paths) == 0:
        paths = []
        # Get related images at 16x9 aspect ratio
        response = google_images_download.googleimagesdownload()
        arguments = {
            'keywords': word,
            'limit': num_images,
            'print_urls': False,
            'exact_size': '1600,900',
        }
        # passing the arguments to the function
        paths_dict = response.download(arguments)
        for value in paths_dict.values():
            paths.extend(value)

        # printing absolute paths of the downloaded images
        # print('paths of images', paths)
    return paths


@lru_cache(maxsize=20)
def _get_google_image_cached(word, num_image, lp):
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


# TITLE GENERATORS
talk_title_generator = text_generator.TemplatedTextGenerator('data/text-templates/talk_title.txt').generate
talk_subtitle_generator = text_generator.TraceryTextGenerator('data/text-templates/talk_subtitle.json').generate

inspiration_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/inspiration.txt").generate
history_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/history.txt").generate
history_person_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/history_person.txt").generate
history_and_history_person_title_generator = combined_generator(
    [(4, history_title_generator), (6, history_person_title_generator)])
about_me_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/about-me.txt").generate
historical_name_generator = text_generator.TraceryTextGenerator("./data/text-templates/name.json",
                                                                "title_name").generate
full_name_generator = text_generator.TraceryTextGenerator("./data/text-templates/name.json",
                                                          "full_name").generate


# QUOTES
def create_goodreads_quote_generator(max_quote_length):
    def generator(presentation_context):
        seed = presentation_context["seed"]
        quotes = goodreads.search_quotes(seed, 50)
        filtered_quotes = [quote for quote in quotes if len(quote) <= max_quote_length]
        return random.choice(filtered_quotes)

    return generator


# INSPIROBOT

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


# REDDIT
class RedditImageGenerator:
    def __init__(self, subreddit):
        self._subreddit = subreddit

    def generate(self, presentation_context):
        seed = presentation_context["seed"]
        images = reddit.search_subreddit(self._subreddit, seed + " nsfw:no (url:.jpg OR url:.png OR url:.gif)")
        while len(images) > 0:
            chosen_image = random.choice(images)
            chosen_image_url = chosen_image.url
            downloaded_url = "downloads/reddit/" + self._subreddit + "/" + get_file_name(chosen_image_url)
            try:
                download_image(chosen_image_url, downloaded_url)
                return downloaded_url
            except PermissionError:
                print("Permission error when downloading", chosen_image_url)
            except requests.exceptions.MissingSchema:
                print("Missing schema for image ", chosen_image_url)
            except OSError:
                print("Non existing image for: ", chosen_image_url)
            images.remove(chosen_image)
        return None


def create_reddit_image_generator(name):
    return RedditImageGenerator(name).generate


weird_image_generator = create_reddit_image_generator("hmmm+hmm+wtf+wtfstockphotos+photoshopbattles"
                                                      "+confusing_perspective+cursedimages+HybridAnimals")


# GOOGLE IMAGES

def get_related_google_image(seed_word):
    # Get all image paths
    # img_paths = args.all_paths.get(word)
    img_paths = get_google_images(seed_word, 1)
    if img_paths:
        # Pick one of the images
        img_path = random.choice(img_paths)
        return img_path


# GIFS

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


giphy_generator = seeded_generator(get_related_giphy)
reddit_gif_generator = create_reddit_image_generator("gifs+gif+gifextra+nonononoYES")

combined_gif_generator = combined_generator([(.5, giphy_generator), (.5, reddit_gif_generator)])

# OLD
vintage_person_generator = create_reddit_image_generator("OldSchoolCool")
vintage_picture_generator = create_reddit_image_generator("TheWayWeWere+100yearsago+ColorizedHistory")

# BOLD_STATEMENT

bold_statement_templated_generator = text_generator.TemplatedTextGenerator('data/text-templates/bold-statements.txt')


def generate_wikihow_bold_statement(presentation_context):
    # template_values = {
    #     "topic": seed,
    #     # TODO: Use datamuse or conceptnet or some other mechanism of finding a related location
    #     'location': 'Here'
    # }
    template_values = presentation_context
    # TODO: Sometimes "Articles Form Wikihow" is being scraped as an action, this is a bug
    related_actions = wikihow.get_related_wikihow_actions(presentation_context["seed"])
    if related_actions:
        action = random.choice(related_actions)
        template_values.update({'action': action.title(),
                                # TODO: Make a scraper that scrapes a step related to this action on wikihow.
                                'step': 'Do Whatever You Like'})

    return bold_statement_templated_generator.generate(template_values)


# DOUBLE CAPTIONS

_double_captions_generator = text_generator.TemplatedTextGenerator("./data/text-templates/double-captions.txt")


def create_double_image_captions(presentation_context):
    line = _double_captions_generator.generate(presentation_context)
    parts = line.split("|")
    return parts[0], parts[1]


# == SCHEMAS ==

# This object holds all the information about how to generate the presentation
presentation_schema = PresentationSchema(
    # Basic powerpoint generator
    slide_templates.create_new_powerpoint,
    # Topic per slide generator
    lambda topic, num_slides: SynonymTopicGenerator(topic, num_slides),

    # Slide generators
    [
        SlideGenerator(
            slide_templates.generate_title_slide(talk_title_generator, talk_subtitle_generator),
            weight_function=create_peaked_weight([0], 100000, 0),
            name="Title slide"),
        SlideGenerator(
            slide_templates.generate_two_column_images_slide_text_second(
                history_and_history_person_title_generator,
                historical_name_generator,
                vintage_person_generator,
                none_generator,
                create_goodreads_quote_generator(280)
            ),
            weight_function=create_peaked_weight([1, 2], 10, 0.4),
            allowed_repeated_elements=1,
            name="Historical Figure Quote"),
        SlideGenerator(
            slide_templates.generate_two_column_images_slide(
                history_title_generator,
                none_generator,
                vintage_picture_generator,
                none_generator,
                vintage_picture_generator
            ),
            weight_function=create_peaked_weight([1, 2], 4, 0.2),
            allowed_repeated_elements=1,
            name="Two History Pictures"),
        SlideGenerator(
            slide_templates.generate_full_image_slide(seeded_identity_generator, combined_gif_generator),
            name="Full Screen Giphy"),
        SlideGenerator(
            slide_templates.generate_image_slide(inspiration_title_generator, get_random_inspirobot_image),
            weight_function=constant_weight(0.6),
            name="Inspirobot"),
        SlideGenerator(
            slide_templates.generate_large_quote_slide(generate_wikihow_bold_statement),
            name="Wikihow Bold Statement"),
        SlideGenerator(
            slide_templates.generate_full_image_slide(seeded_identity_generator, get_related_google_image),
            name="Google Images"),
        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(seeded_identity_generator,
                                                                           create_double_image_captions,
                                                                           combined_gif_generator,
                                                                           combined_gif_generator),
            name="Two Captions Gifs"),
        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(seeded_identity_generator,
                                                                           create_double_image_captions,
                                                                           weird_image_generator,
                                                                           weird_image_generator),
            name="Two Captions Weird Reddit"),
    ]
)

test_schema = PresentationSchema(
    # Basic powerpoint generator
    slide_templates.create_new_powerpoint,
    # Topic per slide generator
    lambda topic, num_slides: IdentityTopicGenerator(topic, num_slides),
    # Slide generators
    [
        SlideGenerator(
            slide_templates.generate_title_slide(talk_title_generator, talk_subtitle_generator),
            weight_function=constant_weight(100000),
            allowed_repeated_elements=1,
            name="Two History Pictures"),
        # Back up in case something goes wrong
        SlideGenerator(
            slide_templates.generate_image_slide(
                inspiration_title_generator,
                create_static_generator("downloads/inspirobot/01-743.jpg")),
            allowed_repeated_elements=1,
            name="Fake Inspirobot")
    ])

schemas = {
    "default": presentation_schema,
    "test": test_schema
}


def get_schema(name):
    return schemas[name]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', help="Topic of presentation.",
                        default='cat', type=str)
    parser.add_argument('--num_images', help="Number of images per synonym.",
                        default=1,
                        type=int)  # TODO(Kory): is this still a useful parameter? We should probably remove it
    parser.add_argument('--num_slides', help="Number of slides to create.",
                        default=10, type=int)
    parser.add_argument('--schema', help="The presentation schema to generate the presentation with",
                        default="default", type=str)
    parser.add_argument('--presenter', help="The full name of the presenter, leave blank to randomise",
                        default=None, type=str)
    parser.add_argument('--output_folder', help="The folder to output the generated presentations",
                        default="./output/", type=str)
    parser.add_argument('--open_file', help="If this flag is true, the generated powerpoint will automatically open",
                        default=True, type=bool)
    args = parser.parse_args()
    main(args)
