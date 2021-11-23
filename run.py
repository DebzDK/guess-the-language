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
import re
from typing import Any, Callable, List, Union
from dotenv import load_dotenv
from classes.enums.inputmode import InputMode
from classes.enums.difficulty import Difficulty
from classes.sentencegenerator import SentenceGenerator
from classes.helpers.translationhelper import TranslationHelper

NUM_OF_QS_PER_DIFFICULTY_LEVEL = [5, 5, 10, 26]
CHAR_LIMIT_PER_DIFFICULTY_LEVEL = [30, 30, 40, 20]
QUIT_COMMANDS = ["q", "quit"]
UNICODES = {
    "green": "\u001b[32;1m",
    "red": "\u001b[31;1m",
    "underline": "\u001b\033[4m",
    "reset": "\u001b[37;0m"
}
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


def display_title():
    """Prints title to terminal."""
    print(TITLE)


def display_main_menu():
    """Print main manu options to terminal."""
    print("-- PLAY [1]")
    print("-- GAME OPTIONS [2]")
    print("-- QUIT [Q]")


def process_main_menu_selection(user_input: str):
    """Display game menu options according to user input.

    Checks if user input corresponds to a main menu option and processes
    accordingly.

    Parameters
    ----------
    user_input
        The value typed by the user.

    Raises
    -------
    SystemExit
        If the user has entered a command to quit the game
    """
    if user_input == "1":
        run_game()
    elif user_input == "2":
        display_game_options_menu()
        await_input("Select game option: ",
                    process_game_option,
                    display_game_options_menu)
    elif is_quit_command(user_input):
        raise SystemExit()


def display_game_options_menu():
    """Print game menu options to console."""
    game_options_str = (
        "---- Input mode [1]: {}\n"
        "---- Difficulty [2]: {}\n"
        "---- Enable hints [3]: {}\n"
        "-- Return to main menu [4]"
    )
    print(game_options_str.format(
                            InputMode.get_description(input_mode),
                            Difficulty.get_description(difficulty_level),
                            enable_hints))


def process_game_option(user_input: str):
    """Toggle game option based on user input and current settings.

    Checks if user input corresponds to a game option and processes
    accordingly.

    Parameters
    ----------
    user_input
        The value typed by the user.

    Returns
    -------
    bool
        True if the user has chosen to return to the main menu, otherwise
        False.
    """
    global input_mode, difficulty_level, enable_hints

    if user_input == "1":
        input_mode = input_mode + 1 if input_mode < 3 else 1
    elif user_input == "2":
        difficulty_level = difficulty_level + 1 if difficulty_level < 3 else 1
    elif user_input == "3":
        enable_hints = not enable_hints
    elif user_input == "4":
        display_main_menu()
        return True
    return False


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
        user_input = input(prompt)
        if process is not None:
            end_loop = process(user_input)
            if (end_loop is not True and
                    update_terminal is not None):
                update_terminal()
            elif end_loop:
                break
        else:
            break


def get_processed_user_input(
        prompt: str, process: Callable[[str], Any] = None) -> Union[str, None]:
    """Prompt user for input, process input if required and return the input.

    Continuously waits for user input and executes functions based on input
    as required until it can be returned.

    Parameters
    ----------
    prompt
        The text to display to the user to indicate the desired type of input.
    process
        The function to call process user input.

    Returns
    -------
        Union[str, None]
            A string value if user input passes processing, otherwise None if
            the input loop should be exited and return nothing.
    """
    while True:
        user_input = input(prompt)
        if process is not None:
            end_loop = process(user_input)
            if end_loop:
                return user_input
        else:
            return None


def run_game():
    """Run the game loop."""
    global input_mode
    num_of_questions_asked = 0
    num_of_correct_answers = 0
    character_limit = CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]
    sentences_from_file = None
    sentence_to_translate = None

    if input_mode == 2:
        print((
            "\nSince you've chosen to play with file input,"
            " please make sure that each sentence in your file"
            " is on a new line.\n"))
        sentences_from_file = read_from_file()

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
            sentence_to_translate = sentences_from_file[num_of_questions_asked]
        elif input_mode == 3:
            sentence_to_translate = SentenceGenerator.generate_sentence(
                CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level])

        if input_mode != 1:
            print(sentence_to_translate)

        translation = TranslationHelper.translate_sentence(
                sentence_to_translate)

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
            "What language is this?\n", is_valid_answer)
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
            f" ({answer.value}){UNICODES['reset']}."
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


def read_from_file() -> List[str]:
    """Read lines from a file.

    Reads from file, line by line, and adds each line to sentences list
    if the line passes validation.

    Returns
    ----------
    List[str]
        A populated list of strings if there are viable lines of text in a
        given file, otherwise an empty one.
    """
    sentences = []
    while len(sentences) == 0:
        path_or_filename = input(
            "\nEnter the name or path of the file you wish to read from: ")
        try:
            with open(path_or_filename, encoding="utf-8") as file:
                for line in file:
                    stripped_line = line.strip()
                    if (stripped_line and
                            is_viable_for_translation(stripped_line)):
                        sentences.append(stripped_line)

                    if (len(sentences) ==
                            NUM_OF_QS_PER_DIFFICULTY_LEVEL[difficulty_level]):
                        break
        except FileNotFoundError:
            print("\nUh oh... Looks like that file doesn't exist.")
    return sentences


def is_viable_for_translation(user_input) -> bool:
    """Check if user input are viable for translation.

    Ensures that input adheres to the character limit for the current
    difficulty level in order for the chosen API's character limit to not be
    exceeded.
    .. A detailed explanation can be found in the project's README:
        https://github.com/DebzDK/guess-the-language#features

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


def is_quit_command(user_input) -> bool:
    """Check if user has given a quit command.

    Determines whether or not the given input is one of the pre-set
    quit commands.

    Parameters
    ----------
    question_count
        The number of questions that have been asked so far in the game

    Returns
    ----------
    bool
        True if all questions have been asked
    """
    return user_input.lower() in QUIT_COMMANDS


def main():
    """Load environment variables and run display and game functions."""
    load_dotenv()
    display_title()
    display_main_menu()
    await_input("Select menu option: ", process_main_menu_selection)


main()
