from inputmode import InputMode
from difficulty import Difficulty

NUMBER_OF_QUESTIONS_PER_DIFFICULTY_LEVEL = [5, 5, 10, 26]
CHARACTER_LIMIT_PER_DIFFICULTY_LEVEL = [30, 30, 40, 20]
QUIT_COMMANDS = ['q', 'quit']
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
    print('-- PLAY [1]')
    print('-- GAME OPTIONS [2]')
    print('-- QUIT [Q]')

def process_main_menu_selection(input):
    """
    Displays game menu options if user input is as expected value
    """
    if input == '2':
        display_game_options_menu()
        await_input('Select game option: ', process_game_option, display_game_options_menu)
    elif quit_game(input):
        raise SystemExit()

def display_game_options_menu():
    """
    Prints game manu options to console
    """
    game_options_str = '---- Input mode [1]: {}\n---- Difficulty [2]: {}\n---- Enable hints [3]: {}\n-- Return to main menu [4]'
    print(game_options_str.format(InputMode.get_description(input_mode), Difficulty.get_description(difficulty_level), enable_hints))

def process_game_option(input):
    """
    Toggles game option based on user input and current settings
    """
    global input_mode
    global difficulty_level
    global enable_hints

    if input == '1':
        input_mode = input_mode + 1 if input_mode < 3 else 1
    elif input == '2':
        difficulty_level = difficulty_level + 1 if difficulty_level < 3 else 1
    elif input == '3':
        enable_hints = not enable_hints
    elif input == '4':
        display_main_menu()
        return True

def await_input(prompt, execute, update_terminal = None):
    """
    Awaits input, gives a prompt, executes a function based on input
    and calls a function to update the terminal if provided
    """
    while True:
        userInput = input(prompt)
        stopLoop = execute(userInput)
        if (not stopLoop and update_terminal != None):
            update_terminal()
        elif stopLoop == True:
            break

def quit_game(input):
    return input.lower() in QUIT_COMMANDS

def main():
    """
    Runs display and game functions
    """
    display_title()
    display_main_menu()
    await_input('Select menu option: ', process_main_menu_selection)

main()