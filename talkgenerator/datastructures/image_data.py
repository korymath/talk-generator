class ImageData:
    def __init__(self, image_url: str, source: str = None):
        self._original_image_url = image_url
        self._image_url = image_url
        self._source = source

    def get_image_url(self) -> str:
        return self._image_url

    def get_original_image_url(self) -> str:
        return self._original_image_url

    def set_local_image_url(self, image_url: str):
        """ Use this method when downloading image locally """
        self._image_url = image_url

    def get_source(self) -> str:
        return self._source

    def __str__(self):
        return (
            "ImageData("
            + self._original_image_url
            + (
                (", " + self._image_url)
                if self._original_image_url != self._image_url
                else ""
            )
            + ((", " + self._source) if self._source is not None else "")
            + ")"
        )

    def __repr__(self):
        return str(self)
