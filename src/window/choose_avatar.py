import PySimpleGUI as sg
from src.constants.directions import *
from src.constants.style import *

avatar_events = ["-SAVE-","-AVATAR1-","-AVATAR2-","-AVATAR3-","-AVATAR4-","-AVATAR5-","-AVATAR6-","-AVATAR7-","-AVATAR8-","-AVATAR9-"]


def create_avatars_window():
    """This function creates the choosing avatar window."""
    avatars_layout = [
        [sg.Text("", pad=(0,0),text_color="black",background_color=CURRENT_COLORS[1])],
        [sg.Text("CHOOSE YOUR AVATAR:", font=FONT_2,text_color="black",background_color=CURRENT_COLORS[1],pad=(20,0))], # FONT
        [
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[0], border_width=0, key=avatar_events[1], pad=(10,10)),
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[1], border_width=0, key=avatar_events[2], pad=(10,10)),
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[2], border_width=0, key=avatar_events[3], pad=(10,10))
        ],
        [
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[3], border_width=0, key=avatar_events[4], pad=(10,10)),
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[4], border_width=0, key=avatar_events[5], pad=(10,10)),
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[5], border_width=0, key=avatar_events[6], pad=(10,10))
        ],
        [
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[6], border_width=0, key=avatar_events[7], pad=(10,10)),
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[7], border_width=0, key=avatar_events[8], pad=(10,10)),
            sg.Button('', button_color=CURRENT_COLORS, image_filename=AVATARS_DIR_ARRAY[8], border_width=0, key=avatar_events[9], pad=(10,10))
        ],
        [sg.Text("", pad=(0,5),text_color="black",background_color=CURRENT_COLORS[1])]
    ]
    return sg.Window("Figurace G14 - Avatar Selection", avatars_layout, margins=(10,0), modal=True)

def new_avatar():
    """This function returns a new avatar."""
    avatars_window = create_avatars_window()
    avatar = 1
    while True:
        event, values = avatars_window.read()
        if event == sg.WIN_CLOSED:
            break
        elif (event in avatar_events):
            avatar = int(event[-2])
            break
    avatars_window.close()
    return avatar

