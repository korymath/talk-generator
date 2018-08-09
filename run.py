import argparse
import math
import ntpath
import os.path
import pathlib
import random
from os import listdir
from os.path import isfile, join

import numpy
import requests
import safygiphy
from google_images_download import google_images_download

import language_util
import reddit
# Own classes:
import slide_templates
import text_generator
import wikihow
from presentation_schema import PresentationSchema, SlideGenerator, constant_weight


def create_identity_topic_generator(topic, _):
    """ Generates always the given topic as the seed for each slide """
    return lambda _: topic


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


def get_file_name(url):
    return ntpath.basename(url)


def read_lines(file):
    return [line.rstrip('\n') for line in open(file)]


# CONTENT GENERATORS
# These functions generate content, sometimes related to given arguments

def get_google_images(word, num_images=1):
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
    chosen_synonym_plural = language_util.to_plural(seed)
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
    template_values = {
        "topic": seed,
        # TODO: Use datamuse or conceptnet or some other mechanism of finding a related location
        'location': 'Here'
    }
    # TODO: Sometimes "Articles Form Wikihow" is being scraped as an action, this is a bug
    related_actions = wikihow.get_related_wikihow_actions(seed)
    if related_actions:
        action = random.choice(related_actions)
        template_values.update({'action': action.title(),
                                # TODO: Make a scraper that scrapes a step related to this action on wikihow.
                                'step': 'Do Whatever You Like'})

    return bold_statement_templated_generator.generate(template_values)


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


def create_static_generator(always_generate_this):
    return lambda _: always_generate_this


def create_double_image_captions(_):
    lines = read_lines("./data/text-templates/double-captions.txt")
    line = random.choice(lines)
    parts = line.split("|")
    return parts[0], parts[1]


class RedditImageGenerator:
    def __init__(self, subreddit):
        self._subreddit = subreddit

    def generate(self, seed):
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


inspirational_title_generator = text_generator.TemplatedTextGenerator("data/text-templates/inspiration.txt")


def generate_inspirational_title(seed):
    return inspirational_title_generator.generate({"topic": seed})


weird_image_generator = create_reddit_image_generator("hmmm+hmm+wtf+wtfstockphotos+photoshopbattles"
                                                      "+confusing_perspective+cursedimages")

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
     SlideGenerator(slide_templates.generate_image_slide(generate_inspirational_title, get_random_inspirobot_image),
                    name="Inspirobot"),
     SlideGenerator(slide_templates.generate_large_quote_slide(generate_wikihow_bold_statement),
                    name="Wikihow Bold Statement"),
     SlideGenerator(slide_templates.generate_full_image_slide(identity_generator, get_related_google_image),
                    name="Google Images"),
     SlideGenerator(
         slide_templates.generate_two_column_images_slide_tuple_caption(identity_generator,
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
    lambda topic, num_slides: create_identity_topic_generator(topic, num_slides),

    # Slide generators

    [

        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(identity_generator,
                                                                           create_double_image_captions,
                                                                           weird_image_generator,
                                                                           weird_image_generator),
            weight_function=constant_weight(1000),
            name="Two Captions Weird Reddit"),
        # Back up in case something goes wrong
        SlideGenerator(slide_templates.generate_image_slide(generate_inspirational_title,
                                                            # get_random_inspirobot_image),
                                                            create_static_generator("downloads/inspirobot/01-743.jpg")),
                       name="Inspirobot")
        # SlideGenerator(slide_templates.generate_large_quote_slide(generate_wikihow_bold_statement),
        #                name="Wikihow Bold Statement")
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
