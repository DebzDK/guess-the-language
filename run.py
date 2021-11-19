from inputmode import InputMode
from difficulty import Difficulty
import re

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
 _                  __    _  ________   __  __              ________   _______ 
| |         /\     |  \  || |  ______| | |  | |     /\     |  ______| |  ___  |
| |        /  \    |   \ || | |  ____  | |  | |    /  \    | |  ____  | |___| |
| |       / /\ \   | |\ \|| | | |___ | | |  | |   / /\ \   | | |___ | |  _____|
| |___   /  __  \  | | \  | | |___ | | | |__| |  /  __  \  | |___ | | | |_____ 
|_____| /__/  \__\ |_|  \_| |________| |______| /__/  \__\ |________| |_______|
////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
"""
input_mode = InputMode.USER.value
difficulty_level = Difficulty.EASY.value
enable_hints = True


def display_title():
    """
    Prints title to console
    """
    print(TITLE)


def display_main_menu():
    """
    Prints main manu options to console
    """
    print("-- PLAY [1]")
    print("-- GAME OPTIONS [2]")
    print("-- QUIT [Q]")


def process_main_menu_selection(input):
    """
    Displays game menu options if user input is as expected value
    """
    if input == "1":
        start_game()
    elif input == "2":
        display_game_options_menu()
        await_input("Select game option: ",
                    process_game_option,
                    display_game_options_menu)
    elif quit_game(input):
        raise SystemExit()


def display_game_options_menu():
    """
    Prints game manu options to console
    """
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


def process_game_option(input):
    """
    Toggles game option based on user input and current settings
    """
    global input_mode
    global difficulty_level
    global enable_hints

    if input == "1":
        input_mode = input_mode + 1 if input_mode < 3 else 1
    elif input == "2":
        difficulty_level = difficulty_level + 1 if difficulty_level < 3 else 1
    elif input == "3":
        enable_hints = not enable_hints
    elif input == "4":
        display_main_menu()
        return True


def await_input(prompt, execute=None, update_terminal=None):
    """
    Awaits input, gives a prompt, executes a function based on input
    and calls a function to update the terminal if provided
    """
    while True:
        user_input = input(prompt)
        if execute is not None:
            stop_loop = execute(user_input)
            if (stop_loop is not True and update_terminal is not None):
                update_terminal()
            elif stop_loop:
                break
        else:
            break


def start_game():
    """
    Runs the game loop
    """
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
            (input_mode == 2 and num_of_questions_asked < len(sentences))):
        print(f"\nQuestion {num_of_questions_asked + 1}\n")

        if input_mode == 1:
            await_input(("Enter a sentence"
                        f" (no longer than {character_limit} characters"
                        " long):\n"),
                        is_viable_for_translation)
            num_of_questions_asked += 1
        elif input_mode == 2:
            print(sentences[num_of_questions_asked])
            num_of_questions_asked += 1
        else:
            break

    print((f"\nYou guessed {num_of_correct_answers}/{num_of_questions_asked}"
            " languages correctly..."
            "\nBetter luck next time.\n"))


def read_from_file():
    """
    Reads sentences from file
    """
    sentences = []
    while len(sentences) == 0:
        path_or_filename = input(
            "\nEnter the name or path of the file you wish to read from: ")
        try:
            with open(path_or_filename) as file:
                for line in file:
                    stripped_line = line.strip()
                    if (len(stripped_line) > 0 and
                            is_viable_for_translation(stripped_line)):
                        sentences.append(stripped_line)

                    if (len(sentences) ==
                            NUM_OF_QS_PER_DIFFICULTY_LEVEL[difficulty_level]):
                        break
        except FileNotFoundError as e:
            print("\nUh oh... Looks like that file doesn't exist.")
    return sentences


def is_viable_for_translation(input):
    """
    Validates sentences to ensure it adheres to the character limit
    for the current difficulty level
    """
    input = input.strip()
    str_len = len(input)
    if (str_len == 0 or
            re.search("^[^A-Za-z0-9]+", input) or
            str_len > CHAR_LIMIT_PER_DIFFICULTY_LEVEL[difficulty_level]):
        return False
    return True


def is_game_over(question_count):
    """
    Returns True if the user has been asked the total number of questions for
    the game's set difficult level, otherwise False
    """
    question_limit = NUM_OF_QS_PER_DIFFICULTY_LEVEL[difficulty_level]
    return question_count == question_limit


def quit_game(input):
    return input.lower() in QUIT_COMMANDS


def main():
    """
    Runs display and game functions
    """
    display_title()
    display_main_menu()
    await_input("Select menu option: ", process_main_menu_selection)


main()
