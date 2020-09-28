"""
Created on Fri Sep 25 2020

File defining the GoalDifference Tiebreaker class

This Tiebreaker is defined for any sport where the team have GoalsScored and GoalsConceded attributes

It's mostly used in Football where the goal difference is widely used as a tie breaker,
but it can be used for other sports if applicable


@author: alexa
"""

from tiebreaker.tiebreakers import Tiebreaker


class GoalDifference(Tiebreaker):
    """
        Defines the Goal-difference Tiebreaker. Subclass of the Tiebreaker class. It ranks Clubs from highest to
        lowest goal difference, goal difference being GoalsScored-GoalsConceded

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their goal difference. If some
                    teams are still tied after applying the tie breaking criteria they'll be grouped in a list inside
                    the list
    """

    def __init__(self, name):
        super().__init__(name)

    def tie_break(self, teams):
        pass
