"""Class to represent a sentence"""
from typing import List
from classes.word import Word
from classes.enums.language import Language


class Sentence():
    """Super class for types of text to inherit from.

    Creates a new Sentence object from the given string.

    Attributes
    ----------
    _value: str
        The string of characters that make up sentence.
    _lang : Language
        The language the sentence is in.
    _parts : List[Word]
        The list of objects representing the sentences and its structure.
    _ending_punctuation: str
        The punctuation symbol to end sentence with.

    Methods
    -------
    translate() -> str:
        Translates sentence into another language.
    """
    def __init__(
            self, parts: List[Word], lang=Language.ENGLISH,
            ending_punctuation="."):
        """Initialise the object with the passed parameters.

        Parameters
        ----------
        parts
            The list of Words that make up the sentence.
        lang: Language
            The language that the sentence is in (defaults to English).
        ending_punctuation: str:
            The punctuation that ends the sentence.
        """
        self._lang = lang
        self._ending_punctuation = ending_punctuation
        self._parts = parts
        sentence = (' '.join([word.value for word in parts]) +
                    ending_punctuation)
        self._value = sentence

    def __str__(self) -> str:
        """Modify object string representation using when printing."""
        return self._value

    def __repr__(self):
        """Modify object string representation."""
        return ('<Sentence value: "%s" lang: %s>'
                % (self._value, self.lang))

    # Use of decorator to access _lang
    @property
    def lang(self):
        """Getter method for lang property"""
        return self._lang.get_user_friendly_name()

    # TODO: Create TranslationHelper class and complete this function
    def translate(self) -> str:
        """Returns a translation."""
        return self._value + " has been translated to: Bonjour!"

    # TODO: If time allows, implement Text-to-speech functionality using
    # gTTs (Google-Text-To-Speech) Python library
    # def read_aloud(self):
    #     """Plays audio equivalent of sentence"
