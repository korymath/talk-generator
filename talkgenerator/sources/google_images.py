from functools import lru_cache

from google_images_download import google_images_download

# == CONTENT GENERATORS ==
# These functions generate content, sometimes related to given arguments

_DEFAULT_NUM_IMAGES = 3

_FULL_SCREEN_ARGUMENTS = {
    'exact_size': '1600,900',
}

_WIDE_ARGUMENTS = {
    'size': '>1024*768',
    'aspect_ratio': 'wide',
}


def create_full_screen_image_generator(num_images=_DEFAULT_NUM_IMAGES):
    return lambda word: _search_full_screen(word, num_images)


@lru_cache(maxsize=20)
def _search_full_screen(word, num_images=_DEFAULT_NUM_IMAGES):
    return search_images(word, _FULL_SCREEN_ARGUMENTS, num_images)


def create_wide_image_generator(num_images=_DEFAULT_NUM_IMAGES):
    return lambda word: _search_wide(word, num_images)


@lru_cache(maxsize=20)
def _search_wide(word, num_images=_DEFAULT_NUM_IMAGES):
    return search_images(word, _WIDE_ARGUMENTS, num_images)


def create_image_generator(num_images=_DEFAULT_NUM_IMAGES):
    return lambda word: _search_normal_image(word, num_images)


@lru_cache(maxsize=20)
def _search_normal_image(word, num_images=_DEFAULT_NUM_IMAGES):
    return search_images(word, None, num_images)


def search_images(word, extra_arguments_dict=None, num_images=_DEFAULT_NUM_IMAGES):
    # Get related images at 16x9 aspect ratio
    response = google_images_download.googleimagesdownload()
    arguments = {
        'keywords': word,
        'limit': num_images,
        'print_urls': False,
        'print_paths': False,
        'output_directory': '../downloads/google_images/',
        'language': 'English',
        'safe_search': True,
        'no_numbering': True,
    }

    # Add more arguments
    if extra_arguments_dict is not None:
        arguments.update(extra_arguments_dict)

    # passing the arguments to the function
    paths_dict = response.download(arguments)
    paths = []
    for value in paths_dict.values():
        paths.extend(value)

    # printing absolute paths of the downloaded images
    return paths

# @lru_cache(maxsize=20)
# def _get_google_image_cached(word, num_image, lp):
#     try:
#         local_files = [lp + f for f in listdir(lp) if isfile(join(lp,
#                                                                   f))]
#         paths = local_files
#     except FileNotFoundError:
#         paths = []
#
#     if len(paths) > 0:
#         print('{} local images on {} found'.format(len(paths), word))
#
#     if len(paths) > num_image:
#         return paths
