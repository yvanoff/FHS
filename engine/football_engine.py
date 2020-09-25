"""
Created on Fri Sep 25 2020

File defining a football Engine and its parameters

@author: alexa
"""

from engine.engine import Engine


class FootballEngine(Engine):
    """
            Defines the Engine.

            Attributes
            ----------
            parameters : FootballECfg
                        The engine parameters
            neutralGround : bool
                        Flag indicating if the match is played on neutral ground or not
            homeTeam : FootballTeam
                        Players for the home team
            awayTeam : FootballTeam
                        Players for the away team
            result : FootballResult
                        The match's result

            Methods
            -------
            simulateMatch : None -> None
                    Plays a 90-minutes long football match with both team's data, saves the result in the corresponding
                    attribute
            simulateExtraTime : str -> None
                    Plays 30 minutes of extra time according to the rules passed in Parameters, and updates the result
            simulateShoutoout : None -> None
                    Simulates a penalty shoutoot and updates the result with its conclusion
            getResult : None -> FootballResult
                    Returns the match's result
    """

    def __init__(self, config_path, home_team, away_team, neutral_ground=False):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           config_path : str
                       Path to the Engine configuration file to load
           home_team : FootballClub
                        Data for the home team
           away_team : FootballClub
                        Data for the away team
           neutral_ground : bool
                        Flag indicating if the match takes place on neutral ground

           Returns
           -------
           Engine
                The initialized FootballEngine
        """
        # init with default values or by loading the file
        pass
