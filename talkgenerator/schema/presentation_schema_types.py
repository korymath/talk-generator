from schema.content_generators import *
from schema.slide_schemas import *
from talkgenerator.schema import slide_topic_generators
from talkgenerator.schema.presentation_schema import PresentationSchema
from talkgenerator.schema.slide_generator_data import ConstantWeightFunction
from talkgenerator.schema.slide_generator_data import PeakedWeight
from talkgenerator.schema.slide_generator_data import SlideGeneratorData
from talkgenerator.slide import powerpoint_slide_creator
from talkgenerator.slide import slide_generator_types

# ==================================
# =====  PRESENTATION SCHEMAS  =====
# ==================================


# This object holds all the information about how to generate the presentation
presentation_schema = PresentationSchema(
    # Basic powerpoint generator
    powerpoint_creator=powerpoint_slide_creator.create_new_powerpoint,
    # Topic per slide generator
    seed_generator=slide_topic_generators.SideTrackingTopicGenerator,
    # Title of the presentation
    title_generator=talk_title_generator,
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
    # Title of the presentation
    title_generator=talk_title_generator,
    # Slide generators
    slide_generators=all_slide_generators,
    # Max tags
    max_allowed_tags=interview_max_allowed_tags,
)

# Test schema: for testing purposes

test_schema = PresentationSchema(
    # Basic powerpoint generator
    powerpoint_slide_creator.create_new_powerpoint,
    # Title of the presentation
    title_generator=talk_title_generator,
    # Topic per slide generator
    # seed_generator=slide_topic_generators.SideTrackingTopicGenerator,
    seed_generator=slide_topic_generators.IdentityTopicGenerator,
    # Slide generators
    slide_generators=title_slide_generators
    + [
        SlideGeneratorData(
            # slide_templates.generate_image_slide(
            slide_generator_types.ImageSlideGenerator.of(
                inspiration_title_generator, generate_unsplash_image
            ),
            weight_function=ConstantWeightFunction(8),
            allowed_repeated_elements=10,
            name="Test sourcing",
        )
    ],
    # ignore_weights=True,
)

# TED schema: using only images from approved sources
ted_schema = PresentationSchema(
    # Basic powerpoint generator
    powerpoint_creator=powerpoint_slide_creator.create_new_powerpoint,
    # Topic per slide generator
    seed_generator=slide_topic_generators.SideTrackingTopicGenerator,
    # Title of the presentation
    title_generator=talk_title_generator,
    # Slide generators
    slide_generators=[
        SlideGeneratorData(
            slide_generator_types.TitleSlideGenerator.of(
                talk_title_generator_if_not_generated, talk_subtitle_generator
            ),
            allowed_repeated_elements=3,
            weight_function=PeakedWeight((0,), 100000, 0),
            tags=["title"],
            name="Title slide",
        )
    ],
    # Max tags
    max_allowed_tags={
        # Absolute maxima
        "title": 1,
        "about_me": 1,
        "history": 1,
        "anecdote": 1,
        "location_chart": 1,
        "chart": 1,
        "weird": 0,
        "meme": 0,
        # Relative (procentual) maxima
        "two_captions": 0.3,
        "three_captions": 0.2,
        "multi_captions": 0.3,
        "gif": 0.5,
        "quote": 0.2,
        "statement": 0.2,
    },
)

schemas = {
    "default": presentation_schema,
    "interview": interview_schema,
    "test": test_schema,
    "ted": ted_schema,
}


def get_schema(name):
    return schemas[name]
