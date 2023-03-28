"""
    FiguRace's main module, initializes all the needed (settings and current player data), calls the menu, and at the time of closing saves Setting's and current Player's data 
"""

if(__name__ == "__main__"):
    import os
    try:
        import PySimpleGUI as sg
    except ImportError:
        print("It seems like you haven't installed the requirements from requirements.txt.\nIf the problem persists maybe is because Tkinter isn't installed.\nInstall it with 'pip install tk' , or 'sudo apt-get install python3-tk' for Ubuntu.")
        exit()
    from src.constants.directions import *
    from src.constants.style import *
    from src.classes.Player import Player
    from src.classes.Settings import Settings
    from src.window.display_menu import menu

    dir_path = os.path.dirname(os.path.realpath(__file__))
    sg.set_options(font=FONT_6)

    Settings.update_with_json()
    Player.update_with_json()

    colors = CURRENT_COLORS

    menu()

    Settings.update_json()
    Player.update_json()
else:
    print("Game not properly executed!")
