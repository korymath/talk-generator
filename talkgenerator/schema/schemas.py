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

schemas = {
    "default": presentation_schema,
    "interview": interview_schema,
    "test": test_schema,
}


def get_schema(name):
    return schemas[name]
