"""
Created on Tue Sep 29 2020

Defines a method to choose the correct Club from a string

It's in a separate file to avoid import loops.

Don't forget to modify this file if you add tiebreakers !

Basically adding new sports would be cumbersome if you had to go modify the competition managers each time you
implemented a new one. This method is called by the competition manager so by just adding a case for your sport's Club
class the manager can load and use it

@author: alexa
"""

from club.football_club import FootballClub


def choose_correct_club(sport, club_data):
    """
       Club is a generic class not intended to be used, instead subclasses implementing Club for a particular sport
       should be used
       The issue is then to load the proper Club subclass corresponding to the proper sport
       This method gives an easy way to do this by using a string to select the correct Club subclass for a sport

       DON'T FORGET TO MODIFIY THIS IF YOU ADD A NEW CLUB SUBCLASS

       Parameters
       ----------
       sport : str
                    The sport which will be used
       club_data : str
                   The path towards the club data file to be loaded

       Returns
       -------
       Club
            The initialized Club, of the Club subclass corresponding to the sport specified in parameter
    """
    correct_club = None
    if sport == "foot":
        correct_club = FootballClub(club_data)
    else:
        print("The chosen sport has no supported Club !")  # EXCEPTION !!!!!
    return correct_club
