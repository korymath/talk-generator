
# FORMAT GENERATORS
# These are functions that get some inputs (texts, images...)
# and create layouted slides with these inputs

def create_title_slide(prs, title):
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title_object = slide.shapes.title
    title_object.text = title
    return slide


def create_text_slide(prs, text):
    # Get a default blank slide layout
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    title_object = slide.shapes.title
    title_object.text = text
    return slide


# Creates a slide with an image covering the whole slide
def create_image_slide(prs, image_url, title=False):
    return _create_single_image_slide(prs, image_url, 2, title)


# Creates a slide with an image covering the whole slide
def create_full_image_slide(prs, image_url, title=False):
    return _create_single_image_slide(prs, image_url, 11, title)


def _create_single_image_slide(prs, image_url, slide_template_idx, title=False):
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

    return False
