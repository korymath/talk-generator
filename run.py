import argparse
import os.path
import pathlib
import random

import safygiphy

# Own modules:
import chart
import goodreads
import google_images
import inspirobot
import os_util
import reddit
import shitpostbot
import slide_templates
import slide_topic_generators
import text_generator
import wikihow
# Import a lot from generator_util to make schema creation easier
from generator_util import create_seeded_generator, none_generator, create_static_generator, combined_generator, \
    create_from_external_image_list_generator, create_from_list_generator, \
    create_backup_generator, remove_invalid_images_from_generator, create_inspired_tuple_generator, \
    apply_function_to_generator, create_tupled_generator
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


# == MAIN ==

def main(arguments):
    """Make a talk with the given topic."""
    # Print status details
    print('******************************************')
    print("Making {} slide talk on: {}".format(arguments.num_slides, arguments.topic))

    # Retrieve the schema to generate the presentation with
    schema = get_schema(arguments.schema)

    # Generate random presenter name if no presenter name given
    if not arguments.presenter:
        arguments.presenter = full_name_generator()

    # Generate the presentation object
    presentation = schema.generate_presentation(topic=arguments.topic,
                                                num_slides=arguments.num_slides,
                                                presenter=arguments.presenter)

    # Save presentation
    if arguments.save_ppt:
        presentation_file = _save_presentation_to_pptx(arguments.output_folder, arguments.topic, presentation)

        # Open the presentation
        if arguments.open_ppt and presentation_file is not None:
            path = os.path.realpath(presentation_file)
            os.startfile(path)

    return presentation


# = TEXT GENERATORS=

# TITLES
talk_title_generator = text_generator.TemplatedTextGenerator('data/text-templates/talk_title.txt').generate
talk_subtitle_generator = text_generator.TraceryTextGenerator('data/text-templates/talk_subtitle.json').generate

default_slide_title_generator = text_generator.TemplatedTextGenerator(
    'data/text-templates/default_slide_title.txt').generate

anticipation_title_generator = text_generator.TemplatedTextGenerator(
    'data/text-templates/anticipation_title.txt').generate

conclusion_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/conclusion_title.txt").generate
inspiration_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/inspiration.txt").generate
anecdote_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/anecdote_title.txt").generate
history_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/history.txt").generate
history_person_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/history_person.txt").generate
history_and_history_person_title_generator = combined_generator(
    (4, history_title_generator), (6, history_person_title_generator))
about_me_title_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/about_me_title.txt").generate

# NAMES
historical_name_generator = text_generator.TraceryTextGenerator("./data/text-templates/name.json",
                                                                "title_name").generate
full_name_generator = text_generator.TraceryTextGenerator("./data/text-templates/name.json",
                                                          "full_name").generate

# ABOUT ME
_about_me_facts_grammar = "./data/text-templates/about_me_facts.json"
book_description_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                                 "book_description").generate
location_description_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                                     "location_description").generate
hobby_description_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                                  "hobby_description").generate
job_description_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                                "job_description").generate
country_description_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                                    "country_description").generate
job_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                    "job").generate
country_generator = text_generator.TraceryTextGenerator(_about_me_facts_grammar,
                                                        "country").generate

# PROMPTS & CHALLENGES

anecdote_prompt_generator = text_generator.TemplatedTextGenerator(
    "data/text-templates/anecdote_prompt.txt").generate


# QUOTES
def create_goodreads_quote_generator(max_quote_length):
    def generator(seed):
        return [quote for quote in goodreads.search_quotes(seed, 50) if len(quote) <= max_quote_length]

    return create_from_list_generator(create_seeded_generator(generator))


# INSPIROBOT
inspirobot_image_generator = inspirobot.get_random_inspirobot_image


# REDDIT
class RedditImageGenerator:
    def __init__(self, subreddit):
        self._subreddit = subreddit

        def generate(seed):
            results = reddit.search_subreddit(
                self._subreddit,
                str(seed) + " nsfw:no (url:.jpg OR url:.png OR url:.gif)")
            if bool(results):
                return [post.url for post in results]

        self._generate = create_from_external_image_list_generator(
            create_seeded_generator(generate),
            lambda url: "./downloads/reddit/" + self._subreddit + "/" + os_util.get_file_name(url)
        )

    def generate(self, presentation_context):
        return self._generate(presentation_context)

    def generate_random(self, _):
        return self.generate({"seed": ""})


def create_reddit_image_generator(*name):
    reddit_generator = RedditImageGenerator("+".join(name))
    return create_backup_generator(reddit_generator.generate, reddit_generator.generate_random)


weird_image_generator = create_reddit_image_generator("hmmm", "hmm", "wtf", "wtfstockphotos", "photoshopbattles",
                                                      "confusing_perspective", "cursedimages", "HybridAnimals")

shitpostbot_image_generator = create_from_external_image_list_generator(
    create_seeded_generator(
        create_backup_generator(
            shitpostbot.search_images,
            shitpostbot.get_random_images
        )),
    lambda url: "./downloads/shitpostbot/{}".format(os_util.get_file_name(url))
)

weird_and_shitpost_generator = combined_generator(
    (1, weird_image_generator),
    (2, shitpostbot_image_generator)
)

# GIFS

giphy = safygiphy.Giphy()


def get_related_giphy(seed_word):
    if bool(seed_word):
        response = giphy.random(tag=seed_word)
    else:
        response = giphy.random()

    if bool(response):
        data = response.get('data')
        if bool(data):
            images = data.get('images')
            original = images.get('original')
            giphy_url = original.get('url')
            gif_name = os.path.basename(os.path.dirname(giphy_url))
            image_url = 'downloads/giphy/' + str(seed_word) + "/" + gif_name + ".gif"
            os_util.download_image(giphy_url, image_url)
            return image_url


giphy_generator = create_backup_generator(
    create_seeded_generator(get_related_giphy),
    lambda _: get_related_giphy(None)
)
reddit_gif_generator = create_reddit_image_generator("gifs", "gif", "gifextra", "nonononoYES")

combined_gif_generator = combined_generator((.5, giphy_generator), (.5, reddit_gif_generator))

weird_and_shitpost_and_gif_generator = combined_generator(
    (1, weird_image_generator),
    (1, shitpostbot_image_generator),
    (1, combined_gif_generator)
)

# GOOGLE IMAGES

generate_full_screen_google_image = create_from_list_generator(
    remove_invalid_images_from_generator(
        create_seeded_generator(
            google_images.create_full_screen_image_generator())))

generate_wide_google_image = create_from_list_generator(
    remove_invalid_images_from_generator(
        create_seeded_generator(
            google_images.create_wide_image_generator())))

generate_google_image = create_from_list_generator(
    remove_invalid_images_from_generator(
        create_seeded_generator(
            google_images.create_image_generator())))

generate_google_image_from_word = create_from_list_generator(
    remove_invalid_images_from_generator(
        google_images.create_image_generator()))

# OLD/VINTAGE
vintage_person_generator = create_reddit_image_generator("OldSchoolCool")
vintage_picture_generator = create_reddit_image_generator("TheWayWeWere", "100yearsago", "ColorizedHistory")

reddit_book_cover_generator = create_reddit_image_generator("BookCovers", "fakebookcovers", "coverdesign", "bookdesign")

reddit_location_image_generator = create_reddit_image_generator("evilbuildings", "itookapicture", "SkyPorn",
                                                                "EarthPorn")

# BOLD_STATEMENT

bold_statement_templated_generator = text_generator.TemplatedTextGenerator('data/text-templates/bold_statements.txt')


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

def split_captions_generator(generator):
    def create_double_image_captions(presentation_context):
        line = generator.generate(presentation_context)
        parts = line.split("|")
        return parts

    return create_double_image_captions


_double_captions_generator = text_generator.TemplatedTextGenerator("./data/text-templates/double_captions.txt")
_triple_captions_generator = text_generator.TemplatedTextGenerator("./data/text-templates/triple_captions.txt")
_historic_double_captions_generator = text_generator.TemplatedTextGenerator(
    "./data/text-templates/historic_double_captions.txt")

double_captions_generator = split_captions_generator(_double_captions_generator)
triple_captions_generator = split_captions_generator(_triple_captions_generator)
historic_double_captions_generator = split_captions_generator(_historic_double_captions_generator)


# TUPLED ABOUT ME

def _apply_job_prefix(job_name):
    if random.uniform(0, 1) < 0.55:
        return job_name
    return job_description_generator() + ": " + job_name


def _apply_country_prefix(country_name):
    if random.uniform(0, 1) < 0.55:
        return country_name
    return country_description_generator() + country_name


about_me_hobby_tuple_generator = create_tupled_generator(
    hobby_description_generator,
    weird_and_shitpost_generator
)
about_me_book_tuple_generator = create_tupled_generator(
    book_description_generator,
    reddit_book_cover_generator,
)
about_me_location_tuple_generator = create_tupled_generator(
    location_description_generator,
    reddit_location_image_generator,
)
about_me_job_tuple_generator = apply_function_to_generator(
    create_inspired_tuple_generator(
        apply_function_to_generator(
            job_generator,
            str.title
        ),
        generate_google_image_from_word
    ),
    lambda x: (_apply_job_prefix(x[0]), x[1])
)

about_me_country_tuple_generator = apply_function_to_generator(
    create_inspired_tuple_generator(
        country_generator,
        generate_google_image_from_word
    ),
    lambda x: (_apply_country_prefix(x[0]), x[1])
)

about_me_location_or_country_tuple_generator = combined_generator(
    (3, about_me_country_tuple_generator),
    (1, about_me_location_tuple_generator),
)

# Charts

reddit_chart_generator = create_reddit_image_generator("dataisbeautiful", "funnycharts", "charts")

# chart_generator = create_seeded_generator(charts.generate_test_chart)

# == SCHEMAS ==

# This object holds all the information about how to generate the presentation
presentation_schema = PresentationSchema(
    # Basic powerpoint generator
    slide_templates.create_new_powerpoint,
    # Topic per slide generator
    slide_topic_generators.SideTrackingTopicGenerator,

    # Slide generators
    [
        # TITLE
        SlideGenerator(
            slide_templates.generate_title_slide(talk_title_generator, talk_subtitle_generator),
            weight_function=create_peaked_weight((0,), 100000, 0),
            tags=["title"],
            name="Title slide"),

        # ABOUT ME
        SlideGenerator(
            slide_templates.generate_three_column_images_slide_tuple(
                about_me_title_generator,
                about_me_location_or_country_tuple_generator,
                about_me_job_tuple_generator,
                about_me_hobby_tuple_generator,
            ),
            create_peaked_weight((1,), 300, 0),
            allowed_repeated_elements=3,
            tags=["about_me"],
            name="About Me: Location-Job-WeirdHobby"),

        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple(
                about_me_title_generator,
                about_me_location_or_country_tuple_generator,
                about_me_job_tuple_generator,
            ),
            create_peaked_weight((1,), 100, 0),
            allowed_repeated_elements=3,
            tags=["about_me"],
            name="About Me: Location-Job"),

        SlideGenerator(
            slide_templates.generate_three_column_images_slide_tuple(
                about_me_title_generator,
                about_me_location_or_country_tuple_generator,
                about_me_book_tuple_generator,
                about_me_hobby_tuple_generator,
            ),
            create_peaked_weight((1,), 100, 0),
            allowed_repeated_elements=0,
            tags=["about_me"],
            name="About Me: Location-Book-WeirdHobby"),

        SlideGenerator(
            slide_templates.generate_image_slide_tuple(
                about_me_hobby_tuple_generator
            ),
            create_peaked_weight((1, 2), 5, 0),
            allowed_repeated_elements=0,
            tags=["about_me"],
            name="Weird Hobby"),

        # HISTORY
        SlideGenerator(
            slide_templates.generate_two_column_images_slide(
                history_and_history_person_title_generator,
                historical_name_generator,
                vintage_person_generator,
                none_generator,
                create_goodreads_quote_generator(280)
            ),
            weight_function=create_peaked_weight((2, 3), 30, 0.1),
            allowed_repeated_elements=0,
            tags=["history", "quote"],
            name="Historical Figure Quote"),

        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(
                history_title_generator,
                historic_double_captions_generator,
                vintage_picture_generator,
                vintage_picture_generator
            ),
            weight_function=create_peaked_weight((2, 3), 12, 0.05),
            allowed_repeated_elements=0,
            tags=["history", "two_images"],
            name="Two History Pictures"),

        # FULL SCREEN RELATED IMAGES
        SlideGenerator(
            slide_templates.generate_full_image_slide(
                anticipation_title_generator,
                combined_gif_generator),
            tags=["full_image", "gif"],
            name="Full Screen Giphy"),
        SlideGenerator(
            slide_templates.generate_image_slide(
                default_slide_title_generator,
                combined_gif_generator),
            tags=["single_image", "gif"],
            name="Single Image Giphy"),
        SlideGenerator(
            slide_templates.generate_full_image_slide(
                none_generator,
                generate_full_screen_google_image),
            tags=["full_image", "google_images"],
            name="Full Screen Google Images"),
        SlideGenerator(
            slide_templates.generate_full_image_slide(
                default_slide_title_generator,
                generate_wide_google_image),
            tags=["full_image", "google_images"],
            name="Wide Google Images"),

        # WISE STATEMENTS

        SlideGenerator(
            slide_templates.generate_image_slide(
                inspiration_title_generator,
                inspirobot_image_generator),
            weight_function=constant_weight(0.6),
            tags=["inspiration", "statement"],
            name="Inspirobot"),

        SlideGenerator(
            slide_templates.generate_large_quote_slide(
                title_generator=none_generator,
                text_generator=generate_wikihow_bold_statement,
                background_image_generator=generate_full_screen_google_image),
            tags=["bold_statement", "statement"],
            name="Wikihow Bold Statement"),

        SlideGenerator(
            slide_templates.generate_large_quote_slide(
                title_generator=none_generator,
                text_generator=create_goodreads_quote_generator(250),
                background_image_generator=generate_full_screen_google_image),
            weight_function=constant_weight(0.6),
            tags=["quote", "statement"],
            name="Goodreads Quote"),

        SlideGenerator(
            slide_templates.generate_large_quote_slide(
                title_generator=none_generator,
                text_generator=anecdote_prompt_generator,
                background_image_generator=generate_full_screen_google_image
            ),
            tags=["anecdote"],
            name="Anecdote"),

        # TWO CAPTIONS VARIATIONS
        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(
                default_slide_title_generator,
                double_captions_generator,
                combined_gif_generator,
                combined_gif_generator),
            weight_function=constant_weight(2),
            tags=["multi_caption", "two_captions", "gif"],
            name="Two Captions Gifs"),

        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(
                default_slide_title_generator,
                double_captions_generator,
                weird_image_generator,
                weird_and_shitpost_generator),
            weight_function=constant_weight(2),
            tags=["multi_caption", "two_captions", "reddit"],
            name="Two Captions Weird Reddit"),

        SlideGenerator(
            slide_templates.generate_two_column_images_slide_tuple_caption(
                default_slide_title_generator,
                double_captions_generator,
                weird_and_shitpost_and_gif_generator,
                weird_and_shitpost_and_gif_generator),
            weight_function=constant_weight(2),
            tags=["multi_caption", "two_captions", "reddit"],
            name="Two Captions Weird"),

        SlideGenerator(
            slide_templates.generate_three_column_images_slide_tuple_caption(
                default_slide_title_generator,
                triple_captions_generator,
                weird_and_shitpost_and_gif_generator,
                weird_and_shitpost_and_gif_generator,
                weird_and_shitpost_generator),
            weight_function=constant_weight(1),
            allowed_repeated_elements=4,
            tags=["multi_caption", "three_captions", "reddit"],
            name="Three Captions Weird"),

        # CHARTS

        SlideGenerator(
            slide_templates.generate_full_image_slide(
                none_generator,
                reddit_chart_generator),
            weight_function=constant_weight(2),
            allowed_repeated_elements=0,
            tags=["chart"],
            name="Reddit Chart"),

        SlideGenerator(
            slide_templates.generate_chart_slide_tuple(
                chart.generate_yes_no_pie
            ),
            retries=1,
            allowed_repeated_elements=4,
            weight_function=constant_weight(2),
            tags=["pie_chart", "yes_no_chart", "chart"],
            name="Yes/No/Funny Chart"),

        SlideGenerator(
            slide_templates.generate_chart_slide_tuple(
                chart.generate_location_pie
            ),
            allowed_repeated_elements=4,
            retries=1,
            weight_function=constant_weight(0.1),
            tags=["location_chart", "pie_chart", "chart"],
            name="Location Chart"),
        SlideGenerator(
            slide_templates.generate_chart_slide_tuple(
                chart.generate_property_pie
            ),
            allowed_repeated_elements=4,
            retries=1,
            weight_function=constant_weight(0.05),
            tags=["property_chart", "pie_chart", "chart"],
            name="Property Chart"),
        SlideGenerator(
            slide_templates.generate_chart_slide_tuple(
                chart.generate_correlation_curve
            ),
            allowed_repeated_elements=4,
            retries=1,
            weight_function=constant_weight(0.5),
            tags=["curve", "chart"],
            name="Correlation Curve"),

        # CONCLUSION:
        SlideGenerator(
            slide_templates.generate_two_column_images_slide(
                conclusion_title_generator,
                create_static_generator("Conclusion 1"),
                generate_google_image,
                # none_generator("Conclusion 2"),
                # generate_google_image,
                create_static_generator("Conclusion 2"),
                weird_image_generator,
            ),
            weight_function=create_peaked_weight((-1,), 10000, 0),
            allowed_repeated_elements=10,
            tags=["conclusion"],
            name="Conclusion"),
        SlideGenerator(
            slide_templates.generate_three_column_images_slide(
                conclusion_title_generator,
                create_static_generator("Conclusion 1"),
                generate_google_image,
                create_static_generator("Conclusion 2"),
                weird_image_generator,
                create_static_generator("Conclusion 3"),
                combined_gif_generator,
            ),
            weight_function=create_peaked_weight((-1,), 5000, 0),
            allowed_repeated_elements=10,
            tags=["conclusion"],
            name="Conclusion"),
    ],
    # Max tags
    max_allowed_tags={
        # Absolute maxima
        "title": 1,
        "about_me": 1,
        "history": 1,
        "anecdote": 1,
        "location_chart": 1,

        # Relative (procentual) maxima
        "two_captions": 0.3,
        "three_captions": 0.2,
        "multi_captions": 0.3,
        "gif": 0.5,
        "weird": 0.5,
        "quote": 0.1,
        "statement": 0.2,
        "chart": 0.2
    },
)

test_schema = PresentationSchema(
    # Basic powerpoint generator
    slide_templates.create_new_powerpoint,
    # Topic per slide generator
    # seed_generator=slide_topic_generators.SideTrackingTopicGenerator,
    seed_generator=slide_topic_generators.IdentityTopicGenerator,
    # Slide generators
    slide_generators=[
        SlideGenerator(
            slide_templates.generate_chart_slide_tuple(
                chart.generate_correlation_curve
            ),
            allowed_repeated_elements=4,
            retries=1,
            weight_function=constant_weight(1),
            tags=["curve", "chart"],
            name="Correlation Curve"),

        # Back up in case something goes wrong
        SlideGenerator(
            slide_templates.generate_image_slide(
                inspiration_title_generator,
                create_static_generator("./data/images/error_placeholder.png")),
            allowed_repeated_elements=2,
            weight_function=constant_weight(0.0001),
            name="Error Placeholder")
    ],
)

schemas = {
    "default": presentation_schema,
    "test": test_schema
}


def get_schema(name):
    return schemas[name]


# From https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', help="Topic of presentation.",
                        default='cat', type=str)
    parser.add_argument('--num_slides', help="Number of slides to create.",
                        default=10, type=int)
    parser.add_argument('--schema', help="The presentation schema to generate the presentation with",
                        default="default", type=str)
    parser.add_argument('--presenter', help="The full name of the presenter, leave blank to randomise",
                        default=None, type=str)
    parser.add_argument('--output_folder', help="The folder to output the generated presentations",
                        default="./output/", type=str)
    parser.add_argument('--save_ppt', help="If this flag is true, the generated powerpoint will be saved",
                        default=True, type=str2bool)
    parser.add_argument('--open_ppt', help="If this flag is true, the generated powerpoint will automatically open",
                        default=True, type=str2bool)
    args = parser.parse_args()
    main(args)
