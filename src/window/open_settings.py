import PySimpleGUI as sg
from src.constants.directions import *
from src.constants.style import *
from src.classes.Settings import Settings


def create_settings_window():
    """ This function creates the parameters of the game options window"""
    # condicion para configurar el boton de musica segun el parametro 
    if(Settings.get_music()):
        music_button = sg.Button("On",font=FONT_4, button_color="white on green", key="-MUSIC-",pad=(0,20))
    else:
        music_button = sg.Button("Off",font=FONT_4, button_color="white on red", key="-MUSIC-",pad=(0,20))    

    settings_buttons_column = [
        [sg.Text('Mode',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))],
        [sg.Text('Difficulty',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))],
        [sg.Text('Rounds',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))],
        [sg.Text('Seconds per Round',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))],
        [sg.Text('Hints',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))],
        [sg.Text('Music',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))],
        [sg.Text('Theme',font=FONT_4,text_color=CURRENT_COLORS[0],background_color=CURRENT_COLORS[1],pad=(0,20))]
    ]
    values_column = [
        [sg.Combo(values=MODE_OPTIONS,font=FONT_4,key=('-TOPIC-'),default_value=(Settings.get_topic()),readonly=True,tooltip=('Choose here'),background_color=CURRENT_COLORS[2],pad=(0,20))],
        [sg.Combo(values=DIFFICULTY_OPTIONS,key=('-DIFFICULTY-'),font=FONT_4,default_value=(Settings.get_difficulty()),readonly=True,tooltip=('Choose here'),background_color=CURRENT_COLORS[2],pad=(0,20))],
        [sg.Slider((2,10),orientation="horizontal",default_value=(Settings.get_rounds()),key='-ROUNDS-',pad=(0,10))],
        [sg.Slider((5,40),orientation="horizontal",default_value=(Settings.get_time()),key='-TIME-',pad=(0,10))],
        [sg.Slider((2,5),orientation="horizontal",default_value=(Settings.get_hints()),key='-HINTS-',pad=(0,10))],
        [music_button],
        [sg.Combo(values=THEME_OPTIONS,font=FONT_4,key=('-THEME-'),default_value=(Settings.get_theme()),readonly=True,tooltip=('Choose here'),background_color=CURRENT_COLORS[2],pad=(0,20))],
    ]     
    settings_layout = [
        [sg.Button(button_color=CURRENT_COLORS, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(20,15))],
        [sg.Column(settings_buttons_column, vertical_alignment='center', justification='center',  k='-C-'),sg.Column(values_column)],
        [sg.Button('SAVE', button_color=CURRENT_COLORS, font=FONT_1, image_filename=LONG_BUTTON_DIR, border_width=0, key="-SAVE-", pad=(115,50))]
    ]
    return sg.Window('Settings',settings_layout,margins=(0,0))

def open_settings():
    """ Implements the game options window"""
    settings_window = create_settings_window()
    aux_music = Settings.get_music()
    while True:
        event, values = settings_window.read()
        if event == sg.WIN_CLOSED or event == "-BACK-":
            break         
        match event:          
            case '-MUSIC-':
                aux_music = not aux_music
                settings_window.find_element("-MUSIC-").update(
                    text='On' if aux_music else 'Off',
                    button_color='white on green' if aux_music else 'white on red'
                )   
            case '-SAVE-':
                Settings.update(Settings.get_user(),aux_music,values['-TOPIC-'],values['-DIFFICULTY-'],values['-ROUNDS-'],values['-TIME-'],values['-HINTS-'],values['-THEME-'])
                break
    settings_window.close()
    