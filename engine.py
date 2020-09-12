"""
Created on Sat Sep 12 2020

File defining the Engine and its parameters

@author: alexa
"""

class EngineCfg:
    """
            Defines the Engine configuration.

            Attributes
            ----------
            bonusDom : float
                        The strength multiplier for teams playing at home
            penProba : float
                        Percentage of the number of goals scored on penalties
            ogProba : float
                        Percentage of the number of goals which are own goals
            penaltyTerm : float
                        A penalty term used in the engine. Basically it should be decreased when the strength of teams
                        lowered, otherwise there can be issues with weak teams having trouble scoring even against
                        teams just as weak
            penScoringProba : float
                        Probability to score a penalty. Used in penalty shoutoots
    """

    def __init__(self, parametersFile = None):
        """
           Initializes engine parameters from a file, or from nothing if the file isn't specified

           Parameters
           ----------
           parametersFile : str
                       The path towards the config file to be loaded

           Returns
           -------
           EngineCfg
                The initialized EngineCfg object
        """
        # init with default values or by loading the file
        pass

class Engine:
    """
            Defines the Engine.

            Attributes
            ----------
            parameters : EngineCfg
                        The engine parameters
            neutralGround : bool
                        Flag indicating if the match is played on neutral ground or not
            homeTeam : Playing11
                        Players for the home team
            awayTeam : Playing11
                        Players for the away team
            result : Result
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
    """

    def __init__(self, config, homeTeam, awayTeam, neutralGround = False):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           config : EngineCfg
                       The Engine configuration
           homeTeam : Team
                        Data for the home team
           awayTeam : Team
                        Data for the away team
           neutralGroud : bool
                        Flag indicating if the match takes place on neutral ground

           Returns
           -------
           Engine
                The initialized Engine
        """
        # init with default values or by loading the file
        pass

class Playing11:
    """
            Defines the 11 playing players for each team.

            Attributes
            ----------
            players : list of Players
                        The 11 players playing
    """

    def __init__(self, team):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           team : Team
                       The team which needs to select their 11 players

           Returns
           -------
           Playing11
                The initialized Playing11, ready to play a match
        """
        # init with default values or by loading the file
        pass