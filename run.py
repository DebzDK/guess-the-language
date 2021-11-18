from inputmode import InputMode
from difficulty import Difficulty

title = """
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
difficulty = Difficulty.EASY.value
enable_hints = True

def display_title():
    """
    Prints title to console
    """
    global title
    print(title)

def display_main_menu():
    """
    Prints main manu options to console
    """
    print('-- PLAY [1]')
    print('-- GAME OPTIONS [2]')

    while True:
        userInput = input('Select menu option: ')

        if userInput == '2':
            display_game_options_menu()

def display_game_options_menu():
    """
    Prints game manu options to console
    """
    game_options_str = '---- Input mode: {}\n---- Difficulty: {}\n---- Enable hints: {}'
    print(game_options_str.format(InputMode.get_description(input_mode), Difficulty.get_description(difficulty), enable_hints))

def main():
    """
    Runs display and game functions
    """
    display_title()
    display_main_menu()

main()