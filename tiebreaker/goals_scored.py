"""
Created on Fri Sep 25 2020

File defining the Goals scored Tiebreaker class

This Tiebreaker is defined for any sport where the team have an GoalsScored attribute

It's mostly used in Football where the number of goals scored may be used as a tie breaker,
but it can be used for other sports if applicable


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
