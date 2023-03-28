import json
import PySimpleGUI as sg
import os
from pygame import mixer
from src.constants.directions import *
from src.constants.style import *

mixer.init()
mixer.music.load(BACKGROUND_MUSIC_DIR)

class Settings():
    """
        La clase settings guardará:
            el nombre del jugador (user),
            el estado de la música (music para el estado actual y music_started para saber si en algún momento se inició)
            y los ajustes de juego (topic, difficulty, rounds, time, hints).
        Todas estas variables se inicializarán con los valores por defecto.
        Tendremos métodos para tratar con estos valores y actualizar la configuración, que se guardará en un fichero JSON, para luego consultarlo al iniciar el juego.
        La clase es completamente estática, no hay necesidad de instanciarla, se irá actualizando con JSON, datos nuevos o valores default.
    """
    music_started = False
    user = SETTINGS_DEFAULTS[0]
    music = SETTINGS_DEFAULTS[1]
    game_settings = SETTINGS_DEFAULTS[2].copy()
    theme = "Noon"

    def reset_nicks_and_users():
        """ Resets both nick's and user's jsons"""
        loaded_nicks = []
        loaded_users = []
        with open(USERS_DIR,"w",encoding="utf-8") as users_file:
            json.dump(loaded_users,users_file)
        with open(NICKS_DIR,"w",encoding="utf-8") as nicks_file:
            json.dump(loaded_nicks,nicks_file)

    def create_settings(user,music,topic,difficulty,rounds,time,hints,theme):
        """ Returns a dictionary with the setttings format"""
        return {
            "user": user,
            "music": music,
            "theme": theme,
            "game_settings": {
                "topic":topic,
                "difficulty":difficulty,
                "rounds":rounds,
                "time":time,
                "hints":hints
            }
        }

    def load_defaults(): 
        """ Creates the json settings with the class values"""
        if(os.path.exists(MATCHES_DIR)): os.remove(MATCHES_DIR)
        try:
            with open(NICKS_DIR,"r") as nicks_file:
                nicks_list = json.load(nicks_file)
            nick = nicks_list[0]
            assert os.path.exists(USERS_DIR)
        except (FileNotFoundError, IndexError, TypeError, json.decoder.JSONDecodeError, AssertionError):
            nick = None
        Settings.update(
            nick,
            SETTINGS_DEFAULTS[1],
            SETTINGS_DEFAULTS[2]["topic"],
            SETTINGS_DEFAULTS[2]["difficulty"],
            SETTINGS_DEFAULTS[2]["rounds"],
            SETTINGS_DEFAULTS[2]["time"],
            SETTINGS_DEFAULTS[2]["hints"],
            SETTINGS_DEFAULTS[3]
        )
    
    def update_json():
        """ This function updates the settings json file"""
        with open(SETTINGS_DIR,"w",encoding="utf-8") as settings_file:
            json.dump(Settings.create_settings(
                    Settings.user,
                    Settings.music,
                    Settings.get_topic(),
                    Settings.get_difficulty(),
                    Settings.get_rounds(),
                    Settings.get_time(),
                    Settings.get_hints(),
                    Settings.get_theme()
                ),
                settings_file
            )

    def update_with_json():
        """ Updates the current class with the settings json"""
        try:
            with open(SETTINGS_DIR,"r",encoding="utf-8") as settings_file:
                current_settings = json.load(settings_file)
                Settings.update(
                    current_settings["user"],
                    current_settings["music"],
                    current_settings["game_settings"]["topic"],
                    current_settings["game_settings"]["difficulty"],
                    current_settings["game_settings"]["rounds"],
                    current_settings["game_settings"]["time"],
                    current_settings["game_settings"]["hints"],
                    current_settings["theme"]
                )
        except (FileNotFoundError, KeyError, TypeError, json.decoder.JSONDecodeError):
            Settings.load_defaults()
    
    def update(user,music,topic,difficulty,rounds,time,hints,theme):
        """ This function updates the settings"""
        Settings.set_user(user)
        Settings.set_music(music)
        Settings.set_theme(theme)
        Settings.set_game_settings({"topic":topic,"difficulty":difficulty,"rounds":rounds,"time":time,"hints":hints})

    def get_music():
        return Settings.music
    
    def get_user():
        return Settings.user
    
    def get_difficulty():
        return Settings.game_settings["difficulty"]
    
    def get_time():
        return Settings.game_settings["time"]
    
    def get_topic():
        return Settings.game_settings["topic"]

    def get_rounds():
        return Settings.game_settings["rounds"]
    
    def get_hints():
        return Settings.game_settings["hints"]
    
    def get_game_settings():
        return Settings.game_settings

    def get_theme():
        return Settings.theme

    def set_user(user):
        Settings.user = user

    def set_game_settings(game_settings):
        Settings.game_settings = game_settings
    
    def set_music(music):
        """ Sets the music value and controls the music mixer"""
        if Settings.music != music:
            Settings.music = music
            if(music == True):
                if(not Settings.music_started):
                    Settings.music_started = True
                    mixer.music.play()
                else:
                    mixer.music.unpause()
            elif(Settings.music_started):
                mixer.music.pause()
    
    def set_theme(theme):
        Settings.theme = theme
        CURRENT_COLORS[1] = THEME_COLORS[theme]
        sg.theme_background_color(CURRENT_COLORS[1])
