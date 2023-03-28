import PySimpleGUI as sg
import json
from src.constants.directions import *
from src.constants.style import *
from src.window.choose_avatar import new_avatar
from src.classes.Player import Player
from src.classes.Settings import Settings

sg.set_options(font=FONT_6)

gender_options = ["Male","Female","I prefer not to say"]
age_options = list(map(lambda i:f"{i}",range(1,101)))
age_options.append("I prefer not to say")

def create_profile_window():
    """ This function creates and returns the window for profile creation"""
    new_profile_input_column = [
        [sg.InputText(pad=(10,10))],
        [sg.InputText(pad=(10,10))],
        [sg.Combo(values=gender_options,pad=(10,10))],
        [sg.Combo(values=age_options,readonly=True,pad=(10,10))]
    ]
    new_profile_text_column = [
        [sg.Text('Name',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))],
        [sg.Text('Nick',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))],
        [sg.Text('Gender',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))],
        [sg.Text('Age',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))]
    ]
    new_profile_avatar_column = [
        [sg.Button(button_color=CURRENT_COLORS, font=FONT_6, image_filename=AVATARS_DIR_ARRAY[0], border_width=0, key="-AVATAR-", pad=(10,20))]
    ]
    new_profile_layout = [
        [sg.Button(button_color=CURRENT_COLORS, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(20,10))],
        [sg.Column(new_profile_avatar_column), sg.Column(new_profile_text_column), sg.Column(new_profile_input_column, vertical_alignment='center', justification='center',  k='-C-')],
        [sg.Button('SAVE', button_color=CURRENT_COLORS, font=FONT_6, image_filename=LONG_BUTTON_DIR, border_width=0, key="-SAVE-", pad=(115,50))]
    ]
    return sg.Window('Figurace G14 - New Profile', new_profile_layout, margins=(0,0))

def new_profile():
    """ This function implements user's creation and it's proper window"""
    avatar_number = 1
    new_profile_window = create_profile_window()
    try:
        with open(NICKS_DIR,"r",encoding="utf-8") as nicks_file:
            loaded_nicks = json.load(nicks_file)
        with open(USERS_DIR,"r",encoding="utf-8") as users_file:
            loaded_users = json.load(users_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        Settings.reset_nicks_and_users()
        loaded_nicks = []
        loaded_users = []

    while True:
        event, values = new_profile_window.read()
        if event == "-BACK-" or event == sg.WINDOW_CLOSED:
            break
        elif event == "-SAVE-":
            # Se previene que exista un usuario en nicks y no en users y viceversa
            if((values[1] in loaded_users) != (values[1] in loaded_nicks)):
                Settings.reset_nicks_and_users()
                loaded_nicks = []
                loaded_users = []
            
            if(1<=len(values[0])<20) and (1<=len(values[1])<20) and (values[1] not in loaded_nicks) and (values[2] != "") and (values[3] in age_options):
                Player.create_new_player(values[0], values[1], values[2], values[3], avatar_number)
                break
            else:
                if not (1<=len(values[0])<20):
                    sg.Popup("Name's length gotta be between 1 and 20 characters!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                elif not (1<=len(values[1])<20):
                    sg.Popup("Nick's length gotta be between 1 and 20 characters!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                elif(values[1] in loaded_nicks):
                    sg.Popup("Nick already in use!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                elif (values[2] == ""):
                    sg.Popup("Enter a gender first!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                elif (values[3] not in age_options):
                    sg.Popup("Choose a valid age first!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
        elif event == "-AVATAR-":
            avatar_number = new_avatar()
            new_profile_window.find_element("-AVATAR-").update(image_filename=AVATARS_DIR_ARRAY[avatar_number - 1])
    new_profile_window.close()