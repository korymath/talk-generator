from functools import lru_cache

from google_images_download import google_images_download

# == CONTENT GENERATORS ==
# These functions generate content, sometimes related to given arguments

_DEFAULT_NUM_IMAGES = 3

_FULL_SCREEN_ARGUMENTS = {"exact_size": "1600,900"}

_WIDE_ARGUMENTS = {"size": ">1024*768", "aspect_ratio": "wide"}


@lru_cache(maxsize=20)
def _search_full_screen(word, num_images=_DEFAULT_NUM_IMAGES):
    return search_images(word, _FULL_SCREEN_ARGUMENTS, num_images)


@lru_cache(maxsize=20)
def _search_wide(word, num_images=_DEFAULT_NUM_IMAGES):
    return search_images(word, _WIDE_ARGUMENTS, num_images)


class FullImageGenerator(object):
    def __init__(self, num_images=_DEFAULT_NUM_IMAGES):
        self._num_images = num_images

    def __call__(self, word):
        return _search_full_screen(word, self._num_images)


class WideImageGenerator(object):
    def __init__(self, num_images=_DEFAULT_NUM_IMAGES):
        self._num_images = num_images

    def __call__(self, word):
        return _search_wide(word, self._num_images)


class ImageGenerator(object):
    def __init__(self, num_images=_DEFAULT_NUM_IMAGES):
        self._num_images = num_images

    def __call__(self, word):
        return _search_normal_image(word, self._num_images)


@lru_cache(maxsize=20)
def _search_normal_image(word, num_images=_DEFAULT_NUM_IMAGES):
    return search_images(word, None, num_images)


def search_images(word, extra_arguments_dict=None, num_images=_DEFAULT_NUM_IMAGES):
    # Get related images at 16x9 aspect ratio
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords": word,
        "limit": num_images,
        "print_urls": False,
        "print_paths": False,
        "print_size": False,
        "output_directory": "downloads/google_images/",
        "language": "English",
        "safe_search": True,
        "no_numbering": True,
        "silent_mode": True,
    }

    # Add more arguments
    if extra_arguments_dict is not None:
        arguments.update(extra_arguments_dict)

    # passing the arguments to the function
    downloaded = response.download(arguments)
    if isinstance(downloaded, dict):
        return downloaded[word]
    else:
        paths_dict = downloaded[0]
        paths = []
        for value in paths_dict.values():
            paths.extend(value)

        # return absolute paths of the downloaded images
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
