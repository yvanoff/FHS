"""
Created on Fri Sep 25 2020

Implementation of the Engine class in the case of Football (also known as Calcio/Soccer/Fussball)

It will implement Engine for a Football match, so that a football match between two football teams can be simulated

@author: alexa
"""

from engine.engine import Engine


class FootballEngine(Engine):
    """
            Defines an Engine implementation for a Football Club. No changes in terms of attributes, it's mostly
            the implementation of the methods which is interesting

            Attributes
            ----------
            parameters : FootballECfg
                        The engine parameters. The class is specific to Football, and is designed for use with
                        a FootballEngine
            neutralGround : bool
                        Flag indicating if the match is played on neutral ground or not
            homeTeam : Club
                        The home club
            awayTeam : Club
                        The away club
            homeTeamPlayers : Team
                        The players for the home team
            awayTeamPlayers : Team
                        The players for the away team
            result : FootballResult
                        The match's result. It's a football match's result

            Methods
            -------
            simulateMatch : None -> None
                    Plays a 90-minutes long football match with both team's data, saves the result in the corresponding
                    attribute
            simulateExtraTime : str -> None
                    Plays 30 minutes of extra time according to the rules passed in Parameters, and updates the result
            simulateShootout : None -> None
                    Simulates a penalty shoutoot and updates the result with its conclusion. Specific to FootballEngine
                    since a lot of sports don't have shootouts in case of ties
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
           FootballEngine
                The initialized FootballEngine
        """
        # init with default values or by loading the file
        pass
