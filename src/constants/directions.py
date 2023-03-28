import os
from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(Path(CURRENT_DIR).parent.parent,"data")

# USERS
USERS_DIR = os.path.join(DATA_DIR,"users","users.json")
NICKS_DIR = os.path.join(DATA_DIR,"users","loaded_nicks.json")

# CACHE
CACHE_DIR = os.path.join(Path(CURRENT_DIR).parent.parent,"data","cache")
SETTINGS_DIR = os.path.join(CACHE_DIR,"cached_settings.json")

# MATCHES
MATCHES_DIR = os.path.join(DATA_DIR,"matches","matches.csv")

# AUDIOS
AUDIO_DIR = os.path.join(DATA_DIR,"audio")
BACKGROUND_MUSIC_DIR = os.path.join(AUDIO_DIR,"slowerTempo.mp3")

# DATASETS
OLD_FIFA_DIR = os.path.join(DATA_DIR,"datasets","original","FIFA-21 Complete.csv")
OLD_LAKES_DIR = os.path.join(DATA_DIR,"datasets","original","Lagos Argentina - Hoja 1.csv")
OLD_SPOTIFY_DIR = os.path.join(DATA_DIR,"datasets","original","Spotify 2010 - 2019 Top 100.csv")

FIFA_DIR = os.path.join(DATA_DIR,"datasets","clean","FIFA_21.csv")
LAKES_DIR = os.path.join(DATA_DIR,"datasets","clean","Lagos_Argentina.csv")
SPOTIFY_DIR = os.path.join(DATA_DIR,"datasets","clean","Top_Spotify.csv")

# IMAGES
IMAGES_DIR = os.path.join(DATA_DIR,"images")

BACKGORUND_TOP_DIR = os.path.join(IMAGES_DIR,"LandscapeUpper.png")
BACKGROUND_BOTTOM_DIR = os.path.join(IMAGES_DIR,"LandscapeBottom.png")

LOGO_DIR = os.path.join(IMAGES_DIR,"FiguraceLogo.png")

BUTTONS_DIR = os.path.join(IMAGES_DIR,"buttons")
BUTTON_DIR = os.path.join(BUTTONS_DIR,"button.png")
RED_CIRCULAR_BUTTON_DIR = os.path.join(BUTTONS_DIR,"RedCircularButton.png")
CIRCULAR_BUTTON_DIR = os.path.join(BUTTONS_DIR,"CircularButton.png")
LONG_BUTTON_DIR = os.path.join(BUTTONS_DIR,"LongButton.png")
GRAY_LONG_BUTON_DIR = os.path.join(BUTTONS_DIR,"GrayLongButton.png")
BACK_BUTTON_DIR = os.path.join(BUTTONS_DIR,"buttonback.png")
X_BUTTON_DIR = os.path.join(BUTTONS_DIR,"buttonx.png")

CARDS_DIR = os.path.join(IMAGES_DIR,"cards")
MIXED_CARD_DIR = os.path.join(CARDS_DIR,"mixedCard.png")
SPOTIFY_CARD_DIR = os.path.join(CARDS_DIR,"spotifyCard.png")
LAKES_CARD_DIR = os.path.join(CARDS_DIR,"lakesCard.png")
FIFA_CARD_DIR = os.path.join(CARDS_DIR,"fifaCard.png")

AVATARS_DIR = os.path.join(IMAGES_DIR,"avatars")
AVATARS_DIR_ARRAY = [
    os.path.join(AVATARS_DIR,"avatar1.png"),
    os.path.join(AVATARS_DIR,"avatar2.png"),
    os.path.join(AVATARS_DIR,"avatar3.png"),
    os.path.join(AVATARS_DIR,"avatar4.png"),
    os.path.join(AVATARS_DIR,"avatar5.png"),
    os.path.join(AVATARS_DIR,"avatar6.png"),
    os.path.join(AVATARS_DIR,"avatar7.png"),
    os.path.join(AVATARS_DIR,"avatar8.png"),
    os.path.join(AVATARS_DIR,"avatar9.png")
]

