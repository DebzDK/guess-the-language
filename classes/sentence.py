"""Class to represent a sentence"""
from typing import List
from classes.word import Word


class Sentence():
    """Super class for types of text to inherit from.

    Creates a new Sentence object from the given string.

    Attributes
    ----------
    _value: str
        string of characters that make up sentence
    _lang : str
        language of sentence
    _parts : List[Word]
        list of objects representing the sentences and its structure
    _ending_punctuation: str
        punctuation symbol to end sentence with

    Methods
    -------
    translate() -> str:
        Translates sentence into another language
    """

    # Overrides __repr__ to modify string representation of the object
    # that contains all of its information
    def __repr__(self):
        return ('<Sentence value: "%s" lang: %s>'
                % (self._value, self._lang))

    # Overrides __str__ to modify 'informal' representation
    # (used when printing the object)
    def __str__(self) -> str:
        return self._value

    def __init__(
            self, parts: List[Word], lang='English',
            ending_punctuation="."):
        self._lang = lang
        self._ending_punctuation = ending_punctuation
        self._parts = parts
        sentence = (' '.join([word.value for word in parts]) +
                    ending_punctuation)
        self._value = sentence

    # TODO: Create TranslationHelper class and complete this function
    def translate(self) -> str:
        """Returns a translation"""
        return self._value + " has been translated to: Bonjour!"

    # TODO: If time allows, implement Text-to-speech functionality using
    # gTTs (Google-Text-To-Speech) Python library
    # def read_aloud(self):
    #     """Plays audio equivalent of sentence"
