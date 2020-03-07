from typing import Callable

from util.generator_util import Generator


class ImageData:
    def __init__(self, image_url: str, source: str = None):
        self._image_url = image_url
        self._source = source

    def get_image_url(self):
        return self._image_url

    def get_source(self):
        return self._source


class ImageGenerator(Generator):
    def __call__(self, seed: str) -> ImageData:
        raise NotImplementedError("Not implemented image generator")


class UnsourcedImageGenerator(ImageGenerator):
    def __init__(self, image_url_generator: Callable[[str], str]):
        self._image_url_generator = image_url_generator

    def __call__(self, seed: str) -> ImageData:
        return ImageData(image_url=self._image_url_generator(seed))
