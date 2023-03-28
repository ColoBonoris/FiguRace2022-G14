import PySimpleGUI as sg
from src.classes.Settings import Settings
from src.classes.Match import Match
from src.window.card_creation import get_card_data, fifa_card_lines, lakes_card_lines, spotify_card_lines
from src.constants.directions import *
from src.constants.style import *


class InGameEvents():
    """ 
        This class will control an instance of the Match class, and will coordinate it with the game window.
        With that said, we can consider it maybe as an "auxiliar" class, to ensure more (relative) security and better code readability.
    """
    def __init__(self, game_window, correct):
        """ Initializes an instance of the class, creates a new match and gets control over the game window"""
        self.match = Match()
        self.match.start_new_round(correct[5])
        self.game_window = game_window
    
    def update_card(self,correct_option,options,topic):
        """ Updates the card to guess"""
        match topic:    
            case "Lakes":
                card_lines = lakes_card_lines(correct_option)
            case "Spotify Top":
                card_lines = spotify_card_lines(correct_option)
            case "Fifa Players":
                card_lines = fifa_card_lines(correct_option)

        self.game_window.find_element("-CARD_LINE_0-").update(card_lines[0])
        self.game_window.find_element("-CARD_LINE_1-").update(card_lines[1])
        self.game_window.find_element("-CARD_LINE_2-").update(card_lines[2])
        self.game_window.find_element("-CARD_LINE_3-").update(card_lines[3])
        self.game_window.find_element("-CARD_LINE_4-").update(card_lines[4])
        self.game_window.find_element("to_guess").update(card_lines[6])
        
        self.game_window.find_element("-OPTION_1-").update(options[0][5])
        self.game_window.find_element("-OPTION_2-").update(options[1][5])
        self.game_window.find_element("-OPTION_3-").update(options[2][5])
        self.game_window.find_element("-OPTION_4-").update(options[3][5])

    def next_round(self):
        """ Moves the match to the next round"""
        self.match.update_used()
        options,correct,topic = get_card_data(self.match.get_used_cards())
        self.update_card(correct,options,topic)
        current_round = self.match.start_new_round(correct[5])
        self.game_window["progressbar"].UpdateBar(current_round)
        self.game_window["round"].update(f"CURRENT ROUND: {current_round}/{int(Settings.get_rounds())}")

    def guess_made(self,event):
        """ Makes everything to make a guess effective"""
        if(event != "-SKIP-"):
            answer = self.game_window[event].get_text()
        else:
            answer = "-"
        if(self.match.actual_correct == answer):
            state = "ok"
        else:
            state = "error"
        
        self.match.new_event(state,Match.possible_events[3],answer)
        if(self.match.get_round() == Settings.get_rounds()):
            self.match_ended_right() 
            return True
        else: 
            self.next_round()
            return False
    
    def timed_out(self):
        """ Makes everything to make a timeout effective"""
        self.match.new_event("-",Match.possible_events[2],"-")
        if(self.match.get_round() == Settings.get_rounds()):
            self.match_ended_right()
            return True
        else: 
            self.next_round()
            return False

    def match_ended_right(self):
        """ Ends the match correctly, returns the events list"""
        self.match.set_correct("-")
        self.match.new_event("-",Match.possible_events[1],"-")
        self.match.save_match()

        game_data = self.match.get_events()
        self.final_score = game_data[-1]["score"]
        del self.match
        
        return game_data

    def match_left(self):
        """ Ends the match as withdrawn, returns the events list"""
        self.match.set_correct("-")
        self.match.events_list = []
        self.match.new_event("-",Match.possible_events[4],"-")
        self.match.save_match()

        game_data = self.match.get_events()
        self.final_score = 0
        del self.match
        
        return game_data

    def ended_with_error(self):
        """ Ends the match with error, returns the events list"""
        self.match.set_correct("-")
        self.match.events_list = []
        self.match.new_event("-",Match.possible_events[5],"-")
        self.match.save_match()

        game_data = self.match.get_events()
        self.final_score = 0
        del self.match
        # Podría hacer un "del self"?
        return game_data
    
    def get_final_score(self):
        """ returns the final score of the match"""
        return self.final_score
