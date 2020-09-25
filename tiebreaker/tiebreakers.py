"""
Created on Thu Sep 10 2020

File defining the generic Tiebreaker class,
and a method converting str arguments to appropriate tiebreakers

@author: alexa
"""

from tiebreaker.away_goals_scored import AwayGoalsScored
from tiebreaker.conf_away_goals_scored import ConfAwayGoalsScored
from tiebreaker.conf_goal_difference import ConfGoalDifference
from tiebreaker.conf_goals_scored import ConfGoalsScored
from tiebreaker.conf_points import ConfPoints
from tiebreaker.goal_difference import GoalDifference
from tiebreaker.goals_scored import GoalsScored
from tiebreaker.points import Points


class Tiebreaker:
    """
        Defines a Tiebreaker. Mostly used as a type of interface, to be overridden by Tiebreaker implementations
        (currently three).

        Attributes
        ----------
        name : str
                    The Tiebreaker's name

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to the tie-breaking criteria. If
                    some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
    """

    def __init__(self, name):
        self.name = name

    def tie_break(self, teams):
        pass


def choose_correct_tb(tb_name):
    correct_tb = None
    # here we init the tiebreakers
    # possible values are:
    # - points to rank the teams according to their number of points
    # - diff to rank teams according to their goal difference
    # - gs to rank teams according to the number of goals scored
    # - ags to rank teams according to the number of goals scored away from home
    # - conf-points to rank teams according to the points won during their confrontations
    # - conf-diff to rank teams according to their goal difference during their confrontations
    # - conf-gs  to rank teams according to the goals scored during their confrontations
    # - conf-ags  to rank teams according to the away goals scored during their confrontations
    # - playoff to hold a playoff between two tied teams (HARDCODED)
    if tb_name == 'points':
        tb_name = Points(tb_name)
    elif tb_name == 'diff':
        tb_name = GoalDifference(tb_name)
    elif tb_name == 'gs':
        tb_name = GoalsScored(tb_name)
    elif tb_name == 'ags':
        tb_name = AwayGoalsScored(tb_name)
    elif tb_name == 'conf-points':
        tb_name = ConfPoints(tb_name)
    elif tb_name == 'conf-diff':
        tb_name = ConfGoalDifference(tb_name)
    elif tb_name == 'conf-gs':
        tb_name = ConfGoalsScored(tb_name)
    elif tb_name == 'conf-ags':
        tb_name = ConfAwayGoalsScored(tb_name)
    elif tb_name == 'playoff':
        tb_name = Tiebreaker(tb_name)
    else:
        print("Error ! Unknown tie-breaker")  # should raise an exception
    return correct_tb
