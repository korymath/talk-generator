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
LAYOUT_TITLE_AND_PICTURE = 12


# HELPERS
def _create_slide(prs, slide_type):
    """ Creates a new slide in the given presentation using the slide_type template """
    return prs.slides.add_slide(prs.slide_layouts[slide_type])


def _add_title(slide, title):
    """ Adds the given title to the slide if the title is present"""
    if title:
        title_object = slide.shapes.title
        title_object.text = title


def _add_image(slide, placeholder_id, image_url, fit_image=True):
    placeholder = slide.placeholders[placeholder_id]
    if fit_image:
        pic = slide.shapes.add_picture(image_url, placeholder.left, placeholder.top)

        # calculate max width/height for target size
        ratio = min(placeholder.width / float(pic.width), placeholder.height / float(pic.height))

        pic.height = int(pic.height * ratio)
        pic.width = int(pic.width * ratio)

        pic.left = int(placeholder.left + ((placeholder.width - pic.width) / 2))
        pic.top = int(placeholder.top + ((placeholder.height - pic.height) / 2))

        placeholder = placeholder.element
        placeholder.getparent().remove(placeholder)
    else:
        placeholder.insert_picture(image_url)


# FORMAT GENERATORS
# These are functions that get some inputs (texts, images...)
# and create layouted slides with these inputs

def create_new_powerpoint():
    return Presentation(POWERPOINT_TEMPLATE_FILE)


def create_title_slide(prs, title):
    slide = _create_slide(prs, LAYOUT_TITLE_SLIDE)
    _add_title(slide, title)
    return slide


def create_text_slide(prs, text):
    # Get a default blank slide layout
    if bool(text):
        slide = _create_slide(prs, LAYOUT_TITLE_ONLY)

        _add_title(slide, text)
        return slide


def create_image_slide(prs, title=None, image_url=None):
    """ Creates a slide with an image covering the whole slide"""
    # TODO debug this: the image can not be set!
    return _create_single_image_slide(prs, title, image_url, LAYOUT_TITLE_AND_PICTURE, True)


def create_full_image_slide(prs, title=None, image_url=None):
    """ Creates a slide with an image covering the whole slide"""
    return _create_single_image_slide(prs, title, image_url, LAYOUT_FULL_PICTURE, False)


def _create_single_image_slide(prs, title, image_url, slide_template_idx, fit_image):
    # Add image url as picture
    if image_url:
        # Get a default blank slide layout
        slide = _create_slide(prs, slide_template_idx)
        _add_title(slide, title)
        _add_image(slide, 1, image_url, fit_image)
        return slide


# GENERATORS: Same as the template fillers above, but using generation functions

def generate_full_image_slide(title_generator, image_generator):
    return lambda prs, seed: create_full_image_slide(prs, title_generator(seed), image_generator(seed))


def generate_image_slide(title_generator, image_generator):
    return lambda prs, seed: create_image_slide(prs, title_generator(seed), image_generator(seed))


def generate_title_slide(title_generator):
    return lambda prs, seed: create_title_slide(prs, title_generator(seed))


def generate_text_slide(text_generator):
    return lambda prs, seed: create_text_slide(prs, text_generator(seed))
