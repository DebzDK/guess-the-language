"""Class to help with translations."""
from os import environ as env
from typing import TypeVar
from datetime import date
import random
import json
import requests
from classes.translation import Translation
from classes.enums.language import Language
from classes.services.requestservice import RequestService

# Learned how to create generic types, like in Java,
# from https://docs.python.org/3/library/typing.html#generics
_T = TypeVar("T")


class TranslationHelper():
    """Class containing method to help with translations.

    Methods
    -------
    translate_sentence(
            text: str, use_all_languages: bool = False) -> Translation:
        Translates sentence into another language.
    """
    _language_choices = None

    @staticmethod
    def translate_sentence(
            text: str, difficulty_level: int,
            use_all_languages: bool = False) -> Translation:
        """Makes request for translation and return response.

        Returns
        -------
        Translation
            The translated sentence as a Translation object or an error
            parsed into a Translation object for later processing to show
            the user a useful message.
        """
        global _language_choices

        def create_translation_error(
                error: _T, target_language: Language) -> Translation:
            """Returns error wrapped in a Translation object.

            Returns
            -------
            Translation
                An error parsed into a Translation object for later processing
                to show the user a useful message.
            """
            return Translation((
                        "\nUh oh... We encountered the following issue:\n"
                        f"Error: {error}"),
                        target_language)

        def get_api_error_message(code: int, detailed_error: str) -> str:
            """Gets a user-friendly error message for the API error.

            Returns
            -------
            str
                The user-friendly representation of an API error.
            """
            if code == 403:
                return (f"FORBIDDEN ({code}) - Please ensure the DeepL "
                        "API key has been provided.")
            if code == 456:
                today = date.today()
                split_date = today.strftime("%Y %m").split()
                limit_refresh_date = date(
                    int(split_date[0]), int(split_date[1]) + 1, 16)
                return (f"LIMIT REACHED ({code}) - The monthly quota has been "
                        "reached.\nIt will reset on "
                        f"{limit_refresh_date.strftime('%B %d, %Y')}.")
            return detailed_error

        api_endpoint = "https://api-free.deepl.com/v2/translate"
        api_key = env.get("DEEPL_API_KEY", "NO_API_KEY_PROVIDED")

        if use_all_languages:
            _language_choices = Language.get_choices_for_difficulty_level(
                difficulty_level)
            if difficulty_level == 3:
                _language_choices.remove(Language.ENGLISH)

        target_language = random.choice(_language_choices)
        _language_choices.remove(target_language)
        params = {
            "auth_key": api_key,
            "text": text,
            "source_lang": "EN",
            "target_lang": target_language.value,
            "split_sentences": "0"
        }

        response = RequestService.make_get_request(api_endpoint, params)

        try:
            result = response.json()
            translation = result["translations"]
            return Translation(translation[0]["text"], target_language)
        except KeyError:
            return create_translation_error(result["message"], target_language)
        except json.decoder.JSONDecodeError as json_error:
            if api_key == "NO_API_KEY_PROVIDED":
                return create_translation_error(api_key, target_language)
            return create_translation_error(
                get_api_error_message(
                    response.status_code, json_error), target_language)
        except requests.RequestException as request_error:
            return create_translation_error(request_error, target_language)
