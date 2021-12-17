"""'Guess The Language' - A language-guessing game program

Author
------
Deborah Dike

Usage
-----
To run the code, use:
    python3 run.py

which should allow a user to play the game and, at the end of the
program, output the total number of correct guesses.

The program can also be run by opening it in a version of Python
IDLE and pressing F5.

Note
----
* Further information can be found in the project's README file.
.. 'Guess The Language' project README:
    https://github.com/DebzDK/guess-the-language#guess-the-language

* # region comments are present to better separate code by their
concerns in order to navigate through the code.
----------------------------------------------------------------------
"""
import os
import re
from threading import Timer
from typing import Any, Callable, Dict, Tuple
import flag
from dotenv import load_dotenv
from prompt_toolkit import prompt as toolkit_prompt
from prompt_toolkit.application import get_app
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.filters import Condition
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.completion import WordCompleter
from classes.translation import Translation
from classes.enums.difficulty import Difficulty
from classes.enums.inputmode import InputMode
from classes.enums.language import Language
from classes.helpers.translationhelper import TranslationHelper
from classes.services.hintservice import HintService
from classes.sentencegenerator import SentenceGenerator

# region Constants
NUM_OF_QS_PER_DIFFICULTY_LEVEL = [5, 5, 10, 24]
CHAR_LIMIT_PER_DIFFICULTY_LEVEL = [30, 30, 40, 20]
ALL_LANGUAGES = [lang.get_user_friendly_name() for lang in Language]
LANGUAGE_COMPLETER = WordCompleter(ALL_LANGUAGES, ignore_case=True)
MAIN_MENU_OPTIONS = ["PLAY", "GAME OPTIONS", "QUIT"]
GAME_OPTIONS = [
    "Input mode",
    "Difficulty",
    "Enable hints",
    "Return to main menu"
]
# ..Found thanks to StackOverflow:
#   https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
UNICODES = {
    "green": "\u001b[32;1m",
    "red": "\u001b[31;1m",
    "white-bg": "\u001b[30;47m",
    "underline": "\u001b\33[4m",
    "reset": "\u001b[37;0m"
}
GAMEPLAY_BINDINGS = KeyBindings()
END_GAME_BINDINGS = KeyBindings()
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
# endregion
# region Globals
input_mode = InputMode.USER.value
difficulty_level = Difficulty.EASY.value
enable_hints = True
hints_used = 0

viewing_main_menu = True
viewing_game_options_menu = False
selected_main_menu_option_index = 0
selected_game_option_index = 0
is_playing_game = False
answer_to_current_question = None
# endregion


# region Display functions
def display_title():
    """Prints title to terminal."""
    print(TITLE)


def display_main_menu():
    """Prints main manu options to terminal."""
    global viewing_main_menu, viewing_game_options_menu

    viewing_main_menu = True
    viewing_game_options_menu = False
    text = ""
    for i, option in enumerate(MAIN_MENU_OPTIONS):
        if i == selected_main_menu_option_index:
            text += f"{UNICODES['white-bg']}> {option} <{UNICODES['reset']}"
        else:
            text += f"> {option}"
        text += "\n"
    print(text)


def display_hint():
    """Displays a hint to the user and increments number of hints used.

    Prints out a hint for the answer to the current question and increments
    the counter variable for number of hints used.
    """
    global answer_to_current_question, hints_used
    hint = HintService.get_next_hint(answer_to_current_question, hints_used)
    print(f"Hint: {hint}")
    increment_hints_used_count()


def display_time_up_message():
    """Displays time up message."""
    print("\nTime's up!")


def display_error_message(error: Translation):
    """Displays an informative error message.

    Parameters
    ----------
    error
        The error in the form of a Translation object.
    """
    print(
        f"{error}\n"
        "You will now be returned to the main menu..."
        "If it's a connection or HTTP issue, please try again."
        "\nOtherwise, please contact the developer to report a "
        "potential bug.\n"
    )


def display_end_of_game_message(
        num_of_correct_answers: int, num_of_questions_asked: int):
    """Displays a message to signal the end of the game.

    Prints out how many questions the user answered correctly along with
    an encouraging statement.

    Parameters
    ----------
    num_of_correct_answers
        The number of questions the user answered correctly.
    num_of_questions_asked
        The number of questions asked during the game.
    """
    extra_text = ""
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


def get_toolbar_text() -> str:
    """Gets toolbar text.

    Displays the appropriate text depending on what the user is currently
    viewing, i.e. the main menu, the game options menu, or the game.

    Returns
    -------
    str
        The string that will display in the bottom toolbar.
    """
    global viewing_game_options_menu, is_playing_game

    menu_default_text = "Press the UP and DOWN arrow keys to navigate the menu"

    if viewing_game_options_menu:
        return f"{menu_default_text}\nPress ENTER to toggle a game option"
    if is_playing_game:
        return (
            "Press CTRL+H for hints (if enabled)\n"
            "Press CTRL+C at any time to quit the game"
        )
    return menu_default_text


def clear_terminal():
    """Clears the terminal."""
    # Line of code from StackOverflow - https://stackoverflow.com/a/684344
    os.system('cls' if os.name == 'nt' else 'clear')
    display_title()


def select_next_main_menu_option():
    """Selects the next main menu option.

    Updates the terminal to show the next menu option as the one
    that's selected.
    """
    global selected_main_menu_option_index

    if selected_main_menu_option_index == len(MAIN_MENU_OPTIONS) - 1:
        clear_terminal()
        display_main_menu()
        return

    selected_main_menu_option_index += 1
    clear_terminal()
    display_main_menu()


def select_previous_main_menu_option():
    """Selects the previous main menu option.

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
    """Processes the main menu option based on user selection.

    Checks if the key pressed corresponds to a main menu option and processes
    accordingly.

    Raises
    -------
    SystemExit
        If the user has entered a command to quit the game
    """
    global viewing_main_menu, viewing_game_options_menu, is_playing_game

    if selected_main_menu_option_index == 0:
        clear_terminal()
        viewing_main_menu = False
        is_playing_game = True
    elif selected_main_menu_option_index == 1:
        clear_terminal()
        viewing_main_menu = False
        display_game_options_menu()
    elif selected_main_menu_option_index == 2:
        quit_game()


def display_game_options_menu():
    """Prints game menu options to console."""
    global viewing_game_options_menu
    viewing_game_options_menu = True

    text = ""
    for i, option in enumerate(GAME_OPTIONS):
        if i == selected_game_option_index:
            text += f"{UNICODES['white-bg']}> {option}"
            text += ": " if i != len(GAME_OPTIONS) - 1 else ""
            text += f"{get_game_option_description(i)} <{UNICODES['reset']}"
        else:
            text += f"> {option}"
            text += ": " if i != len(GAME_OPTIONS) - 1 else ""
            text += get_game_option_description(i)
        text += "\n"
    print(text)


def get_game_option_description(index: int) -> str:
    """Gets the description for the currently selected game option.

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
        hint_message = str(enable_hints)
        if difficulty_level == 3 and enable_hints:
            hint_message += " (Ignored - No hints for BEAST level)"
        return hint_message
    return ""


def select_next_game_option():
    """Selects the next game menu option.

    Updates the terminal to show the next menu option as the one
    that's selected.
    """
    global selected_game_option_index

    if selected_game_option_index == len(GAME_OPTIONS) - 1:
        return

    selected_game_option_index += 1
    clear_terminal()
    display_game_options_menu()


def select_previous_game_option():
    """Selects the previous game option.

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
    """Toggles the game option based on user input and current settings.

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
# endregion


# region Gameplay functions
def end_prompt():
    """Ends prompt for user input.

    Exits prompt after 5 seconds.
    """
    if difficulty_level == 3:
        display_time_up_message()

    try:
        get_app().exit()
    except Exception:  # Not best practice but this is what the library throws
        pass


def get_processed_user_input(
        prompt: str, process: Callable[[str], Any],
        completer: WordCompleter = None,
        set_timer: bool = False) -> str:
    """Prompts user for input, process input if required and return the input.

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
    set_timer
        True if playing with BEAST level difficulty, otherwise
        False by default.

    Returns
    -------
        str
            A string value if user input passes processing, otherwise an empty
            string if the input loop should be exited and return nothing.
    """
    user_input = ""
    timer = None
    while True:
        if set_timer:
            print("You have 5 seconds to answer: ")
            # Learned how to achieve similar effect as JavaScript's timeout
            # function thanks to StackOverflow.
            # Link is in README due to length of link:
            #   https://github.com/DebzDK/guess-the-language#languages-and-technologies-used
            timer = Timer(5.0, end_prompt)
            timer.start()

        user_input = toolkit_prompt(
            prompt,
            completer=completer,
            key_bindings=GAMEPLAY_BINDINGS,
            bottom_toolbar=get_toolbar_text) or ""

        if timer:
            timer.cancel()

        if process is not None:
            end_loop = process(user_input)
            if end_loop or set_timer:
                return user_input
        else:
            return user_input


def ask_question():
    """Prints the question."""
    print("What language is this?")


def get_user_answer() -> str:
    """Gets the answer from the user.

    Returns
    -------
    str
        The value that the user has provided as the answer.
    """
    guess = get_processed_user_input(
        "", is_valid_answer, LANGUAGE_COMPLETER, difficulty_level == 3)
    return guess


def increment_hints_used_count():
    """Increments the number of hints used."""
    global hints_used

    hints_used += 1


def end_question(guess: str, answer: Language):
    """Ends question by printing a statemtn to inform the user as to whether
    they were right or not.

    Parameters
    ----------
    guess
        The value the user provided as input.
    answer
        The correct answer.
    """
    if is_correct_guess(guess, answer):
        result_indicator = UNICODES['green']
    else:
        result_indicator = UNICODES['red']

    guess_statement = ""
    answer_statement = ""

    if guess:
        guess_statement = f"\nYou guessed{result_indicator} {guess}"
        answer_statement = f"{UNICODES['reset']} and the answer is"
    else:
        answer_statement = "The answer is"

    print(
        f"{guess_statement}{answer_statement}"
        f"{UNICODES['green']} {answer.get_user_friendly_name()}"
        f" ({flag.flag(answer.get_language_abbreviation())})"
        f"{UNICODES['reset']}."
    )


def read_from_file() -> Tuple[str, Tuple[str, bool]]:
    """Reads lines from a file.

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

    print((
        "\nSince you've chosen to play with file input,"
        " please make sure that each sentence\n in your file"
        " is on a new line.\n"))

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


def write_translations_to_file(
        path_or_filename: str, original_values: Tuple[str, bool],
        content: Dict[str, str]):
    """Writes translations to a file.

    Overwrites file with original sentences and their translations,
    adding an appropriate note if a sentence had to be replaced with an
    auto-generated one.

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


def get_sentence_for_translation(
        file_sentences: Tuple[str, bool],
        num_of_questions_asked: int) -> str:
    """Gets sentence for translation.

    Parameters
    ----------
    file_sentences
        The sentences extracted from file (only for file input game mode).
    num_of_questions_asked
        The number of questions asked in the game so far.

    Returns
    -------
    str
        The sentence for translation.
    """
    global input_mode, difficulty_level

    sentence_to_translate = ""
    if input_mode == 1:
        char_limit = CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]
        sentence_to_translate = get_processed_user_input(
            (
                "Enter a sentence"
                f" (no longer than {char_limit} characters"
                " long and has more than one word):\n"
            ),
            is_viable_for_translation
        )
    else:
        is_viable = None
        if input_mode == 2:
            sentence_to_translate, is_viable = (
                file_sentences[num_of_questions_asked]
            )
        if (not is_viable and is_viable is not None) or input_mode == 3:
            sentence_to_translate = SentenceGenerator.generate_sentence(
                CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level])
    return sentence_to_translate


def run_game():
    """Runs the game loop."""
    global input_mode, is_playing_game, answer_to_current_question, hints_used

    num_of_questions_asked = 0
    num_of_correct_answers = 0
    file_name = ""
    file_sentences = None
    sentence_to_translate = None
    translations = {}

    if input_mode == 2:
        file_name, file_sentences = read_from_file()

    while (check_if_game_can_continue(
            num_of_questions_asked, file_sentences)):
        hints_used = 0
        print(
            f"\n{UNICODES['underline']}"
            f"Question {num_of_questions_asked + 1}{UNICODES['reset']}\n"
        )

        sentence_to_translate = get_sentence_for_translation(
            file_sentences, num_of_questions_asked)

        if input_mode != 1:
            print(sentence_to_translate)

        translation = TranslationHelper.translate_sentence(
                sentence_to_translate, difficulty_level,
                num_of_questions_asked == 0)

        answer_to_current_question = translation.lang.value

        if input_mode == 2:
            translations[sentence_to_translate] = translation

        if "Error: " in translation.text:
            display_error_message(translation)
            end_game()
            return

        num_of_questions_asked += 1

        print(f"\nTranslation: {translation}\n")
        ask_question()
        guess = get_user_answer()

        if is_correct_guess(guess, translation.lang):
            num_of_correct_answers += 1

        end_question(guess, translation.lang)
        answer_to_current_question = None

    display_end_of_game_message(num_of_correct_answers, num_of_questions_asked)

    if input_mode == 2:
        write_translations_to_file(file_name, file_sentences, translations)

    end_game()


def end_game():
    """Ends the game."""
    global is_playing_game
    toolkit_prompt(
        "Press any key to return to the main menu",
        key_bindings=END_GAME_BINDINGS
    )
    is_playing_game = False


def quit_game():
    """Quits the game."""
    print("Thank you for playing!\n")
    raise SystemExit()
# endregion


# region Key press conditions
# Decorator from prompt-toolkit library
@Condition
def can_get_hint() -> bool:
    """Checks if hints are enabled.

    Returns
    -------
    bool
        Returns True if hints are enabled, otherwise False.
    """
    return (
        difficulty_level != 3 and
        is_playing_game and
        enable_hints and answer_to_current_question is not None)
# endregion


# region Key press listeners
# ..As described in prompt-toolkit documentation:
#   https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html
@MENU_NAVIGATION_BINDINGS.add(Keys.Any)  # All keys except enter and arrows
@END_GAME_BINDINGS.add(Keys.Any)  # End game listener
@END_GAME_BINDINGS.add("enter")   # 'Enter' key press listener
def _(event: KeyPressEvent):
    """Clears terminal on any key press and display main menu.

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
    """Cycles up through menu options.

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
    """Cycles down through menu options.

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
    """Processes the selected menu option.

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


@MENU_NAVIGATION_BINDINGS.add("c-c")   # 'CTRL+C' key press listener for menu
def _(event: KeyPressEvent):
    """Quits the game.

    Parameters
    ----------
    event
        The key press event.
    """
    event.app.exit()
    run_in_terminal(quit_game)


# 'CTRL+H' key press listener for hints
@GAMEPLAY_BINDINGS.add("c-h", filter=can_get_hint)
def _(event: KeyPressEvent):
    """Gets the next hint for language.

    Parameters
    ----------
    event
        The key press event.
    """
    event.app.exit()
    run_in_terminal(display_hint)
# endregion


# region Validation functions
def check_if_game_can_continue(
        num_of_questions_asked: int,
        file_sentences: Tuple[str, bool]) -> bool:
    """Checks if the game can continue.

    Returns
    -------
    bool
        Returns True is the game can continue, otherwise False.
    """
    global input_mode
    return (not is_game_over(num_of_questions_asked) and
            ((input_mode != 2) or
                (input_mode == 2 and
                    num_of_questions_asked < len(file_sentences))))


def is_correct_guess(guess: str, answer: Language) -> bool:
    """Checks if the guess is correct.

    Returns
    -------
    bool
        Returns True if the guess matches the answer, otherwise False.
    """
    return guess.lower() == answer.name.lower()


def is_game_over(question_count: int) -> bool:
    """Checks if the game is over.

    Determines whether or not the game is over based on the game's
    difficulty level (easy, normal, hard or beast):
        - Easy and normal difficulty level = 5 questions
        - Hard difficulty level = 10 questions
        - BEAST difficulty level = 24 questions (all available languages in
            chosen API minus English)

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


def is_viable_for_translation(user_input: str) -> bool:
    """Checks if user input are viable for translation.

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
            len(user_input.split()) == 1 or
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
    """Checks if user input is a valid answer.

    Ensures that the user input isn't an empty string and that it's at
    least 2 characters, in case the use has entered a code representing
    a language.

    Returns
    -------
    bool
        True if user input is not an empty string, otherwise False.
    """
    user_input = user_input.strip()
    return user_input and len(user_input) > 1
# endregion


def main():
    """Loads environment variables and run display and game functions."""
    load_dotenv()
    display_title()
    display_main_menu()

    while True:
        while not is_playing_game:
            toolkit_prompt(
                "", key_bindings=MENU_NAVIGATION_BINDINGS,
                bottom_toolbar=get_toolbar_text
            )

        try:
            run_game()
        except KeyboardInterrupt:
            quit_game()


main()
