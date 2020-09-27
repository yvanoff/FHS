"""
Created on Fri Sep 25 2020

File defining the football Engine Configuration.

My FootballEngine implementation of Engine requires some parameters used in the simulation to be set to values
which one might want to change depending on various criteria.

So this class reads a JSON file and initialize its parameters - which will be used by FootballEngine - using its content

@author: alexa
"""

from engine.ecfg.ecfg import ECfg


class FootballECfg(ECfg):
    """
            Defines the Engine configuration for the football matches Engine.

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

    def __init__(self, parameters_file=None):
        """
           Initializes engine parameters from a file, or from nothing if the file isn't specified (in which case
           defaults values will be used).

           Parameters
           ----------
           parameters_file : str
                       The path towards the config file to be loaded

           Returns
           -------
           FootballECfg
                The initialized EngineCfg object
        """
        # init with default values or by loading the file
        pass
