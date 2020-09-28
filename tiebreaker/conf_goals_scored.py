"""
Created on Fri Sep 25 2020

File defining the Goals scored in direct confrontations Tiebreaker class

It's the same as the GoalsScored tiebreaker, except here it will computes the value of GoalsScored by itself.

Basically what a tiebreaker does is rank a list of Club according to the value of one of their attributes (here,
GoalsScored).

But sometimes, when some clubs are tied on an attribute value, you might want to break the tie by using the attribute
value recomputed on the matches between these teams.

Example: in Football, if two teams are tied on points, you might want to break the tie by looking at the team which
scored the most goals when playing away from home, but only when they were playing each other. So if A and B are tied on
points, A won 4-1 at home and B won 2-0 at home, then A would rank higher because they scored 4 goals against B while B
scored 3 goals when playing against A.

So basically what ConfGoalsScored does is recompute the value of the GoalsScored attribute for each team,
counting only the matches where they were playing each other (using the list of Results which is an attribute
of Club). Then it ranks the clubs according to the recomputed attribute. Of course the original values of the attributes
are backed up and restored afterwards.

@author: alexa
"""

from tiebreaker.goals_scored import GoalsScored


class ConfGoalsScored(GoalsScored):
    """
        Defines the Conf Goals scored Tiebreaker. Subclass of the Tiebreaker class. Ranks Clubs according
        to the value of their GoalsScored attribute from highest to lowest, but only when playing each other

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their number of goals
                    scored when they were playing against each other.
                    If some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
    """
    def __init__(self, name):
        super().__init__(name)

    def tie_break(self, teams):
        pass
