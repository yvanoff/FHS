"""
Created on Tue Sep 29 2020

Defines a method to choose the correct Engine from a string

It's in a separate file to avoid import loops.

Don't forget to modify this file if you add tiebreakers !

Basically adding new sports would be cumbersome if you had to go modify the competition managers each time you
implemented a new one. This method is called by the competition manager so by just adding a case for your sport's Engine
class the manager can load and use it

@author: alexa
"""

from engine.football_engine import FootballEngine


def choose_correct_engine(sport, config_path, home_team, away_team, neutral_ground=False):
    """
       Engine is a generic class not intended to be used, instead subclasses implementing Engine for a particular sport
       should be used
       The issue is then to load the proper Engine subclass corresponding to the proper sport
       This method gives an easy way to do this by using a string to select the correct Engine subclass for a sport

       DON'T FORGET TO MODIFIY THIS IF YOU ADD A NEW CLUB SUBCLASS

       Parameters
       ----------
       sport : str
                    The sport which will be used
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
            The initialized Engine, of the Engine subclass corresponding to the sport specified in parameter
    """
    correct_engine = None
    if sport == "foot":
        correct_engine = FootballEngine(config_path, home_team, away_team, neutral_ground)
    else:
        print("The chosen sport has no supported Engine !")  # EXCEPTION !!!!!
    return correct_engine
