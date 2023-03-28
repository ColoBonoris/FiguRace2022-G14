from src.classes.Settings import Settings
from src.constants.directions import *
from time import time
import uuid
import pandas as pd

class Match():
    """
        This class will manage a match, it's instantiable and can be used to take control of a match.

        * possible_events will be a list of possible events that can be used in the match. This will be the only class variable.
        * scoring_tab will be a class variable, it will be used to calculate the scores, depending on the difficulty.
        * calculate_score will be static, it doesn't need any interaction with an instance.
    """
    possible_events = ["match_started", "match_ended", "timeout", "guess_made", "match_left","ended_with_error"]
    scoring_tab = {
        "Easy": 100,
        "Medium": 200,
        "Hard": 300,
    }

    def calculate_score(time_elapsed):
        """
          This function calculate the score based on the match scoring and time 
        """
        try:
            return int((((Settings.get_time() - time_elapsed) * Match.scoring_tab[Settings.get_difficulty()]) / (Settings.get_time() * Settings.get_hints())) * 1000)
        except (ZeroDivisionError):
            return 0

    def __init__(self):
        """ 
          This function is the instantiation of the game class to handle the events.
        """
        self.actual_round = 0
        self.events_list = []
        self.used_cards = []
        self.actual_correct = "-"
        self.new_event("-",Match.possible_events[0],"-")

    def create_event_dict(self, event, answer, state):
        """ This function creates and returns a proper event dictionary"""
        timestamp = time()
        if (event == Match.possible_events[3]):
            time_elapsed = (timestamp - self.events_list[-1]["timestamp"])
        elif (event == Match.possible_events[2]):
            time_elapsed = Settings.get_time()
        else:
            time_elapsed = "-"

        if(time_elapsed != "-" and state != "error"):
            score = Match.calculate_score(time_elapsed)
        elif(event == Match.possible_events[1]):
            score = (self.calculate_total_score())
        else:
            score = "-"

        return {
            "timestamp": timestamp,
            "id": str(uuid.uuid1()), # Puede ser uuid4 que en teoria deberia costar menos que uuid1 (creo)
            "player": Settings.get_user(),
            "event": event,
            "answer": answer,
            "correct": self.actual_correct,
            "state": state,
            "time_elapsed": time_elapsed,
            "score": score,
            "rounds_left": int(Settings.get_rounds() - self.actual_round),
            "level": Settings.get_difficulty()
        }

    def new_event(self, state, event, answer):
        """ This function creates a new event, to then append it to the events list"""
        self.events_list.append(self.create_event_dict(event, answer, state))

    def save_match(self):
        """ Saves all the events happened on the current match"""
        try:
            df=pd.read_csv(MATCHES_DIR,delimiter=',',encoding="utf-8")
        except FileNotFoundError:
            df=pd.DataFrame(columns=self.events_list[0].keys())
        for i in self.events_list:
           df=pd.concat([df,pd.DataFrame([i])])
        df.to_csv(MATCHES_DIR, index=False, encoding='utf-8')
    
    def calculate_total_score(self):
        """ Calculates the final score"""
        scores = list(filter(lambda x: x["state"] == "ok", self.events_list))
        score = 0
        for i in scores:
            score += i["score"]
        return score
    
    def start_new_round(self, new_correct):
        """ Starts a new round"""
        self.actual_round += 1
        self.set_correct(new_correct)
        return self.actual_round

    def set_correct(self, new_correct):
        self.actual_correct = new_correct
    
    def update_used(self):
        self.used_cards.append(self.actual_correct)

    def get_round(self):
        return self.actual_round
    
    def get_events(self):
        return self.events_list
    
    def get_correct(self):
        return self.actual_correct
    
    def get_used_cards(self):
        return self.used_cards
