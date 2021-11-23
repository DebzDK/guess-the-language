"""Class to help with translations."""
from os import environ as env
from typing import TypeVar
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
    translate_sentence(text: str) -> str:
        Translates sentence into another language.
    """

    @staticmethod
    def translate_sentence(text: str):
        """Make request for translation and returns response."""

        def create_translation_error(error: _T, target_language: Language):
            """Returns error wrapped as in a Translation object."""
            return Translation((
                        "\nUh oh... We encountered the following issue:\n"
                        f"Error: {error}"),
                        target_language)

        api_endpoint = "https://api-free.deepl.com/v2/translate"
        api_key = env.get("DEEPL_API_KEY", "NO_KEY_PROVIDED")
        target_language = random.choice(list(Language))
        params = {
            "auth_key": api_key,
            "text": text,
            "target_language": target_language.value
        }

        response = RequestService.make_get_request(api_endpoint, params)
        has_response = False

        while not has_response:
            try:
                result = response.json()
                translation_json = json.loads(result)
                return Translation(translation_json["text"], target_language)
            except json.decoder.JSONDecodeError as json_error:
                return create_translation_error(json_error, target_language)
            except requests.RequestException as request_error:
                return create_translation_error(request_error, target_language)
