"""Class used to represent a translation"""


class Translation():
    """Class used to represent a translation.

    Creates a new Translation object.

    Attributes
    ----------
    _text : str
        The translation.
    _lang : str
        The language the translation is in.
    """

    def __init__(self, text: str, lang: str):
        """Initialise the object with the passed parameters.

        Parameters
        ----------
        text
            The translation
        lang
            The language the translation is in
        """
        self._text = text
        self._lang = lang

    def __str__(self):
        """Modify object string representation using when printing"""
        return self._text

    def __repr__(self):
        """Modify object string representation"""
        return (f"<Translation text: {self._text}"
                f"lang: {self._lang}>")
