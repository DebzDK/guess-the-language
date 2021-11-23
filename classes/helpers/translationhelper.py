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

_T = TypeVar("T")


class TranslationHelper():
    """Class containing method to help with translations.

    Methods
    -------
    translate_sentence(text: str) -> Translation:
        Translates sentence into another language.
    """

    @staticmethod
    def translate_sentence(text: str) -> Translation:
        """Make request for translation and returns response."""

        def create_translation_error(
                error: _T, target_language: Language) -> Translation:
            """Returns error wrapped as in a Translation object."""
            return Translation((
                        "\nUh oh... We encountered the following issue:\n"
                        f"Error: {error}"),
                        target_language)

        def get_api_error_message(code: int, detailed_error: str) -> str:
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
        language_choices = list(Language)
        language_choices.remove(Language.ENGLISH)
        target_language = random.choice(language_choices)
        params = {
            "auth_key": api_key,
            "text": text,
            "target_lang": target_language.value
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
