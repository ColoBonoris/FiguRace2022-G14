import PySimpleGUI as sg
from src.constants.directions import *
from src.constants.style import *
from src.window.card_creation import get_card_data, fifa_card_lines, lakes_card_lines, spotify_card_lines
from src.classes.Settings import Settings
from src.classes.InGameEvents import InGameEvents
from time import time

in_game_events = ["-OPTION_1-","-OPTION_2-","-OPTION_3-","-OPTION_4-","-SKIP-"]

#faltaría tener bien en cuenta el caso de strings muy largos y que no se corten
def create_game_window():
    """This function creates the game window"""
    options, correct, topic = get_card_data([])
    match Settings.get_topic():
        case "Mixed":
            card_colorTs = ("#cf7125","black")
            match topic:    
                case "Lakes":
                    card_lines = lakes_card_lines(correct)
                case "Spotify Top":
                    card_lines = spotify_card_lines(correct)
                case "Fifa Players":
                    card_lines = fifa_card_lines(correct)
            card_lines = (card_lines[0],card_lines[1],card_lines[2],card_lines[3],card_lines[4],MIXED_CARD_DIR,card_lines[6])
        case "Lakes":
            card_colorTs = ("#663f22","#35BFE9")
            card_lines = lakes_card_lines(correct)
        case "Spotify Top":
            card_colorTs = ("#02c101","black")
            card_lines = spotify_card_lines(correct)
        case "Fifa Players":
            card_colorTs = ("#35BFE9","#7f2b8a")
            card_lines = fifa_card_lines(correct)
                                                                
    data = [
        [sg.Image(filename=card_lines[5], background_color=card_colorTs[1],key="mode_image", pad=(10,5))],
        [sg.Text(card_lines[0],font=FONT_7,background_color=card_colorTs[0],text_color=card_colorTs[1],key="-CARD_LINE_0-", pad=(10,5))], 
        [sg.Text(card_lines[1],font=FONT_7, background_color=card_colorTs[0], text_color=card_colorTs[1],key="-CARD_LINE_1-", pad=(10,5))],
        [sg.Text(card_lines[2],font=FONT_7,background_color=card_colorTs[0],text_color=card_colorTs[1],key="-CARD_LINE_2-", pad=(10,5))],
        [sg.Text(card_lines[3],font=FONT_7, background_color=card_colorTs[0], text_color=card_colorTs[1],key="-CARD_LINE_3-",pad=(10,5))],
        [sg.Text(card_lines[4],font=FONT_7,background_color=card_colorTs[0],text_color=card_colorTs[1],key="-CARD_LINE_4-", pad=(10,5))]                                                          
    ]
    frame=[[sg.Frame('',data,font=FONT_4,background_color=card_colorTs[0],border_width=10)]]
    card=sg.Column(frame, size=(400,450), background_color=CURRENT_COLORS[1],key="-CARD-")

    options_game_buttons_column = sg.Column(
        [
            [sg.Text(f"00:{int(Settings.get_time())}",font=FONT_1,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],key="time")],
            [sg.Text("",background_color=CURRENT_COLORS[1])],
            [sg.Text("",background_color=CURRENT_COLORS[1])],
            [sg.Text(f"{card_lines[6]}",font=FONT_1,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],key="to_guess")],
            [sg.Button(options[0][5],font=FONT_4,button_color=(CURRENT_COLORS[0], CURRENT_COLORS[2]),size=(25,1),key="-OPTION_1-")],
            [sg.Button(options[1][5],font=FONT_4,button_color=(CURRENT_COLORS[0], CURRENT_COLORS[2]),size=(25,1),key="-OPTION_2-")],
            [sg.Button(options[2][5],font=FONT_4,button_color=(CURRENT_COLORS[0], CURRENT_COLORS[2]),size=(25,1),key="-OPTION_3-")],
            [sg.Button(options[3][5],font=FONT_4,button_color=(CURRENT_COLORS[0], CURRENT_COLORS[2]),size=(25,1),key="-OPTION_4-")],
            [sg.Button("Skip Card",font=FONT_4,button_color=CURRENT_COLORS[0],key="-SKIP-")]
        ],
        vertical_alignment='top',
        justification='center',
        key="-OPTIONS-"
    )
    
    play_game_layout = [
        [sg.Button(button_color=CURRENT_COLORS, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(20,15))],
        [sg.Text(f"Playing: {Settings.get_topic()}",font=FONT_1,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],key="-TITLE-")],
        [card,sg.Push(background_color=CURRENT_COLORS[1]),options_game_buttons_column],
        [sg.Text(f"CURRENT ROUND: 1/{int(Settings.get_rounds())}",font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],key="round")],
        [sg.ProgressBar(Settings.get_rounds(), orientation='h',size=(500,30), key='progressbar')]
    ]   
    return sg.Window('Partida',play_game_layout,margins=(0,0),size=(700,700)), correct

def play_figurace():
    """This function initializes the game window and it's functions."""
    game_window, correct = create_game_window()
    game_controller = InGameEvents(game_window, correct)
    ended = False

    starting_time = time()
    total_time = int(Settings.get_time())

    try:
        while not ended:
            event, values = game_window.read(timeout=100)

            ran_time = int(time() - starting_time)
            timer = total_time - ran_time
            game_window["time"].update(f"00:{timer}")
            if timer == 0:
                event = "-TIMED_OUT-"

            if event == sg.WIN_CLOSED or event == "-BACK-":
                break
            elif event in in_game_events:
                ended = game_controller.guess_made(event)
                if(not ended):
                    starting_time = time()
                    game_window["time"].update(f"00:{total_time}")
            elif event == "-TIMED_OUT-":
                ended = game_controller.timed_out()
                if(not ended):
                    starting_time = time()
                    game_window["time"].update(f"00:{total_time}")
    except:
        game_controller.ended_with_error()
        sg.Popup(f"Match ended with ERROR!\nScores won´t be saved",modal=True,font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
    else:
        if(not ended):
            game_controller.match_left()
            sg.Popup(f"Match Withdrawn!\nScores won´t be saved\nNeither your cheating counsciousness...",modal=True,font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
        else:
            sg.Popup(f"Match Ended! your\nfinal score is:\n{game_controller.get_final_score()}",modal=True,font=FONT_6,text_color="black",background_color=CURRENT_COLORS[1])
    
    del game_controller

    game_window.close()
