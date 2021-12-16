"""Class used to represent a translation"""
from classes.enums.language import Language


class Translation():
    """Class used to represent a translation.

    Creates a new Translation object.

    Attributes
    ----------
    _text : str
        The translation.
    _lang : Language
        The language the translation is in.
    """

    def __init__(self, text: str, lang: Language):
        """Initialises the object with the passed parameters.

        Parameters
        ----------
        text
            The translation.
        lang
            The language the translation is in.
        """
        self._text = text
        self._lang = lang

    def __str__(self):
        """Modifies object string representation using when printing"""
        return self._text

    def __repr__(self):
        """Modifies object string representation"""
        return (f"<Translation text: {self._text}"
                f"lang: {self._lang}>")

    # Use of decorator to access _text
    @property
    def text(self):
        """Getter method for text property"""
        return self._text

    # Use of decorator to access _lang
    @property
    def lang(self):
        """Getter method for lang property"""
        return self._lang
