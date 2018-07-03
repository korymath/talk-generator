import argparse


from pptx import Presentation
from pptx.util import Inches

from nltk.corpus import wordnet as wn
from py_thesaurus import Thesaurus
from PyDictionary import PyDictionary
from google_images_download import google_images_download


# One inch equates to 914400 EMUs 
inches_to_emu = 914400
# One centimeter is 360000 EMUs
cms_to_emu = 360000


def main(args):
  """Make a presentation with the given topic."""

  print('Topic: {}'.format(args.topic))
  
  # Get definition
  dictionary = PyDictionary()
  definitions = dictionary.meaning(args.topic)
  
  if definitions:
    print('{} definition(s)'.format(len(definitions)))
    for word_type,word_type_defs in definitions.items():
      print('As a {}, {} can mean: '.format(word_type, args.topic))
      for word_type_def in word_type_defs:
        print(word_type_def)
  else:
    print('No definition found.')

  # Get N synonyms
  for ss in wn.synsets(args.topic):
    print(ss.name(), ss.lemma_names())

  # Get related images at 16x9 aspect ratio
  response = google_images_download.googleimagesdownload()   #class instantiation

  arguments = {
    'keywords':args.topic,
    'limit':3,
    'print_urls':True,
    'exact_size':'1600,900',
    # 'size':'large',
    # 'usage_rights':'labeled-for-noncommercial-reuse-with-modification'
  }

  #passing the arguments to the function
  paths = response.download(arguments)
  #printing absolute paths of the downloaded images
  print(paths)   

  # Make a presentation
  prs = Presentation()
  
  # Get a default blank slide layout
  blank_slide_layout = prs.slide_layouts[6]

  # Set the heigh and width
  prs.slide_height = 9 * inches_to_emu
  prs.slide_width = 16 * inches_to_emu

  
  
  slides = []
  
  # Make slide 1, introducing the topic
  slides.append(prs.slides.add_slide(blank_slide_layout))
  
  # Make slide 2, expanding on a word from slide 1
  slides.append(prs.slides.add_slide(blank_slide_layout))
  
  # Make slide 3 connecting words from slide 1 and 2
  slides.append(prs.slides.add_slide(blank_slide_layout))

  left = top = Inches(1)
  pic = slide.shapes.add_picture(img_path, left, top)

  left = Inches(2)
  height = Inches(2.5)
  pic = slide.shapes.add_picture(img_path, left, top, height=height)

  # Save the presentation
  prs.save('output/' + args.output)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('--output', help="Output filename.", 
    default='test.pptx', type=str)
  parser.add_argument('--topic', help="Topic of presentation.", 
    default='bagels', type=str)
  args = parser.parse_args()
  main(args)



  