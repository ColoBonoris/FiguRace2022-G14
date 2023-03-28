import random
import csv
from src.constants.directions import *
from src.classes.Settings import Settings

def fifa_card_lines(line):
    """This function returns the card_lines of the fifa card"""
    line[2] = line[2].replace(" |", ",\n                 ")

    return (
        f"Team: {line[0]}",
        "Nationality: {}".format(line[1] if Settings.get_hints() > 1 else "-"),
        "Position: {}".format(line[2] if Settings.get_hints() > 2 else "-"),
        "Age: {}".format(line[3] if Settings.get_hints() > 3 else "-"),
        "Potential: {}".format(line[4] if Settings.get_hints() > 4 else "-"),
        FIFA_CARD_DIR,
        "Player:"
    )

def lakes_card_lines(line):
    """This function returns the card_lines of the lakes card"""
    if line[0]=="Tierra del Fuego, Antártida e Islas del Atlántico Sur":
        line[0]="Tierra del Fuego, Antártida\n                   e Islas del Atlántico Sur"
    line[4] = line[4].replace(", ", ",\n                          ")  

    return (
        f"Location: {line[0]}", 
        "Surface (km2): {}".format(line[1] if Settings.get_hints() > 1 else "-"),
        "Max. depth (m): {}".format(line[2] if Settings.get_hints() > 2 else "-"),
        "Avg. depth (m): {}".format(line[3] if Settings.get_hints() > 3 else "-"), 
        "Coordinates: {}".format(line[4] if Settings.get_hints() > 4 else "-"),
        LAKES_CARD_DIR,
        "Lake:"
    )

def spotify_card_lines(line):
    """This function returns the card_lines of the spotify card"""
    return (
        f"Genre: {line[0]}", 
        "Artist type: {}".format(line[1] if Settings.get_hints() > 1 else "-"),
        "Drop year: {}".format((line[2])[:-2] if Settings.get_hints() > 2 else "-"),
        "Best year: {}".format((line[3])[:-2] if Settings.get_hints() > 3 else "-"),
        "BPM: {}".format((line[4])[:-2] if Settings.get_hints() > 4 else "-"),
        SPOTIFY_CARD_DIR,
        "Artist:"
    )

def verify_option(options,option,df):
    """ This function checks that the correct answer is not repeated in the options """
    while (option in options):
        option=random.randint(1,len(df)-1)
    return option

def get_options_and_correct(df, used, end):
    """ This function checks that the correct answer is not repeated in the options """
    correct=random.randint(1,end)
    while df[correct][5] in used:
        correct=random.randint(1,end)
    option1=random.randint(1,end)
    option2=random.randint(1,end)
    option3=random.randint(1,end)
    options = [correct,option1,option2,option3]
    options[1]=verify_option(options,options[1],df)
    options[2]=verify_option(options,options[2],df)
    options[3]=verify_option(options,options[3],df)
    options[0]=df[options[0]]
    options[1]=df[options[1]]
    options[2]=df[options[2]]
    options[3]=df[options[3]]

    return options

def get_card_data(used):
    """Creates the card and the options, and returns them in that order"""
    if(Settings.get_topic() == "Mixed"):
        topic =  random.choice(["Lakes","Spotify Top","Fifa Players"])
    else:
        topic = Settings.get_topic()
    # FIFA: 17981 lines
    # Lakes: 57 lines
    # Spotify: 1000 lines
    match topic:
        case "Lakes":
            dir = LAKES_DIR
            amount = 57
            match Settings.get_difficulty():
                case "Easy":
                    end = amount // 3
                case "Medium":
                    end = amount // 2
                case "Hard":
                    end = amount
        case "Spotify Top":
            dir =SPOTIFY_DIR
            amount = 1000
            match Settings.get_difficulty():
                case "Easy":
                    end = amount // 20
                case "Medium":
                    end = amount // 10
                case "Hard":
                    end = amount
        case "Fifa Players":
            dir =FIFA_DIR
            amount = 17981
            match Settings.get_difficulty():
                case "Easy":
                    end = amount // 100
                case "Medium":
                    end = amount // 10
                case "Hard":
                    end = amount
    
    with open(dir, "r", encoding='utf-8') as file:
        df = csv.reader(file,delimiter=',')
        df = list(df)

    options = get_options_and_correct(df,used,end)
    correct = options[0]
    random.shuffle(options)

    return options, correct, topic
