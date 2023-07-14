"""Class for convepip rting text to speech."""
import os
from threading import Timer
# import pygame
from playsound import playsound
from gtts import gTTS as text_to_speech, lang


class TextToSpeechService():
    """Class for converting text to speech.

    Methods
    -------
    play_audio_for_text(text: str, lang_code: str) -> bool
        Plays the audio for the given text and language.
    """

    @classmethod
    def play_audio_for_text(
            cls, text: str, lang_code: str):
        """Plays the audio file for the given text and language.

        Parameters
        ----------
        text
            The text to convert into speech.
        lang_code
            The language with which the text should be spoken.
        """

        if cls._has_language_in_library(lang_code):
            tld = "com.br" if lang_code == "br" else "com"
            file_name = "hint.mp3"

            file = text_to_speech(
                text=text,
                tld=tld,
                lang=lang_code
            )
            file.save(file_name)

            timer = Timer(2.0, cls._play_and_delete_audio, [file_name])
            timer.start()

    @staticmethod
    def _play_and_delete_audio(file_name: str):
        try:
            # pygame.mixer.init()
            # pygame.mixer.music.load(file_name)
            # pygame.mixer.music.play()
            # while pygame.mixer.music.get_busy():
            #     pygame.time.Clock().tick(5)
            # pygame.mixer.quit()
            playsound(file_name, block=False)
            os.remove(file_name)
            print("      Hopefully that helped!")
        except Exception as exc:
            print(f"Exception: {exc}")
            print(
                "      Oops! There was an issue playing the audio.\n"
                "      Hopefully the other hints were enough to help you!"
            )

    @staticmethod
    def _has_language_in_library(lang_code: str) -> bool:
        """Checks that the gTTs library has the given language available.

        Parameters
        ----------
        lang_code
            The language with which the text should be spoken.

        Returns
        -------
        bool
            Returns True if the library has the language listed, otherwise
            False.
        """

        if lang_code in lang.tts_langs() or lang_code == "br":
            return True
        return False

    @staticmethod
    def _format_file_path(path: str) -> str:
        """Fixes the path in order for the playsound function to work.

        Parameters
        ----------
        path
            The temp path to the file to be played.

        Returns
        -------
        str
            Returns the formatted file path.
        """

        new_path = ''

        for part in path.split('/'):
            if part != '':
                new_path += '//' + part

        return new_path
