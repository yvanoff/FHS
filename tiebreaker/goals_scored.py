"""
Created on Fri Sep 25 2020

File defining the Goals scored Tiebreaker class

@author: alexa
"""

from tiebreaker.tiebreakers import Tiebreaker


class GoalsScored(Tiebreaker):
    """
        Defines the Goals scored Tiebreaker. Subclass of the Tiebreaker class

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their number of goals scored.
                    If some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
    """
    def __init__(self, name):
        super().__init__(name)

    def tie_break(self, teams):
        pass
