import pandas as pd
import PySimpleGUI as sg
from src.constants.directions import *
from src.constants.style import *
from src.classes.Settings import Settings
from src.classes.Match import Match

FONT_0 = ("Arial 25 bold")
FONT_3 = ('Arial 17 bold')
FONT_5 = ("Arial 15 bold")
FONT_8 = ("Arial 10")

def get_tables_rows(mode):
    """ This function returns the rows for the scoreboard tables, first the mean's and second the score's"""

    try:
        events_df = pd.read_csv(MATCHES_DIR)
        assert(len(events_df) > 0)
        
        scores_df = events_df[(events_df["event"] == Match.possible_events[1]) & (events_df["level"] == mode)]
        scores_df = scores_df[["player", "score"]]

        scores_df = scores_df.sort_values(by="score", ascending=False).head(20)
        scores_lines = scores_df.values.tolist()
        means_lines = {}
        for i in scores_lines:
            if(i[0] in means_lines.keys()):
                means_lines[i[0]] = [int(means_lines[i[0]][0]) + int(i[1]), means_lines[i[0]][1]+1]
            else:
                means_lines[i[0]] = [int(i[1]),1]
        means_lines = list(map(lambda x: [x, str(means_lines[x][0] // means_lines[x][1])], means_lines))



        for i in range(len(means_lines),20):
            means_lines.append([["---"],["---"]])

        for i in range(len(scores_df),20):
            scores_lines.append([["---"],["---"]])
    
    except (FileNotFoundError, AssertionError):
        scores_lines = [[["---"],["---"]]] * 20
        means_lines = [[["---"],["---"]]] * 20

    means_lines = list(map(lambda x: [x+1, means_lines[x][0], means_lines[x][1]], range(0,20)))
    scores_lines = list(map(lambda x: [x+1, scores_lines[x][0], scores_lines[x][1]], range(0,20)))

    return means_lines, scores_lines
    
def create_scoreboard_table(mode):
    """ """
    means_lines, scores_lines = get_tables_rows(mode)
    
    return sg.Table(
            scores_lines,
            headings = [" # ", " Nick ", " Score "],
            def_col_width = 10,
            max_col_width = 300,
            display_row_numbers = False,
            num_rows = 20,
            row_height = None,
            font = FONT_5,
            justification = "center",
            text_color = "black",
            background_color = CURRENT_COLORS[2],
            header_background_color = "#69afb5",
            vertical_scroll_only = True,
            hide_vertical_scroll = False,
            border_width = 1,
            size = (400, 350),
            pad = (10,0),
            key = "-SCORES_TABLE-"
        ), sg.Table(
            means_lines,
            headings = [" # ", " Nick ", " Average "],
            def_col_width = 10,
            max_col_width = 300,
            display_row_numbers = False,
            num_rows = 20,
            row_height = None,
            font = FONT_5,
            justification = "center",
            text_color = "black",
            background_color = CURRENT_COLORS[2],
            header_background_color = "#69afb5",
            vertical_scroll_only = True,
            hide_vertical_scroll = False,
            border_width = 1,
            size = (400, 350),
            pad = (10,0),
            key = "-MEANS_TABLE-"
        )

def create_scores_window(mode):
    """ This function creates and returns the scoreboard's window"""
    table_1, table_2 = create_scoreboard_table(mode)

    scores_layout = [
        [sg.Button(button_color=CURRENT_COLORS, image_filename=BACK_BUTTON_DIR, border_width=0, key="-BACK-", pad=(0,0))],
        [   
            sg.Text('Difficulty:',font=FONT_5,text_color="black",background_color=CURRENT_COLORS[1],pad=(10,10)),
            sg.Combo(values=["Hard","Medium","Easy"],background_color=CURRENT_COLORS[2],default_value=Settings.get_difficulty(),enable_events=True,key="-DIFFICULTY_COMBO-",pad=(10,10))], 
        [table_1, sg.Push(background_color=CURRENT_COLORS[1]), table_2],
    ]

    return sg.Window("Scoreboards", scores_layout,background_color=CURRENT_COLORS[1],size=(850,500),margins=(0,0))

def show_scoreboard():
    """ This function shows the scoreboard window"""
    mode = Settings.get_difficulty()
    scoreboard_window = create_scores_window(mode)
    while True:
        event, values = scoreboard_window.read()
        if ((event == sg.WINDOW_CLOSED) or (event == "-BACK-")):
            break
        elif (event == "-DIFFICULTY_COMBO-"):
            if(mode != values[event]):
                mode = values[event]
                mean_rows, score_rows = get_tables_rows(mode)
                scoreboard_window.find_element("-MEANS_TABLE-").update(mean_rows)
                scoreboard_window.find_element("-SCORES_TABLE-").update(score_rows)

    scoreboard_window.close()
