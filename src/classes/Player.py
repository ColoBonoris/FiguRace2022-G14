import json
import pandas as pd
import PySimpleGUI as sg
from src.classes.Settings import Settings
from src.constants.directions import *
from src.constants.style import *

class Player():
    """
        La clase Player guardará los datos del jugador actualmente en uso.
        Contiene todos los datos del usuario, menos el nick, que será manejado por la clase Settings.
        Así, podemos decir que la clase Player es una clase auxiliar, que solo se usará para guardar los datos "menos importantes" del jugador.
        Todos los datos se inicializarán con los valores por defecto.
        Tendrá utilidades para el tratado de usuarios en JSON, como añadir un nuevo usuario, eliminar uno, actualizar los datos del usuario actual en el JSON, etc.
        Al ser de uso único (no múltiple en un mismo momento), no se tendrá que instanciar, se usará directamente.
    """
    name =  PLAYER_DEFAULTS[0]
    avatar =  PLAYER_DEFAULTS[4]
    gender =  PLAYER_DEFAULTS[2]
    age =  PLAYER_DEFAULTS[3]

    def create_player_dict(name,
            nick,
            gender,
            age,
            avatar_number
        ):
        """ This function creates a player dictionary"""
        return {
            "name": name,
            "nick": nick,
            "avatar": avatar_number,
            "gender": gender,
            "age": age
        }
    
    def create_new_player(name, nick, gender, age, avatar_number):
        """ This function creates a new player"""
        new_player = Player.create_player_dict(name=name,nick=nick,gender=gender,age=age,avatar_number=avatar_number,)

        try:
            with open(USERS_DIR,"r",encoding="utf-8",newline="") as users_file:
                players_list = json.load(users_file)
                players_list.append(new_player)
            with open(USERS_DIR,"w",encoding="utf-8",newline="") as users_file:
                json.dump(players_list,users_file)
            with open(NICKS_DIR,"r",encoding="utf-8") as nicks_file:
                loaded_nicks = json.load(nicks_file)
                loaded_nicks.append(nick)
        except (FileNotFoundError, json.decoder.JSONDecodeError, TypeError, ValueError):
            with open(USERS_DIR,"w",encoding="utf-8",newline="") as users_file:
                json.dump([new_player],users_file)
            loaded_nicks = [nick]
        with open(NICKS_DIR,"w",encoding="utf-8") as nicks_file:
            json.dump(loaded_nicks,nicks_file)
        return new_player

    def delete_player(nick):
        """ This function deletes a player"""
        try:
            with open(USERS_DIR,"r",encoding="utf-8") as users_file:
                users_list = json.load(users_file)
            with open(NICKS_DIR,"r",encoding="utf-8") as nicks_file:
                nicks_list = json.load(nicks_file)
            delete_index = nicks_list.index(nick)
            nicks_list.remove(nick)
            del users_list[delete_index]
            with open(USERS_DIR,"w",encoding="utf-8") as users_file:
                json.dump(users_list,users_file)
            with open(NICKS_DIR,"w",encoding="utf-8") as nicks_file:
                json.dump(nicks_list,nicks_file)
            matches_df = pd.read_csv(MATCHES_DIR)
            matches_df = matches_df[(matches_df['player'] != nick)]
            matches_df.to_csv(MATCHES_DIR, index=False, encoding='utf-8')
        except (FileNotFoundError,IndexError,TypeError,ValueError,json.decoder.JSONDecodeError):
            sg.Popup("Player selected for deletion not found!",font=FONT_6,text_color="black",background_color="LightBlue")

    def update_with_json():
        """ This function updates player from  JSON File. The inverse function of update_json"""
        try:
            with open (NICKS_DIR,"r",encoding="utf-8") as nicks_file:
                nicks_list = json.load(nicks_file)
                position = nicks_list.index(Settings.get_user())
            with open(USERS_DIR,"r",encoding="utf-8")as users_file:
                players_list = json.load(users_file)
                player = players_list[position]
                Player.update(player["name"],player["gender"],player["age"],player["avatar"])
        except (FileNotFoundError, TypeError, ValueError, json.decoder.JSONDecodeError, IndexError):
            Settings.set_user(None)

    def update_json():
        """ This function updates JSON File with player data. The inverse function of update_with_json"""
        try:
            with open (NICKS_DIR,"r",encoding="utf-8") as nicks_file:
                nicks_list = json.load(nicks_file)
                position = nicks_list.index(Settings.get_user())
            with open(USERS_DIR,"r",encoding="utf-8") as users_file:
                loaded_users = json.load(users_file)
            loaded_users[position] = Player.create_player_dict(Player.name,Settings.get_user(),Player.gender,Player.age,Player.avatar)
        except (FileNotFoundError, json.decoder.JSONDecodeError, ValueError):
            # Isn't the most beautiful practice, but prevents errors from manual manipulation of the data files
            Settings.load_defaults()
            return
        with open(USERS_DIR,"w",encoding="utf-8") as users_file:
            json.dump(loaded_users,users_file)

    def update(name, gender, age, avatar):
        """ Updates player's information (only profile-related, not involving scores nor game-related data)"""
        Player.set_name(name)
        Player.set_avatar(avatar)
        Player.set_gender(gender)
        Player.set_age(age)

    def get_name():
        return Player.name

    def get_gender():
        return Player.gender

    def get_age():
        return Player.age

    def get_avatar():
        return Player.avatar

    def set_name(name):
        Player.name=name

    def set_avatar(avatar):
        Player.avatar=avatar
    
    def set_gender(gender):
        Player.gender=gender
    
    def set_age(age):
        Player.age=age
