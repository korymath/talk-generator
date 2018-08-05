from pptx import Presentation

# CONSTANTS
# HEIGHT = 9
# WIDTH = 16
# LEFTMOST = Inches(0)
# TOPMOST = Inches(0)
# HEIGHT_IN = Inches(HEIGHT)
# WIDTH_IN = Inches(WIDTH)

# One inch equates to 914400 EMUs
# INCHES_TO_EMU = 914400
# One centimeter is 360000 EMUs
# CMS_TO_EMU = 360000

# Location of powerpoint template
POWERPOINT_TEMPLATE_FILE = 'data/powerpoint/template.pptx'

# Layouts index in template
LAYOUT_TITLE_SLIDE = 0
LAYOUT_TITLE_AND_CONTENT = 1
LAYOUT_SECTION_HEADER = 2
LAYOUT_TWO_CONTENT = 3
LAYOUT_TWO_TITLE_AND_CONTENT = 4
LAYOUT_TITLE_ONLY = 5
LAYOUT_BLANK = 6
LAYOUT_CONTENT_CAPTION = 7
LAYOUT_PICTURE_CAPTION = 8
LAYOUT_FULL_PICTURE = 11


# FORMAT GENERATORS
# These are functions that get some inputs (texts, images...)
# and create layouted slides with these inputs

def create_new_powerpoint():
    return Presentation(POWERPOINT_TEMPLATE_FILE)


def create_title_slide(prs, title):
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE_SLIDE])
    title_object = slide.shapes.title
    title_object.text = title
    return slide


def create_text_slide(prs, text):
    # Get a default blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[LAYOUT_TITLE_ONLY])

    title_object = slide.shapes.title
    title_object.text = text
    return slide


# Creates a slide with an image covering the whole slide
def create_image_slide(prs, title=None, image_url=None):
    # TODO debug this: the image can not be set!
    return _create_single_image_slide(prs, title, image_url, LAYOUT_TITLE_AND_CONTENT)


# Creates a slide with an image covering the whole slide
def create_full_image_slide(prs, title=None, image_url=None):
    return _create_single_image_slide(prs, title, image_url, LAYOUT_FULL_PICTURE)


def _create_single_image_slide(prs, title, image_url, slide_template_idx):
    # Add image url as picture
    if image_url:
        # Get a default blank slide layout
        slide = prs.slides.add_slide(prs.slide_layouts[slide_template_idx])

        if title:
            title_object = slide.shapes.title
            title_object.text = title

        image_placeholder = slide.placeholders[1]
        image_placeholder.insert_picture(image_url)

        return slide


# GENERATORS: Same as the template fillers above, but using generation functions

def generate_full_image_slide(title_generator, image_generator):
    return lambda prs, seed: create_full_image_slide(prs, title_generator(seed), image_generator(seed))


def generate_image_slide(title_generator, image_generator):
    return lambda prs, seed: create_image_slide(prs, title_generator(seed), image_generator(seed))


def generate_title_slide(title_generator):
    return lambda prs, seed: create_title_slide(prs, title_generator(seed))
