import PySimpleGUI as sg
from src.constants.directions import *
from src.constants.style import *
from src.window.choose_avatar import new_avatar
from src.classes.Player import Player

sg.set_options(font=FONT_6)

age_options = list(map(lambda i:f"{i}",range(1,101)))
age_options.append("I prefer not to say")

def create_edit_profile_window():
    """ Editing window layout"""
    edit_profile_input_column = [
        [sg.InputText(pad=(10,10),default_text=Player.get_name())],
        [sg.Combo(values=GENDER_OPTIONS,default_value=Player.get_gender(),pad=(10,10))],
        [sg.Combo(values=age_options,default_value=Player.get_age(),readonly=True,pad=(10,10))]
    ]
    edit_profile_text_column = [
        [sg.Text('Name',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))],
        [sg.Text('Gender',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))],
        [sg.Text('Age',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1],pad=(0,10))]
    ]
    edit_profile_avatar_column = [
        [sg.Button(button_color=CURRENT_COLORS, font=FONT_6, image_filename=AVATARS_DIR_ARRAY[Player.get_avatar()-1], border_width=0, key="-AVATAR-", pad=(10,20))]
    ]
    new_profile_layout = [
        [sg.Button(button_color=CURRENT_COLORS, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(20,10))],
        [sg.Column(edit_profile_avatar_column), sg.Column(edit_profile_text_column), sg.Column(edit_profile_input_column, vertical_alignment='center', justification='center',  k='-C-')],
        [sg.Button('SAVE', button_color=CURRENT_COLORS, font=FONT_6, image_filename=LONG_BUTTON_DIR, border_width=0, key="-SAVE-", pad=(115,50))]
    ]
    return sg.Window('Figurace G14 - New Profile', new_profile_layout, margins=(0,0))

def edit_profile():
    """ Window that allows editing an existing user"""
    avatar_number = Player.get_avatar()
    edit_profile_window = create_edit_profile_window()
    
    while True:
        event, values = edit_profile_window.read()
        if event == "-BACK-" or event == sg.WINDOW_CLOSED:
            break
        elif event == "-SAVE-":
            if(1<=len(values[0])<20) and (values[1] != "") and (values[2] in age_options):
                Player.update(values[0], values[1], values[2], avatar_number)
                Player.update_json()
                break
            else:
                if not (1<=len(values[0])<20):
                    sg.Popup("Name's length gotta be between 1 and 20 characters!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                elif (values[1] == ""):
                    sg.Popup("Enter a gender first!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
                elif (values[2] not in age_options):
                    sg.Popup("Choose a valid age first!",font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
        elif event == "-AVATAR-":
            avatar_number = new_avatar()
            edit_profile_window.find_element("-AVATAR-").update(image_filename=AVATARS_DIR_ARRAY[avatar_number - 1])
    edit_profile_window.close()
