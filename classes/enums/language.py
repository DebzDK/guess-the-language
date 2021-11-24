"""Enum to represent languages and their codes"""
import re
from enum import Enum


class Language(Enum):
    """
    Enum type to represent all available target languages
    offered by the DeepL Translator API.

    ...

    Methods
    -------
    get_user_friendly_name(mode) -> str:
        Gets a user-friendly version of the language text
    """
    BULGARIAN = "BG"
    CZECH = "CZ"
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
