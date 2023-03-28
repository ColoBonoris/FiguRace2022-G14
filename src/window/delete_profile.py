import PySimpleGUI as sg
import json
from src.constants.directions import *
from src.constants.style import *
from src.classes.Player import Player
from src.classes.Settings import Settings

def create_user_row(player_dict):
    """ Creates an interactive user frame"""
    if Settings.get_user() == player_dict["nick"]:
        aux_button = CIRCULAR_BUTTON_DIR
    else:
        aux_button = RED_CIRCULAR_BUTTON_DIR
    button_column = [
        [sg.Button('', button_color=CURRENT_COLORS, font=FONT_8, image_filename=aux_button, border_width=0, key="-NICK_{}-".format(player_dict["nick"]), pad=(10,0))]
    ]
    avatar_column = [
        [sg.Image(os.path.join(AVATARS_DIR,("avatar{}.png".format(player_dict["avatar"]))), background_color=CURRENT_COLORS[1])]
    ]
    avatar_nick_column = [
        [sg.Text(player_dict["nick"], font=FONT_3, text_color=CURRENT_COLORS[0], background_color=CURRENT_COLORS[1])],
        [sg.Text(player_dict["name"], font=FONT_5, text_color=CURRENT_COLORS[0], background_color=CURRENT_COLORS[1])]
    ]
    return [sg.Column(button_column), sg.Column(avatar_column,pad=(0,10)), sg.Column(avatar_nick_column, pad=(10,10))]
    #sg.Frame

def create_users_column():
    """ creates a column with all users"""
    try:
        with open(USERS_DIR,"r",encoding="utf-8",newline="") as users_file:
            players_list = json.load(users_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        players_list = []
    if(len(players_list) > 1):
        users_column = []
        for i in players_list:
            users_column.append([sg.Frame("",[create_user_row(i)], background_color=CURRENT_COLORS[1], size=(600,170))])
    else:
        return sg.Text("NOT ENOUGH TO DELETE",font=FONT_0,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(100,10))
    return sg.Column(users_column,scrollable=True,vertical_scroll_only=True,size=(605,500))

def create_users_layout():
    """ Returns a layout with all users to delete"""
    return [
        [sg.Button(button_color=CURRENT_COLORS, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(10,10))],
        [sg.Text("PROFILES",font=FONT_0,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(250,10))],
        [sg.Text("",font=FONT_0,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,0))],
        [sg.Frame("",[[create_users_column()]],background_color=CURRENT_COLORS[1],pad=(20,0))],
        [sg.Button('DELETE', button_color=CURRENT_COLORS, font=FONT_3, image_filename=LONG_BUTTON_DIR, border_width=0, key="-DELETE-", pad=(145,50))]
    ]

def create_users_window():
    """ creates the user deletion window"""
    scoreboard_layout = create_users_layout()
    return sg.Window("Delete User",scoreboard_layout,margins=(0,0))#,size=(650,600))

def delete_profile():
    """ Displays user deletion window"""
    try:
        with open(NICKS_DIR,"r",encoding="utf-8") as nicks_file:
            nicks_list = json.load(nicks_file)
        delete_user_events = list(map(lambda x: f"-NICK_{x}-",nicks_list))
    except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError):
        delete_user_events = []
    delete_profile_window = create_users_window()
    chosen_nick = Settings.get_user()
    while True:
        event, values = delete_profile_window.read()
        if event == sg.WINDOW_CLOSED or event == "-BACK-":
            break
        elif event == "-DELETE-":
            if(chosen_nick != Settings.get_user()):
                if(sg.PopupYesNo(f'Are you sure you wanna\ndelete "{chosen_nick}"',font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1]) == "Yes"):
                    Player.delete_player(chosen_nick)
                    break
            else:
                if(Settings.get_user() != None):
                    sg.Popup("You can't delete in-use profile!",font=FONT_5,text_color="black",background_color=CURRENT_COLORS[1])
                else:
                    break
        elif event in delete_user_events and (chosen_nick != (event[6:-1])):
            delete_profile_window.find_element("-NICK_{}-".format(chosen_nick)).update(image_filename=RED_CIRCULAR_BUTTON_DIR)
            delete_profile_window.find_element(event).update(image_filename=CIRCULAR_BUTTON_DIR)
            chosen_nick = (event[6:-1])
    delete_profile_window.close()