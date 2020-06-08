class ImageData:
    def __init__(self, image_url: str, source: str = None):
        self._image_url = image_url
        self._source = source

    def get_image_url(self) -> str:
        return self._image_url

    def get_source(self) -> str:
        return self._source

    def __str__(self):
        return (
            "ImageData("
            + self._image_url
            + ((", " + self._source) if self._source is not None else "")
            + ")"
        )

    def __repr__(self):
        return str(self)
