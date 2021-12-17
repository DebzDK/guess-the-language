"""Enum to represent languages and their codes"""
import re
import random
from enum import Enum
from typing import List


class Language(Enum):
    """
    Enum type to represent all available target languages
    offered by the DeepL Translator API.

    ...

    Methods
    -------
    get_user_friendly_name() -> str:
        Gets a user-friendly version of the language text
    get_language_abbreviation() -> str:
        Gets a lanugage's abbreviation.
    get_choices_for_difficulty_level(
            difficulty_level: int) -> List["Language"]:
        Gets a list of all possible languages to translate sentences into for
        the current game's difficulty level.
    """
    BULGARIAN = "BG"
    CZECH = "CS"
    DANISH = "DA"
    GERMAN = "DE"
    GREEK = "EL"
    ENGLISH = "EN_GB"
    SPANISH = "ES"
    ESTONIAN = "ET"
    FINNISH = "FI"
    FRENCH = "FR"
    HUNGARIAN = "HU"
    ITALIAN = "IT"
    JAPANESE = "JA"
    LITHUANIAN = "LT"
    LATVIAN = "LV"
    DUTCH = "NL"
    POLISH = "PL"
    PORTUGUESE = "PT-PT"
    BRAZILIAN_PORTUGUESE = "PT-BR"
    ROMANIAN = "RO"
    RUSSIAN = "RU"
    SLOVAK = "SK"
    SLOVENIAN = "SL"
    SWEDISH = "SV"
    CHINESE = "ZH"

    def get_user_friendly_name(self) -> str:
        """Gets the name of language, e.g: ENGLISH --> English

        Returns
        ----------
        str
            The name of the language.
        """
        names = self.name.split("_")
        name = names[0].capitalize()
        for i in range(1, len(names)):
            name += f" {names[i].capitalize()}"
        return name

    def get_language_abbreviation(self) -> str:
        """Gets the abbreviation for language, e.g: PT-BR --> BR

        Returns
        ----------
        str
            The abbreviated form of a language's name.
        """
        abbreviated_lang_form = re.sub("[-_]", " ", self.value).split()
        return abbreviated_lang_form[-1]

    @staticmethod
    def get_choices_for_difficulty_level(
            difficulty_level: int) -> List["Language"]:
        """Gets list of possible language choices for a given difficulty level.

        Returns a list of all the possible languages that sentences can be
        translated into depending on the current games difficulty level.

        Returns
        ----------
        List[Language]
            A list of possible language choices for a given difficulty level.
        """
        # NORMAL
        if difficulty_level == 1:
            return [
                Language.CHINESE,
                Language.RUSSIAN,
                Language.BRAZILIAN_PORTUGUESE,
                Language.DUTCH,
                Language.SWEDISH
            ]
        # HARD
        if difficulty_level == 2:
            lesser_known_languages = [
                Language.GREEK,
                Language.POLISH,
                Language.DANISH,
                Language.FINNISH,
                Language.ROMANIAN,
                Language.CZECH,
                Language.HUNGARIAN
            ]
            languages_to_complete_set = random.sample(
                [
                    Language.LITHUANIAN,
                    Language.BULGARIAN,
                    Language.PORTUGUESE,
                    Language.ESTONIAN,
                    Language.LATVIAN,
                    Language.SLOVAK,
                    Language.SLOVENIAN
                ], k=3)

            lesser_known_languages.extend(languages_to_complete_set)
            return lesser_known_languages
        # BEAST
        if difficulty_level == 3:
            languages = list(Language)
            languages.remove(Language.ENGLISH)
            return languages
        # EASY (default)
        return [
            Language.FRENCH,
            Language.SPANISH,
            Language.ITALIAN,
            Language.GERMAN,
            Language.JAPANESE
        ]
