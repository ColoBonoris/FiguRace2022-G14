import PySimpleGUI as sg
from src.constants.directions import *
from src.constants.style import *
from src.window.open_profile import open_profile
from src.window.show_scoreboard import show_scoreboard
from src.window.open_settings import open_settings
from src.window.main_game import play_figurace
from src.classes.Settings import Settings

menu_events = ["-PLAY-","-SETTINGS-","-PROFILE-","-SCOREBOARD-"]

sg.set_options(font=FONT_6)

def create_menu_window():
    """ This function creates the menu window"""
    menu_layout = [
        [sg.Image(BACKGORUND_TOP_DIR,background_color = CURRENT_COLORS[1],pad=(0,0))],
        [sg.Button('PLAY', button_color=CURRENT_COLORS, image_filename=(LONG_BUTTON_DIR if Settings.get_user() != None else GRAY_LONG_BUTON_DIR), border_width=0, key="-PLAY-", pad=(115,0))],
        [sg.Button('SETTINGS', button_color=CURRENT_COLORS, image_filename=LONG_BUTTON_DIR, border_width=0, key="-SETTINGS-", pad=(115,0))],
        [sg.Button('PROFILE', button_color=CURRENT_COLORS, image_filename=LONG_BUTTON_DIR, border_width=0, key="-PROFILE-", pad=(115,0))],
        [sg.Button('SCOREBOARD', button_color=CURRENT_COLORS, image_filename=LONG_BUTTON_DIR, border_width=0, key="-SCOREBOARD-", pad=(115,0))],
        [sg.Image(BACKGROUND_BOTTOM_DIR,background_color = CURRENT_COLORS[1],pad=(0,0))]
    ]
    return sg.Window('Figurace G14', menu_layout, margins=(0,0))

def menu():
    """ This function is the main function of the menu. It is the main window of the game menu"""
    menu_window = create_menu_window()
    while True:
        event, values = menu_window.read()
        if event == sg.WINDOW_CLOSED:
            break
        if event not in menu_events:
            continue
        match event:
            case "-PLAY-":
                if(Settings.get_user() != None):
                    menu_window.Hide()
                    play_figurace()
                    menu_window.UnHide()
                else:
                    sg.Popup("You can't play without first\npicking an user!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
            case "-SETTINGS-":
                menu_window.close()
                open_settings()
                menu_window = create_menu_window()
            case "-PROFILE-":
                menu_window.Hide()
                open_profile()
                if(Settings.get_user() == None) and (menu_window.find_element("-PLAY-").ImageFilename != GRAY_LONG_BUTON_DIR):
                    menu_window.find_element("-PLAY-").update(image_filename=GRAY_LONG_BUTON_DIR)
                elif(Settings.get_user() != None) and (menu_window.find_element("-PLAY-").ImageFilename == GRAY_LONG_BUTON_DIR):
                    menu_window.find_element("-PLAY-").update(image_filename=LONG_BUTTON_DIR)
                menu_window.UnHide()
            case "-SCOREBOARD-":
                menu_window.Hide()
                show_scoreboard()
                menu_window.UnHide()
    menu_window.close()
