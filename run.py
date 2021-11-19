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
from typing import Any, Callable, List
from inputmode import InputMode
from difficulty import Difficulty

NUM_OF_QS_PER_DIFFICULTY_LEVEL = [5, 5, 10, 26]
CHAR_LIMIT_PER_DIFFICULTY_LEVEL = [30, 30, 40, 20]
QUIT_COMMANDS = ["q", "quit"]
TITLE = """
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
 ________   __  __   _______   ______   ______
|  ______| | |  | | |  ___  | |  ____| |  ____|
| |  ____  | |  | | | |___| | | |____  | |____
| | |___ | | |  | | |  _____| |____  | |____  |
| |___ | | | |__| | | |_____   ____| |  ____| |
|________| |______| |_______| |______| |______|
 _______   __  __   _______
|__   __| | |  | | |  ___  |
   | |    | |__| | | |___| |
   | |    |  __  | |  _____|
   | |    | |  | | | |_____
   |_|    |_|  |_| |_______|
 _       _______   ______   ________   __  __   _______   ________   _______
| |     |  ___  | |      | |  ______| | |  | | |  ___  | |  ______| |  ___  |
| |     | |   | | |  __  | | |  ____  | |  | | | |   | | | |  ____  | |___| |
| |     | |___| | | |  | | | | |___ | | |  | | | |___| | | | |___ | |  _____|
| |___  |   _   | | |  | | | |___ | | | |__| | |   _   | | |___ | | | |_____
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
        start_game()
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
            stop_loop = process(user_input)
            if (stop_loop is not True and
                    update_terminal is not None):
                update_terminal()
            elif stop_loop:
                break
        else:
            break


def start_game():
    """Run the game loop."""
    global input_mode
    num_of_questions_asked = 0
    num_of_correct_answers = 0
    character_limit = CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]

    if input_mode == 2:
        print((
            "\nSince you've chosen to play with file input,"
            " please make sure that each sentence in your file"
            " is on a new line.\n"))
        sentences = read_from_file()

    while (not is_game_over(num_of_questions_asked) and
            ((input_mode != 2) or
                (input_mode == 2 and
                    num_of_questions_asked < len(sentences)))):
        print(f'\nQuestion {num_of_questions_asked + 1}\n')

        if input_mode == 1:
            await_input(
                (
                    "Enter a sentence"
                    f" (no longer than {character_limit} characters"
                    " long):\n"
                ),
                is_viable_for_translation
            )
        elif input_mode == 2:
            print(sentences[num_of_questions_asked])
            num_of_questions_asked += 1
        else:
            break

    print(
        (
            f"\nYou guessed {num_of_correct_answers}/{num_of_questions_asked}"
            " languages correctly..."
            "\nBetter luck next time.\n"
        )
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
            with open(path_or_filename) as file:
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
    """Run display and game functions."""
    display_title()
    display_main_menu()
    await_input("Select menu option: ", process_main_menu_selection)


main()
