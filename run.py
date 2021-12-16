"""'Guess The Language' - A language-guessing game program

Author
----------
Deborah Dike

Usage
----------
To run the code, use:
    python3 run.py

which should allow a user to play the game and, at the end of the
program, output the total number of correct guesses.

The program can also be run by opening it in a version of Python
IDLE and pressing F5.

Note
----------
Further information can be found in the project's README file.
.. 'Guess The Language' project README:
    https://github.com/DebzDK/guess-the-language#guess-the-language

----------------------------------------------------------------------
"""
import os
import re
from typing import Any, Callable, Dict, Tuple, Union
import flag
from dotenv import load_dotenv
from prompt_toolkit import prompt as toolkit_prompt
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.completion import WordCompleter
from classes.enums.difficulty import Difficulty
from classes.enums.inputmode import InputMode
from classes.enums.language import Language
from classes.sentencegenerator import SentenceGenerator
from classes.helpers.translationhelper import TranslationHelper

NUM_OF_QS_PER_DIFFICULTY_LEVEL = [5, 5, 10, 26]
CHAR_LIMIT_PER_DIFFICULTY_LEVEL = [30, 30, 40, 20]
QUIT_COMMANDS = ["q", "quit"]
UNICODES = {
    "green": "\u001b[32;1m",
    "red": "\u001b[31;1m",
    "white-bg": "\u001b[30;47m",
    "underline": "\u001b\33[4m",
    "reset": "\u001b[37;0m"
}
GAMEPLAY_BINDINGS = KeyBindings()
MENU_NAVIGATION_BINDINGS = KeyBindings()
TITLE = """
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
 ________   __  __   _______   ______   ______
|  ______| | |  | | |  ___  | |  ____| |  ____|
| |  ____  | |  | | | |___| | | |____  | |____
| | |___ | | |  | | |  _____| |____  | |____  |
| |____| | | |__| | | |_____   ____| |  ____| |
|________| |______| |_______| |______| |______|
 _______   __  __   _______
|__   __| | |  | | |  ___  |
   | |    | |__| | | |___| |
   | |    |  __  | |  _____|
   | |    | |  | | | |_____
   |_|    |_|  |_| |_______|
 _       _______   ______   ________   __  __   _______   ________   _______
| |     |  ___  | |  __  | |  ______| | |  | | |  ___  | |  ______| |  ___  |
| |     | |   | | | |  | | | |  ____  | |  | | | |   | | | |  ____  | |___| |
| |     | |___| | | |  | | | | |___ | | |  | | | |___| | | | |___ | |  _____|
| |___  |   _   | | |  | | | |____| | | |__| | |   _   | | |____| | | |_____
|_____| |__| |__| |_|  |_| |________| |______| |__| |__| |________| |_______|

////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
"""
input_mode = InputMode.USER.value
difficulty_level = Difficulty.EASY.value
enable_hints = True

viewing_main_menu = True
viewing_game_options_menu = False
selected_main_menu_option_index = 0
main_menu_options = ["PLAY", "GAME OPTIONS", "QUIT"]
selected_game_option_index = 0
game_options = [
    "Input mode",
    "Difficulty",
    "Enable hints",
    "Return to main menu"
]
start_game = False


def display_title():
    """Prints title to terminal."""
    print(TITLE)


def display_main_menu():
    """Print main manu options to terminal."""
    global viewing_main_menu, viewing_game_options_menu

    viewing_main_menu = True
    viewing_game_options_menu = False
    text = ""
    for i, option in enumerate(main_menu_options):
        if i == selected_main_menu_option_index:
            text += f"{UNICODES['white-bg']}> {option} <{UNICODES['reset']}"
        else:
            text += f"> {option}"
        text += "\n"
    print(text)


def get_toolbar_text() -> str:
    """Get toolbar text.

    Displays the appropriate text depending on what the user is currently
    viewing, i.e. the main menu, the game options menu, or the game.

    Returns
    -------
    str
        The string that will display in the bottom toolbar.
    """
    global viewing_game_options_menu

    menu_default_text = "Press the UP and DOWN arrow keys to navigate the menu"

    if viewing_game_options_menu:
        return f"{menu_default_text}\nPress ENTER to toggle a game option"
    return menu_default_text


# Code from StackOverflow - https://stackoverflow.com/a/684344
def clear_terminal():
    """Clear the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')
    display_title()


def select_next_main_menu_option():
    """Select next main menu option.

    Updates the terminal to show the next menu option as the one
    that's selected.
    """
    global selected_main_menu_option_index

    if selected_main_menu_option_index == len(main_menu_options) - 1:
        clear_terminal()
        display_main_menu()
        return

    selected_main_menu_option_index += 1
    clear_terminal()
    display_main_menu()


def select_previous_main_menu_option():
    """Select previous main menu option.

    Updates the terminal to show the previous menu option as the one
    that's selected.
    """
    global selected_main_menu_option_index

    if selected_main_menu_option_index == 0:
        clear_terminal()
        display_main_menu()
        return

    selected_main_menu_option_index -= 1
    clear_terminal()
    display_main_menu()


def process_main_menu_selection():
    """Process main menu selection from user input.

    Checks if the key pressed corresponds to a main menu option and processes
    accordingly.

    Raises
    -------
    SystemExit
        If the user has entered a command to quit the game
    """
    global viewing_main_menu, viewing_game_options_menu, start_game

    if selected_main_menu_option_index == 0:
        clear_terminal()
        viewing_main_menu = False
        start_game = True
    elif selected_main_menu_option_index == 1:
        clear_terminal()
        viewing_main_menu = False
        display_game_options_menu()
    elif selected_main_menu_option_index == 2:
        raise SystemExit()


def display_game_options_menu():
    """Print game menu options to console."""
    global viewing_game_options_menu
    viewing_game_options_menu = True

    text = ""
    for i, option in enumerate(game_options):
        if i == selected_game_option_index:
            text += f"{UNICODES['white-bg']}> {option}"
            text += ": " if i != len(game_options) - 1 else ""
            text += f"{get_game_option_description(i)} <{UNICODES['reset']}"
        else:
            text += f"> {option}"
            text += ": " if i != len(game_options) - 1 else ""
            text += get_game_option_description(i)
        text += "\n"
    print(text)


def get_game_option_description(index: int) -> str:
    """Get the description for the currently selected game option.

    Parameters
    ----------
    index
        The index of the game option.

    Returns
    -------
    str
        The game options's description.
    """
    if index == 0:
        return InputMode.get_description(input_mode)

    if index == 1:
        return (
            Difficulty.get_description(difficulty_level) +
            " (" + Difficulty(difficulty_level).name + ")")

    if index == 2:
        return str(enable_hints)
    return ""


def select_next_game_option():
    """Select next game menu option.

    Updates the terminal to show the next menu option as the one
    that's selected.
    """
    global selected_game_option_index

    if selected_game_option_index == len(game_options) - 1:
        return

    selected_game_option_index += 1
    clear_terminal()
    display_game_options_menu()


def select_previous_game_option():
    """Select previous game option.

    Updates the terminal to show the previous game option as the one
    that's selected.
    """
    global selected_game_option_index

    if selected_game_option_index == 0:
        return

    selected_game_option_index -= 1
    clear_terminal()
    display_game_options_menu()


def process_game_option_selection():
    """Toggle game option based on user input and current settings.

    Checks if user input corresponds to a game option and processes
    accordingly.
    """
    global input_mode, difficulty_level, enable_hints

    if selected_game_option_index == 0:
        input_mode = input_mode + 1 if input_mode < 3 else 1
    elif selected_game_option_index == 1:
        difficulty_level = difficulty_level + 1 if difficulty_level < 3 else 0
    elif selected_game_option_index == 2:
        enable_hints = not enable_hints

    clear_terminal()

    if selected_game_option_index == 3:
        display_main_menu()
    else:
        display_game_options_menu()


def await_input(prompt: str, process: Callable[[str], Any] = None,
                update_terminal: Callable[[str], Any] = None):
    """Prompt user for input, process input if required
    and update the terminal or exit the loop as needed.

    Continuously waits for user input and executes functions based on input
    as required until the feedback loop is exited.

    Parameters
    ----------
    prompt
        The text to display to the user to indicate the desired type of input.
    process
        The function to call process user input.
    update_terminal
        The function to call to print changes made by calling process()
        to the terminal.
    """
    while True:
        user_input = toolkit_prompt(prompt)
        if process is not None:
            end_loop = process(user_input)
            if (end_loop is not True and
                    update_terminal is not None):
                clear_terminal()
                update_terminal()
            elif end_loop:
                break
        else:
            break


def get_processed_user_input(
        prompt: str, process: Callable[[str], Any],
        completer: WordCompleter = None) -> Union[str, None]:
    """Prompt user for input, process input if required and return the input.

    Continuously waits for user input and executes functions based on input
    as required until it can be returned.

    Parameters
    ----------
    prompt
        The text to display to the user to indicate the desired type of input.
    process
        The function to call process user input.
    completer
        The class holding the list of all values to use as autocomplete
        suggestions for the user.

    Returns
    -------
        Union[str, None]
            A string value if user input passes processing, otherwise None if
            the input loop should be exited and return nothing.
    """
    while True:
        user_input = toolkit_prompt(prompt, completer=completer)
        if process is not None:
            end_loop = process(user_input)
            if end_loop:
                return user_input
        else:
            return None


def run_game():
    """Run the game loop."""
    global input_mode, start_game
    num_of_questions_asked = 0
    num_of_correct_answers = 0
    character_limit = CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]
    all_languages = [lang.get_user_friendly_name() for lang in Language]
    language_completer = WordCompleter(all_languages, ignore_case=True)
    file_name = ""
    sentences_from_file = None
    sentence_to_translate = None
    translations = {}

    if input_mode == 2:
        print((
            "\nSince you've chosen to play with file input,"
            " please make sure that each sentence in your file"
            " is on a new line.\n"))
        file_name, sentences_from_file = read_from_file()

    while (not is_game_over(num_of_questions_asked) and
            ((input_mode != 2) or
                (input_mode == 2 and
                    num_of_questions_asked < len(sentences_from_file)))):
        print(
            f"\n{UNICODES['underline']}"
            f"Question {num_of_questions_asked + 1}{UNICODES['reset']}\n"
        )

        if input_mode == 1:
            sentence_to_translate = get_processed_user_input(
                (
                    "Enter a sentence"
                    f" (no longer than {character_limit} characters"
                    " long):\n"
                ),
                is_viable_for_translation
            )
        elif input_mode == 2:
            sentence_to_translate, is_viable = (
                sentences_from_file[num_of_questions_asked]
            )
            if not is_viable:
                sentence_to_translate = SentenceGenerator.generate_sentence(
                    CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level])
        elif input_mode == 3:
            sentence_to_translate = SentenceGenerator.generate_sentence(
                CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level])

        if input_mode != 1:
            print(sentence_to_translate)

        translation = TranslationHelper.translate_sentence(
                sentence_to_translate, difficulty_level,
                num_of_questions_asked == 0)

        if input_mode == 2:
            translations[sentence_to_translate] = translation

        if "Error: " in translation.text:
            print(f"{translation}\n")
            print("You will now be returned to the main menu...")
            print(
                "If it's a connection or HTTP issue, please try again."
                "\nOtherwise, please contact the developer to report a "
                "potential bug.\n"
            )
            return

        num_of_questions_asked += 1
        answer = translation.lang

        print(f"\nTranslation: {translation}\n")
        guess = get_processed_user_input(
            "What language is this?\n", is_valid_answer, language_completer)
        lower_case_guess = guess.lower()

        if lower_case_guess == answer.name.lower():
            result_indicator = UNICODES['green']
            num_of_correct_answers += 1
        else:
            result_indicator = UNICODES['red']

        print(
            f"\nYou guessed{result_indicator} {guess}"
            f"{UNICODES['reset']} and the answer is"
            f"{UNICODES['green']} {translation.lang.get_user_friendly_name()}"
            f" ({flag.flag(answer.get_language_abbreviation())})"
            f"{UNICODES['reset']}."
        )

    if num_of_correct_answers < (num_of_questions_asked / 2):
        extra_text = "..\nBetter luck next time"
    elif num_of_correct_answers == num_of_questions_asked:
        extra_text = "\nPerfect score"
    else:
        extra_text = "\nWell done"

    print(
        f"\nYou guessed {num_of_correct_answers}/{num_of_questions_asked}"
        f" languages correctly.{extra_text}!\n"
    )

    if input_mode == 2:
        write_to_file(file_name, sentences_from_file, translations)

    toolkit_prompt(
        "Press any key to return to the main menu",
        key_bindings=GAMEPLAY_BINDINGS
    )

    start_game = False


@GAMEPLAY_BINDINGS.add(Keys.Any)  # Key press listener (minus 'Enter' & arrows)
@MENU_NAVIGATION_BINDINGS.add(Keys.Any)
@GAMEPLAY_BINDINGS.add("enter")   # 'Enter' key press listener
def _(event: KeyPressEvent):
    """Clear terminal on any key press and display main menu.

    Parameters
    ----------
    event
        The key press event.
    """
    event.app.exit()
    run_in_terminal(clear_terminal)
    run_in_terminal(display_main_menu)


@MENU_NAVIGATION_BINDINGS.add("up")  # Up arrow key press listener
def _(event: KeyPressEvent):
    """Cycle up through menu options.

    Parameters
    ----------
    event
        The key press event.
    """
    global viewing_main_menu, viewing_game_options_menu

    event.app.exit()
    if viewing_main_menu:
        run_in_terminal(select_previous_main_menu_option)
    elif viewing_game_options_menu:
        run_in_terminal(select_previous_game_option)


@MENU_NAVIGATION_BINDINGS.add("down")  # Down arrow key press listener
def _(event: KeyPressEvent):
    """Cycle down through menu options.

    Parameters
    ----------
    event
        The key press event.
    """
    global viewing_main_menu, viewing_game_options_menu

    event.app.exit()
    if viewing_main_menu:
        run_in_terminal(select_next_main_menu_option)
    elif viewing_game_options_menu:
        run_in_terminal(select_next_game_option)


@MENU_NAVIGATION_BINDINGS.add("enter")   # 'Enter' key press listener
def _(event: KeyPressEvent):
    """Process selected menu option.

    Parameters
    ----------
    event
        The key press event.
    """
    global viewing_main_menu, viewing_game_options_menu

    event.app.exit()

    if viewing_main_menu:
        process_main_menu_selection()
    elif viewing_game_options_menu:
        process_game_option_selection()


@MENU_NAVIGATION_BINDINGS.add("c-c")   # 'Control-C' key press listener
def _(event: KeyPressEvent):
    """Exit the game.

    Parameters
    ----------
    event
        The key press event.
    """
    event.app.exit()
    raise SystemExit()


def read_from_file() -> Tuple[str, Tuple[str, bool]]:
    """Read lines from a file.

    Reads from file, line by line, and adds each line to sentences list
    if the line passes validation.

    Returns
    ----------
    Tuple[str, Tuple[str, bool]]
        A tuple containing the file_name and a populated tuple of strings
        paired with whether or not there are viable for translation, otherwise
        an empty one.
    """
    sentences = ()
    question_limit = NUM_OF_QS_PER_DIFFICULTY_LEVEL[difficulty_level]
    char_limit = CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]

    while len(sentences) == 0:
        path_or_filename = toolkit_prompt(
            "\nEnter the name or path of the file you wish to read from: ")
        try:
            with open(path_or_filename, encoding="utf-8") as file:
                for line in file:
                    stripped_line = line.strip()
                    if (stripped_line and
                            not is_inserted_file_sentence(stripped_line)):
                        sentences += (
                            (
                                stripped_line,
                                is_viable_for_translation(stripped_line)
                            ),
                        )

                    if len(sentences) == question_limit:
                        break

                while len(sentences) < question_limit:
                    sentences += (
                        (
                            SentenceGenerator.generate_sentence(char_limit),
                            is_viable_for_translation(stripped_line)
                        ),
                    )
        except FileNotFoundError:
            print("\nUh oh... Looks like that file doesn't exist.")
    return (path_or_filename, sentences)


def write_to_file(
        path_or_filename: str, original_values: Tuple[str, bool],
        content: Dict[str, str]):
    """Writes translations to a file.

    Overwrites file with original sentences and their translations.

    Parameters
    ----------
    file_name
        The path to or name of the file to write to.
    original_values
        The original file sentences paired with whether or not they were
        viable for translation.
    content
        The content to be written to the file.
    """
    char_limit = CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]
    print("\nWriting translations to file...")
    with open(path_or_filename, mode="w", encoding="utf-8") as file:
        index = 0
        for sentence, translation in content.items():
            file.write(f"{sentence}\n")
            file.write(f"Translation: {translation}\n")
            file.write(f"""Language: {
                translation.lang.get_user_friendly_name()}""")
            original_sentence, was_viable = original_values[index]
            if not was_viable:
                file.write(f"\nOriginal sentence: {original_sentence}")
                file.write("\nNote: Exceeded character limit for")
                file.write(f" {Difficulty(difficulty_level).name} level")
                file.write(f" ({char_limit} chars)")
                file.write(" so was replaced with an auto-generated sentence.")
            file.write("\n\n")
            index += 1

    print("All done!\n")


def is_viable_for_translation(user_input: str) -> bool:
    """Check if user input are viable for translation.

    Ensures that input adheres to the character limit for the current
    difficulty level in order for the chosen API's character limit to not be
    exceeded.
    .. A detailed explanation can be found in the project's README:
        https://github.com/DebzDK/guess-the-language#features

    Parameters
    ----------
    user_input
        The input given by a user.

    Returns
    ----------
    bool
        True if user input is viable for translation, otherwise False
    """
    user_input = user_input.strip()
    str_len = len(user_input)
    if (str_len == 0 or
            re.search("^[^A-Za-z0-9]+", user_input) or
            str_len > CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]):
        return False
    return True


def is_inserted_file_sentence(sentence) -> bool:
    """Checks if a given sentence starts with a preset value.

    Parameters
    ----------
    sentence
        The sentence to check.

    Returns
    ----------
    bool
        True if the sentence starts with a preset marker for file additions
        that are not part of the original file content, i.e. the sentence to
        translate.
    """
    if (sentence.startswith("Translation:") or
            sentence.startswith("Language:") or
            sentence.startswith("Note:")):
        return True
    return False


def is_valid_answer(user_input: str) -> bool:
    """Check if user input is a valid answer.

    Ensures that the user input isn't an empty string and that it's at
    least 2 characters, in case the use has entered a code representing
    a language.

    Returns
    ----------
    bool
        True if user input is not an empty string, otherwise False.
    """
    user_input = user_input.strip()
    return user_input and len(user_input) > 1


def is_game_over(question_count: int) -> bool:
    """Check if the game is over.

    Determines whether or not the game is over based on the game's
    difficulty level (easy, normal, hard or beast):
        - Easy and normal difficulty level = 5 questions
        - Hard difficulty level = 10 questions
        - BEAST difficulty level = 26 questions (all available languages in
            chosen API)

    A detailed explanation can be found at:
        https://github.com/DebzDK/guess-the-language#features

    Parameters
    ----------
    question_count
        The number of questions that have been asked so far in the game

    Returns
    ----------
    bool
        True if all questions have been asked
    """
    return question_count == NUM_OF_QS_PER_DIFFICULTY_LEVEL[difficulty_level]


def main():
    """Load environment variables and run display and game functions."""
    load_dotenv()
    display_title()
    display_main_menu()

    while True:
        while not start_game:
            toolkit_prompt(
                "", key_bindings=MENU_NAVIGATION_BINDINGS,
                bottom_toolbar=get_toolbar_text
            )

        run_game()


main()
