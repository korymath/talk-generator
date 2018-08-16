
from functools import lru_cache
from os import listdir
from os.path import isfile, join

from google_images_download import google_images_download



# == CONTENT GENERATORS ==
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
            'print_urls': False,
            'exact_size': '1600,900',
        }
        # passing the arguments to the function
        paths_dict = response.download(arguments)
        for value in paths_dict.values():
            paths.extend(value)

        # printing absolute paths of the downloaded images
        # print('paths of images', paths)
    return paths


@lru_cache(maxsize=20)
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
