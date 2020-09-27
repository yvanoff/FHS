"""
Created on Fri Sep 25 2020

File defining the generic Engine Configuration.

This is just related to the Engine class: any Engine will require various parameters depending on the sport being
simulated.

So just override this class with an implementation for your sport so your Engine can grab its correct parameters
from there

You might not even need it (I need it for the Football version implemented alongside the original release of FHS).

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
