"""
Created on Fri Sep 25 2020

File defining the football Engine Configuration.

My FootballEngine implementation of Engine requires some parameters used in the simulation to be set to values
which one might want to change depending on various criteria.

So this class reads a JSON file and initialize its parameters - which will be used by FootballEngine - using its content

@author: alexa
"""

from engine.ecfg.ecfg import ECfg
import json


class FootballECfg(ECfg):
    """
            Defines the Engine configuration for the football matches Engine.

            Attributes
            ----------
            bonusHome : float
                        The strength multiplier for teams playing at home
            penProb : float
                        Percentage of the number of goals scored on penalties
            ogProb : float
                        Percentage of the number of goals which are own goals
            penaltyTerm : float
                        A penalty term used in the engine. Basically it should be decreased when the strength of teams
                        lowered, otherwise there can be issues with weak teams having trouble scoring even against
                        teams just as weak
            penScoringProb : float
                        Probability to score a penalty. Used in penalty shootouts
    """

    def __init__(self, parameters_file=''):
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
        if parameters_file == '':
            self.bonusHome = 1.025
            self.penProb = 0.08
            self.ogProb = 0.03
            self.penaltyTerm = 2.0
            self.penScoringProb = 0.7
        else:
            comp_cfg_file = open(parameters_file)
            comp_cfg = comp_cfg_file.read()
            comp_cfg_file.close()
            json_cfg = json.loads(comp_cfg)
            self.bonusHome = json_cfg['bonus_home']
            self.penProb = json_cfg['pen_threshold']
            self.ogProb = json_cfg['prob_og']
            self.penaltyTerm = json_cfg['penalty_term']
            self.penScoringProb = json_cfg['prob_goal_pen']
