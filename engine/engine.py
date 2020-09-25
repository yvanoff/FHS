"""
Created on Sat Sep 12 2020

File defining the generic Engine and its parameters, and a method selecting the appropriate subclass for a given sport

@author: alexa
"""

from engine.football_engine import FootballEngine


class Engine:
    """
            Defines the Engine.

            Attributes
            ----------
            parameters : ECfg
                        The engine parameters
            neutralGround : bool
                        Flag indicating if the match is played on neutral ground or not
            homeTeam : Team
                        Players for the home team
            awayTeam : Team
                        Players for the away team
            result : Result
                        The match's result

            Methods
            -------
            simulateMatch : None -> None
                    Plays a 90-minutes long football match with both team's data, saves the result in the corresponding
                    attribute
            simulateExtraTime : str -> None
                    Plays extra time according to the rules passed in Parameters, and updates the result
            getResult : None -> Result
                    Returns the Result
    """

    def __init__(self, config_path, home_team, away_team, neutral_ground=False):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           config_path : str
                       Path to the Engine configuration file to load
           home_team : Club
                        Data for the home team
           away_team : Club
                        Data for the away team
           neutral_ground : bool
                        Flag indicating if the match takes place on neutral ground

           Returns
           -------
           Engine
                The initialized Engine
        """
        # init with default values or by loading the file
        pass


def choose_correct_engine(sport, config_path, home_team, away_team, neutral_ground=False):
    correct_engine = None
    if sport == "foot":
        correct_engine = FootballEngine(config_path, home_team, away_team, neutral_ground)
    else:
        print("The chosen sport has no supported Engine !")  # EXCEPTION !!!!!
    return correct_engine
