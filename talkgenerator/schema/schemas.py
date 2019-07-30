import random

from talkgenerator.util import os_util
from talkgenerator.sources import shitpostbot, unsplash
from talkgenerator.sources import wikihow
from talkgenerator.sources import google_images
from talkgenerator.sources import inspirobot
from talkgenerator.sources import chart
from talkgenerator.sources import giphy
from talkgenerator.schema import slide_topic_generators
from talkgenerator.slide import powerpoint_slide_creator
from talkgenerator.slide import slide_generators
from talkgenerator.util.generator_util import SeededGenerator
from talkgenerator.util.generator_util import NoneGenerator
from talkgenerator.util.generator_util import CombinedGenerator
from talkgenerator.util.generator_util import ExternalImageListGenerator
from talkgenerator.util.generator_util import FromListGenerator
from talkgenerator.util.generator_util import BackupGenerator
from talkgenerator.util.generator_util import InvalidImagesRemoverGenerator
from talkgenerator.util.generator_util import InspiredTupleGenerator
from talkgenerator.util.generator_util import MappedGenerator
from talkgenerator.util.generator_util import TupledGenerator
from talkgenerator.schema.presentation_schema import PresentationSchema
from talkgenerator.schema.slide_generator_data import SlideGeneratorData
from talkgenerator.schema.slide_generator_data import ConstantWeightFunction
from talkgenerator.schema.slide_generator_data import PeakedWeight

from talkgenerator.schema.content_generator_structures import RedditImageGenerator
from talkgenerator.schema.content_generator_structures import ShitPostBotURLGenerator
from talkgenerator.schema.content_generator_structures import GoodReadsQuoteGenerator
from talkgenerator.schema.content_generator_structures import CountryPrefixApplier
from talkgenerator.schema.content_generator_structures import JobPrefixApplier
from talkgenerator.schema.content_generator_structures import create_tracery_generator
from talkgenerator.schema.content_generator_structures import create_templated_text_generator
from talkgenerator.schema.content_generator_structures import create_reddit_image_generator
from talkgenerator.schema.content_generator_structures import SplitCaptionsGenerator
from talkgenerator.schema.content_generator_structures import generate_wikihow_bold_statement
from talkgenerator.schema.content_generator_structures import generate_google_image_generator
from talkgenerator.schema.content_generator_structures import UnsplashURLGenerator

# ===============================
# =====  CONTENT GENERATORS =====
# ===============================

# === TEXT GENERATORS ===

# TITLES
talk_title_generator = create_templated_text_generator("data/text-templates/talk_title.txt")
talk_subtitle_generator = create_tracery_generator("data/text-templates/talk_subtitle.json")


def talk_title_generator_if_not_generated(presentation_context):
    if presentation_context['title'] is not None:
        return presentation_context['title']
    return talk_title_generator(presentation_context)


default_slide_title_generator = create_templated_text_generator("data/text-templates/default_slide_title.txt")

default_or_no_title_generator = CombinedGenerator(
    (1, default_slide_title_generator),
    (1, NoneGenerator())
)

anticipation_title_generator = create_templated_text_generator('data/text-templates/anticipation_title.txt')

conclusion_title_generator = create_templated_text_generator("data/text-templates/conclusion_title.txt")
inspiration_title_generator = create_templated_text_generator("data/text-templates/inspiration.txt")
anecdote_title_generator = create_templated_text_generator("data/text-templates/anecdote_title.txt")
history_title_generator = create_templated_text_generator("data/text-templates/history.txt")
history_person_title_generator = create_templated_text_generator("data/text-templates/history_person.txt")
history_and_history_person_title_generator = CombinedGenerator(
    (4, history_title_generator), (6, history_person_title_generator))
about_me_title_generator = create_templated_text_generator("data/text-templates/about_me_title.txt")

# NAMES
historical_name_generator = create_tracery_generator("data/text-templates/name.json", "title_name")
full_name_generator = create_tracery_generator("data/text-templates/name.json", "full_name")

# ABOUT ME
_about_me_facts_grammar = "data/text-templates/about_me_facts.json"
book_description_generator = create_tracery_generator(_about_me_facts_grammar, "book_description")
location_description_generator = create_tracery_generator(_about_me_facts_grammar, "location_description")
hobby_description_generator = create_tracery_generator(_about_me_facts_grammar, "hobby_description")
job_generator = create_tracery_generator(_about_me_facts_grammar, "job")
country_generator = create_tracery_generator(_about_me_facts_grammar, "country")

# PROMPTS & CHALLENGES

anecdote_prompt_generator = create_templated_text_generator(
    "data/text-templates/anecdote_prompt.txt")

# QUOTES
goodreads_quote_generator = GoodReadsQuoteGenerator(250)

# DOUBLE CAPTIONS

_double_image_captions_generator = create_templated_text_generator("data/text-templates/double_captions.txt")
_triple_image_captions_generator = create_templated_text_generator("data/text-templates/triple_captions.txt")
_historic_double_captions_generator = create_templated_text_generator(
    "data/text-templates/historic_double_captions.txt")

double_image_captions_generator = SplitCaptionsGenerator(_double_image_captions_generator)
triple_image_captions_generator = SplitCaptionsGenerator(_triple_image_captions_generator)
historic_double_captions_generator = SplitCaptionsGenerator(_historic_double_captions_generator)

# Conclusions
_conclusions_tuple_grammar = "data/text-templates/conclusion_tuple.json"
conclusion_two_captions_tuple_generator = SplitCaptionsGenerator(
    create_tracery_generator(_conclusions_tuple_grammar, "two_conclusions"))

conclusion_three_captions_tuple_generator = SplitCaptionsGenerator(
    create_tracery_generator(_conclusions_tuple_grammar, "three_conclusions"))

# === IMAGE GENERATORS ===

# INSPIROBOT
inspirobot_image_generator = inspirobot.get_random_inspirobot_image

# GIFS

giphy_generator = BackupGenerator(
    SeededGenerator(giphy.get_related_giphy),
    giphy.get_random_giphy
)
reddit_gif_generator = create_reddit_image_generator("gifs", "gif", "gifextra", "nonononoYES")

combined_gif_generator = CombinedGenerator((.5, giphy_generator), (.5, reddit_gif_generator))

# REDDIT

weird_reddit_image_generator = create_reddit_image_generator("hmmm", "hmm", "wtf", "wtfstockphotos", "weirdstockphotos",
                                                             "darkstockphotos", "photoshopbattles",
                                                             "confusing_perspective", "cursedimages", "HybridAnimals",
                                                             "EyeBleach", "natureismetal")

shitpostbot_image_generator = ExternalImageListGenerator(
    SeededGenerator(
        BackupGenerator(
            shitpostbot.search_images,
            shitpostbot.get_random_images
        )),
    ShitPostBotURLGenerator()
)

weird_punchline_static_image_generator = CombinedGenerator(
    (1, weird_reddit_image_generator),
    (2, shitpostbot_image_generator)
)

weird_punchline_image_generator = CombinedGenerator(
    (5, weird_reddit_image_generator),
    (5, shitpostbot_image_generator),
    (3, combined_gif_generator)
)

# GOOGLE IMAGES

generate_full_screen_google_image = generate_google_image_generator(google_images.FullImageGenerator())

generate_wide_google_image = generate_google_image_generator(google_images.WideImageGenerator())

generate_google_image = generate_google_image_generator(google_images.ImageGenerator())

generate_google_image_from_word = FromListGenerator(InvalidImagesRemoverGenerator(google_images.ImageGenerator()))

# UNSPLASH

generate_unsplash_image = ExternalImageListGenerator(SeededGenerator(unsplash.search_photos_return_urls),
                                                     UnsplashURLGenerator(), check_image_validness=False)
generate_unsplash_image_from_word = ExternalImageListGenerator(unsplash.search_photos_return_urls,
                                                               UnsplashURLGenerator(), check_image_validness=False)

normal_image_generator = CombinedGenerator(
    (1000, generate_unsplash_image),
    (1, generate_google_image)
)

normal_image_generator_from_word = CombinedGenerator(
    (1000, generate_unsplash_image_from_word),
    (1, generate_google_image_from_word)
)

normal_or_weird_image_generator = CombinedGenerator(
    (1, normal_image_generator),
    (1, weird_punchline_image_generator)
)



# OLD/VINTAGE
vintage_person_generator = create_reddit_image_generator("OldSchoolCool")
vintage_picture_generator = create_reddit_image_generator("TheWayWeWere", "100yearsago", "ColorizedHistory")

reddit_book_cover_generator = create_reddit_image_generator("BookCovers", "fakebookcovers", "coverdesign",
                                                            "bookdesign")

reddit_location_image_generator = create_reddit_image_generator("evilbuildings", "itookapicture", "SkyPorn",
                                                                "EarthPorn")

# TUPLED ABOUT ME

about_me_hobby_tuple_generator = TupledGenerator(
    hobby_description_generator,
    weird_punchline_image_generator
)
about_me_book_tuple_generator = TupledGenerator(
    book_description_generator,
    reddit_book_cover_generator,
)
about_me_location_tuple_generator = TupledGenerator(
    location_description_generator,
    reddit_location_image_generator,
)

about_me_job_tuple_generator = MappedGenerator(
    InspiredTupleGenerator(
        MappedGenerator(
            job_generator,
            str.title
        ),
        normal_image_generator_from_word
    ),
    JobPrefixApplier()
)

about_me_country_tuple_generator = MappedGenerator(
    InspiredTupleGenerator(
        country_generator,
        normal_image_generator_from_word
    ),
    CountryPrefixApplier()
)

about_me_location_or_country_tuple_generator = CombinedGenerator(
    (3, about_me_country_tuple_generator),
    (1, about_me_location_tuple_generator),
)

# Charts

reddit_chart_generator = create_reddit_image_generator("dataisbeautiful", "funnycharts", "charts")

# ==============================
# =====  SLIDE GENERATORS  =====
# ==============================


# TITLE SLIDE
title_slide_generators = [
    SlideGeneratorData(
        slide_generators.TitleSlideGenerator.of(talk_title_generator_if_not_generated, talk_subtitle_generator),
        allowed_repeated_elements=3,
        weight_function=PeakedWeight((0,), 100000, 0),
        tags=["title"],
        name="Title slide")
]

# ABOUT ME
about_me_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_three_column_images_slide_tuple(
        slide_generators.ThreeColumnImageSlideGenerator.of_tupled_captioned_images(
            about_me_title_generator,
            about_me_location_or_country_tuple_generator,
            about_me_job_tuple_generator,
            about_me_hobby_tuple_generator,
        ),
        PeakedWeight((1,), 10, 0),
        allowed_repeated_elements=3,
        tags=["about_me"],
        name="About Me: Location-Job-WeirdHobby"),

    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide_tuple(

        slide_generators.TwoColumnImageSlideGenerator.of_tupled_captioned_images(
            about_me_title_generator,
            about_me_location_or_country_tuple_generator,
            about_me_job_tuple_generator,
        ),
        PeakedWeight((1,), 4, 0),
        allowed_repeated_elements=3,
        tags=["about_me"],
        name="About Me: Location-Job"),

    SlideGeneratorData(
        # slide_templates.generate_three_column_images_slide_tuple(
        slide_generators.ThreeColumnImageSlideGenerator.of_tupled_captioned_images(
            about_me_title_generator,
            about_me_location_or_country_tuple_generator,
            about_me_book_tuple_generator,
            about_me_hobby_tuple_generator,
        ),
        PeakedWeight((1,), 4, 0),
        allowed_repeated_elements=0,
        tags=["about_me"],
        name="About Me: Location-Book-WeirdHobby"),

    SlideGeneratorData(
        # slide_templates.generate_image_slide_tuple(
        slide_generators.ImageSlideGenerator.of_tupled_captioned_image(
            about_me_hobby_tuple_generator
        ),
        PeakedWeight((1, 2), 3, 0),
        allowed_repeated_elements=0,
        tags=["about_me"],
        name="Weird Hobby")]

# HISTORY
history_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide(
        slide_generators.TwoColumnImageSlideGenerator.of(
            history_and_history_person_title_generator,
            historical_name_generator,
            vintage_person_generator,
            NoneGenerator(),
            goodreads_quote_generator
        ),
        weight_function=PeakedWeight((2, 3), 20, 0.3),
        allowed_repeated_elements=0,
        tags=["history", "quote"],
        name="Historical Figure Quote"),

    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide_tuple_caption(
        slide_generators.TwoColumnImageSlideGenerator.of_images_and_tupled_captions(
            history_title_generator,
            historic_double_captions_generator,
            vintage_picture_generator,
            vintage_picture_generator
        ),
        weight_function=PeakedWeight((2, 3), 12, 0.1),
        allowed_repeated_elements=0,
        tags=["history", "two_images"],
        name="Two History Pictures")
]

# FULL SCREEN RELATED IMAGES
single_image_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_full_image_slide(
        slide_generators.FullImageSlideGenerator.of(
            anticipation_title_generator,
            combined_gif_generator),
        tags=["full_image", "gif"],
        name="Full Screen Giphy"),
    SlideGeneratorData(
        # slide_templates.generate_image_slide(
        slide_generators.ImageSlideGenerator.of(
            default_slide_title_generator,
            combined_gif_generator),
        tags=["single_image", "gif"],
        name="Single Image Giphy"),
    SlideGeneratorData(
        # slide_templates.generate_full_image_slide(
        slide_generators.FullImageSlideGenerator.of(
            NoneGenerator(),
            CombinedGenerator(
                (1, normal_image_generator),
                (1, generate_wide_google_image)
            )),
        tags=["full_image", "google_images"],
        name="Full Screen Google Images"),
    SlideGeneratorData(
        # slide_templates.generate_full_image_slide(
        slide_generators.FullImageSlideGenerator.of(
            default_slide_title_generator,
            CombinedGenerator(
                (1, normal_image_generator),
                (1, generate_wide_google_image)
            )),
        tags=["full_image", "google_images"],
        name="Wide Google Images")
]

# WISE STATEMENTS
statement_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_image_slide(
        slide_generators.ImageSlideGenerator.of(
            inspiration_title_generator,
            inspirobot_image_generator),
        weight_function=ConstantWeightFunction(0.6),
        tags=["inspiration", "statement"],
        name="Inspirobot"),

    SlideGeneratorData(
        # slide_templates.generate_large_quote_slide(
        slide_generators.LarqeQuoteSlideGenerator.of(
            title_generator=NoneGenerator(),
            text_generator=generate_wikihow_bold_statement,
            background_image_generator=generate_full_screen_google_image),
        tags=["bold_statement", "statement"],
        name="Wikihow Bold Statement"),

    SlideGeneratorData(
        # slide_templates.generate_large_quote_slide(
        slide_generators.LarqeQuoteSlideGenerator.of(
            title_generator=NoneGenerator(),
            text_generator=goodreads_quote_generator,
            background_image_generator=generate_full_screen_google_image),
        weight_function=ConstantWeightFunction(0.6),
        tags=["quote", "statement"],
        name="Goodreads Quote"),

    SlideGeneratorData(
        # slide_templates.generate_large_quote_slide(
        slide_generators.LarqeQuoteSlideGenerator.of(
            title_generator=NoneGenerator(),
            text_generator=anecdote_prompt_generator,
            background_image_generator=generate_full_screen_google_image
        ),
        tags=["anecdote"],
        name="Anecdote")
]

# TWO CAPTIONS VARIATIONS
captioned_images_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide_tuple_caption(
        slide_generators.TwoColumnImageSlideGenerator.of_images_and_tupled_captions(
            default_or_no_title_generator,
            double_image_captions_generator,
            normal_or_weird_image_generator,
            combined_gif_generator),
        weight_function=ConstantWeightFunction(2),
        tags=["multi_caption", "two_captions", "gif"],
        name="Two Captions Gifs"),

    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide_tuple_caption(
        slide_generators.TwoColumnImageSlideGenerator.of_images_and_tupled_captions(
            default_or_no_title_generator,
            double_image_captions_generator,
            weird_reddit_image_generator,
            weird_punchline_image_generator),
        weight_function=ConstantWeightFunction(2),
        tags=["multi_caption", "two_captions", "reddit"],
        name="Two Captions Weird Reddit"),

    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide_tuple_caption(
        slide_generators.TwoColumnImageSlideGenerator.of_images_and_tupled_captions(
            default_or_no_title_generator,
            double_image_captions_generator,
            weird_punchline_image_generator,
            weird_punchline_image_generator),
        weight_function=ConstantWeightFunction(2),
        tags=["multi_caption", "two_captions", "reddit"],
        name="Two Captions Weird"),

    SlideGeneratorData(
        # slide_templates.generate_three_column_images_slide_tuple_caption(
        slide_generators.ThreeColumnImageSlideGenerator.of_images_and_tupled_captions(
            default_or_no_title_generator,
            triple_image_captions_generator,
            normal_or_weird_image_generator,
            weird_punchline_image_generator,
            weird_punchline_static_image_generator),
        weight_function=ConstantWeightFunction(1),
        allowed_repeated_elements=4,
        tags=["multi_caption", "three_captions", "reddit"],
        name="Three Captions Weird"),
]

# CHART GENERATORS
chart_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_full_image_slide(
        slide_generators.FullImageSlideGenerator.of(
            NoneGenerator(),
            reddit_chart_generator),
        weight_function=ConstantWeightFunction(4),
        allowed_repeated_elements=0,
        tags=["chart"],
        name="Reddit Chart"),

    SlideGeneratorData(
        # slide_templates.generate_chart_slide_tuple(
        slide_generators.ChartSlideGenerator(
            chart.generate_yes_no_pie
        ),
        retries=1,
        allowed_repeated_elements=4,
        weight_function=ConstantWeightFunction(2.5),
        tags=["pie_chart", "yes_no_chart", "chart"],
        name="Yes/No/Funny Chart"),

    SlideGeneratorData(
        # slide_templates.generate_chart_slide_tuple(
        slide_generators.ChartSlideGenerator(
            chart.generate_location_pie
        ),
        allowed_repeated_elements=4,
        retries=1,
        weight_function=ConstantWeightFunction(0.08),
        tags=["location_chart", "pie_chart", "chart"],
        name="Location Chart"),
    SlideGeneratorData(
        # slide_templates.generate_chart_slide_tuple(
        slide_generators.ChartSlideGenerator(
            chart.generate_property_pie
        ),
        allowed_repeated_elements=4,
        retries=1,
        weight_function=ConstantWeightFunction(0.04),
        tags=["property_chart", "pie_chart", "chart"],
        name="Property Chart"),
    SlideGeneratorData(
        # slide_templates.generate_chart_slide_tuple(
        slide_generators.ChartSlideGenerator(
            chart.generate_correlation_curve
        ),
        allowed_repeated_elements=4,
        retries=1,
        weight_function=ConstantWeightFunction(0.5),
        tags=["curve", "chart"],
        name="Correlation Curve"),
]

# CONCLUSIONS
conclusion_slide_generators = [
    SlideGeneratorData(
        # slide_templates.generate_two_column_images_slide(
        slide_generators.TwoImagesAndTupledCaptions(
            conclusion_title_generator,
            conclusion_two_captions_tuple_generator,
            normal_image_generator,
            weird_reddit_image_generator,
        ),
        weight_function=PeakedWeight((-1,), 10000, 0),
        allowed_repeated_elements=10,
        tags=["conclusion"],
        name="2 Conclusions"),
    SlideGeneratorData(
        # slide_templates.generate_three_column_images_slide(
        slide_generators.ThreeImagesAndTupledCaptions(
            conclusion_title_generator,
            conclusion_three_captions_tuple_generator,
            normal_image_generator,
            weird_reddit_image_generator,
            combined_gif_generator,
        ),
        weight_function=PeakedWeight((-1,), 8000, 0),
        allowed_repeated_elements=10,
        tags=["conclusion"],
        name="3 Conclusions")
]

all_slide_generators = title_slide_generators + about_me_slide_generators + history_slide_generators + \
                       single_image_slide_generators + statement_slide_generators \
                       + captioned_images_slide_generators + chart_slide_generators + conclusion_slide_generators

default_max_allowed_tags = {
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
    "quote": 0.2,
    "statement": 0.2,
    "chart": 0.3
}

# ==================================
# =====  PRESENTATION SCHEMAS  =====
# ==================================


# This object holds all the information about how to generate the presentation
presentation_schema = PresentationSchema(
    # Basic powerpoint generator
    powerpoint_creator=powerpoint_slide_creator.create_new_powerpoint,
    # Topic per slide generator
    seed_generator=slide_topic_generators.SideTrackingTopicGenerator,

    # Slide generators
    slide_generators=all_slide_generators,
    # Max tags
    max_allowed_tags=default_max_allowed_tags,
)

# Interview schema: Disallow about_me slides
interview_max_allowed_tags = default_max_allowed_tags.copy()
interview_max_allowed_tags["about_me"] = 0

interview_schema = PresentationSchema(
    # Basic powerpoint generator
    powerpoint_creator=powerpoint_slide_creator.create_new_powerpoint,
    # Topic per slide generator
    seed_generator=slide_topic_generators.SideTrackingTopicGenerator,

    # Slide generators
    slide_generators=all_slide_generators,
    # Max tags
    max_allowed_tags=interview_max_allowed_tags,
)

# Test schema: for testing purposes

test_schema = PresentationSchema(
    # Basic powerpoint generator
    powerpoint_slide_creator.create_new_powerpoint,
    # Topic per slide generator
    # seed_generator=slide_topic_generators.SideTrackingTopicGenerator,
    seed_generator=slide_topic_generators.IdentityTopicGenerator,
    # Slide generators
    slide_generators=single_image_slide_generators,
    ignore_weights=True
)

schemas = {
    "default": presentation_schema,
    "interview": interview_schema,
    "test": test_schema
}


def get_schema(name):
    return schemas[name]
