import random
import pathlib
import os.path
import inflect
import argparse
from os import listdir
from os.path import isfile, join

from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

from nltk.corpus import wordnet as wn
from py_thesaurus import Thesaurus
from google_images_download import google_images_download


# CONSTANTS
HEIGHT = 9
WIDTH = 16
LEFTMOST = Inches(0)
TOPMOST = Inches(0)
HEIGHT_IN = Inches(HEIGHT)
WIDTH_IN = Inches(WIDTH)

# One inch equates to 914400 EMUs 
INCHES_TO_EMU = 914400
# One centimeter is 360000 EMUs
CMS_TO_EMU = 360000


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
    print('{} synonyms for "{}"'.format(len(all_synonyms), word))
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

def get_title(synonyms):
    """Returns a template title from a source list."""
    print('******************************************')
    chosen_synonym = random.choice(synonyms)
    chosen_synonym_plural = inflect.engine().plural(chosen_synonym)
    synonym_templates = ['The Unexpected Benefits of {}',
                         'What Your Choice in {} Says About You',
                         'How to Get Rid of {}',
                         'Why {} Will Ruin Your Life',
                         'The Biggest Concerns About {}']
    chosen_template = random.choice(synonym_templates);
    return chosen_template.format(chosen_synonym_plural.title())


def get_images(synonyms, num_images, search_google_images=False):
    """Get images, first search locally then Google Image Search."""
    all_paths = {}
    if num_images > 0:    
        for word in synonyms:
            lp = 'downloads/' + word + '/'
            try:
                local_files = [lp+f for f in listdir(lp) if isfile(join(lp, f))]
                all_paths[word] = local_files
            except FileNotFoundError as e:
                all_paths[word] = []
                pass

            if len(all_paths[word]) > 0:
                print('{} local images on {} found'.format(len(all_paths[word]), 
                    word))
            # If no local images, search on Google Image Search
            if len(all_paths[word]) == 0 and search_google_images:
                # Get related images at 16x9 aspect ratio
                # TODO: add image filter for weird and NSFW stuff
                response = google_images_download.googleimagesdownload()
                arguments = {
                    'keywords': word,
                    'limit': num_images,
                    'print_urls': True,
                    'exact_size': '1600,900',
                    # 'size':'large',
                    # 'usage_rights':'labeled-for-noncommercial-reuse-with-modification'
                }
                # passing the arguments to the function
                paths = response.download(arguments)
                # printing absolute paths of the downloaded images
                print('paths of images', paths)
                # Add to main dictionary
                all_paths[word] = paths[word]
    return all_paths


def compile_presentation(args, all_paths, title, definitions, synonyms):
    """Compile the talk with the given source material."""
    prs = Presentation()
    # Set the height and width
    prs.slide_height = HEIGHT * INCHES_TO_EMU
    prs.slide_width = WIDTH * INCHES_TO_EMU
    # Get a default blank slide layout
    slide_layout = prs.slide_layouts[5]

    # Build an ordered list of slides for access
    slides = []

    # Add title slide
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slides.append(slide)
    title_object = slide.shapes.title
    title_object.text = title
    title_object.width = WIDTH_IN
    title_object.height = HEIGHT_IN
    title_object.left = LEFTMOST
    title_object.right = TOPMOST
    slide_idx_iter = 1

    # For each synonym 
    for word, path_list in all_paths.items():
        # print('Word: {}'.format(word))
        # For each image collected add a new slide
        for i in range(len(path_list)):
            print('***********************************')
            print('Adding slide: {}'.format(slide_idx_iter))
            slides.append(prs.slides.add_slide(slide_layout))
            # Get an image
            img_path = path_list[i]
            # Add the image to the slide.
            if img_path:
                pic = slides[slide_idx_iter].shapes.add_picture(img_path, 
                    LEFTMOST, TOPMOST, width=WIDTH_IN, height=HEIGHT_IN)
                # Add title to the slide
                shapes = slides[slide_idx_iter].shapes
                shapes.title.text = word
                # TODO: Add the text to the slide.
                slide_idx_iter += 1
    return prs, slides


def save_talk(args, prs):
    """Save the talk."""
    fp = './output/' + args.topic + '.pptx'
    # Create the parent folder if it doesn't exist
    pathlib.Path(os.path.dirname(fp)).mkdir(parents=True, exist_ok=True)
    prs.save(fp)
    print('Saved talk to {}'.format(fp))
    return True


def main(args):
    """Make a talk with the given topic."""
    # Print status details
    print('******************************************')
    print("Making {} slide talk on: {}".format(args.num_slides, args.topic))
    topic_string = args.topic

    # Get definitions
    definitions = get_definitions(topic_string)
    # Get relations
    relations = get_relations(topic_string)
    # Get synonyms
    synonyms = get_synonyms(topic_string)
    # Get a title
    title = get_title(synonyms)
    # For each synonym download num_images
    all_paths = get_images(synonyms, args.num_images)
    # Compile the presentation
    prs, slides = compile_presentation(args, 
                                       all_paths=all_paths, 
                                       title=title,
                                       definitions=definitions, 
                                       synonyms=synonyms)
    if save_talk(args, prs):
        print('Successfully built talk.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--topic', help="Topic of presentation.",
                        default='bagels', type=str)
    parser.add_argument('--num_images', help="Number of images per synonym.",
                        default=0, type=int)
    parser.add_argument('--num_slides', help="Number of slides to create.",
                        default=3, type=int)
    args = parser.parse_args()
    main(args)
