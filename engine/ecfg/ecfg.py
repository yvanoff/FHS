"""
Created on Fri Sep 25 2020

File defining the generic Engine Configuration and its parameters

@author: alexa
"""

from engine.ecfg.football_ecfg import FootballECfg


class ECfg:
    """
            Defines a generic Engine configuration.
    """

    def __init__(self, parameters_file=None):
        """
           Initializes engine parameters from a file, or from nothing if the file isn't specified

           Parameters
           ----------
           parameters_file : str
                       The path towards the config file to be loaded

           Returns
           -------
           ECfg
                The initialized EngineCfg object
        """
        # init with default values or by loading the file
        pass
