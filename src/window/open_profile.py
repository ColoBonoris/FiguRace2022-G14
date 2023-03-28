import PySimpleGUI as sg
from src.window.new_profile import  new_profile
from src.window.load_profile import load_profile
from src.window.delete_profile import delete_profile
from src.window.edit_profile import edit_profile
from src.constants.directions import *
from src.constants.style import *
from src.classes.Settings import Settings

profile_events = ["-LOAD-","-NEW-","-DELETE-","-BACK-","-EDIT-"]

sg.set_options(font=FONT_6)

def create_profile_window():
    """ Creates the profile creation window"""
    colors = (sg.theme_background_color("black"), sg.theme_background_color(CURRENT_COLORS[1]))
    profile_buttons_column = [
        [sg.Button('NEW PROFILE', button_color=colors, font=FONT_6, image_filename=LONG_BUTTON_DIR, border_width=0, key="-NEW-", pad=(115,10))],
        [sg.Button('LOAD PROFILE', button_color=colors, font=FONT_6, image_filename=LONG_BUTTON_DIR, border_width=0, key="-LOAD-", pad=(115,0))],
        [sg.Button('EDIT PROFILE', button_color=colors, font=FONT_6, image_filename=(LONG_BUTTON_DIR if Settings.get_user() != None else GRAY_LONG_BUTON_DIR), border_width=0, key="-EDIT-", pad=(115,10))],
        [sg.Button('DELETE PROFILE', button_color=colors, font=FONT_6, image_filename=LONG_BUTTON_DIR, border_width=0, key="-DELETE-", pad=(115,0))]
    ]
    profile_buttons_layout = [
        [sg.Button(button_color=colors, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(20,10))],
        [sg.Text("", pad=(0,10),font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])],
        [sg.Column(profile_buttons_column, vertical_alignment='center', justification='center',  k='-C-')],
        [sg.Text("", pad=(0,15),font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])]
    ]
    return sg.Window('Figurace G14 - Profile', profile_buttons_layout, margins=(0,0))

def open_profile():
    """ This function opens the user's managing window"""
    
    profile_window = create_profile_window()
    while True:
        event, values = profile_window.read()
        if event == sg.WINDOW_CLOSED or event == "-BACK-":
            break
        elif event in profile_events:
            match event:
                case "-NEW-":
                    profile_window.Hide()
                    new_profile()
                    profile_window.UnHide()
                case "-LOAD-":
                    profile_window.Hide()
                    load_profile()
                    if(Settings.get_user() == None) and (profile_window.find_element("-EDIT-").ImageFilename != GRAY_LONG_BUTON_DIR):
                        profile_window.find_element("-EDIT-").update(image_filename=GRAY_LONG_BUTON_DIR)
                    elif(Settings.get_user() != None) and (profile_window.find_element("-EDIT-").ImageFilename == GRAY_LONG_BUTON_DIR):
                        profile_window.find_element("-EDIT-").update(image_filename=LONG_BUTTON_DIR)
                    profile_window.UnHide()
                case "-EDIT-":
                    if(Settings.get_user() != None):
                        profile_window.Hide()
                        edit_profile()
                        profile_window.UnHide()
                    else:
                        sg.Popup("You can't edit without first\npicking an user!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                case "-DELETE-":
                    profile_window.Hide()
                    delete_profile()
                    profile_window.UnHide()
                    
    profile_window.close()
