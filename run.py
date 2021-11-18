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
input_mode = InputMode.USER
difficulty = Difficulty.EASY
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
    print('-- PLAY')
    print('-- GAME OPTIONS')

def display_game_options_menu():
    """
    Prints game manu options to console
    """
    game_options_str = '---- Input mode: {}\n---- Difficulty: {}\n---- Enable hints: {}'
    print(game_options_str.format(InputMode(input_mode).name, Difficulty(difficulty).name, enable_hints))

def main():
    """
    Runs display and game functions
    """
    display_title()
    display_main_menu()
    display_game_options_menu()

main()