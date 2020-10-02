"""
Created on Tue Sep 29 2020

Defines a method to choose the correct Tiebreaker from a string

It's in a separate file to avoid import loops.

Don't forget to modify this file if you add tiebreakers !

Basically adding tiebreakers would be cumbersome if you had to go modify the competition managers each time you
implemented a new one. This method is called by the competition manager so by just adding a case for your tiebreaker
the manager can load and use it

@author: alexa
"""

from tiebreaker.away_goals_scored import AwayGoalsScored
from tiebreaker.conf_away_goals_scored import ConfAwayGoalsScored
from tiebreaker.conf_goal_difference import ConfGoalDifference
from tiebreaker.conf_goals_scored import ConfGoalsScored
from tiebreaker.goal_difference import GoalDifference
from tiebreaker.goals_scored import GoalsScored
from tiebreaker.points import Points
from tiebreaker.tiebreakers import HardcodedTiebreaker


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
        correct_tb = Points(tb_name)
    elif tb_name == 'diff':
        correct_tb = GoalDifference(tb_name)
    elif tb_name == 'gs':
        correct_tb = GoalsScored(tb_name)
    elif tb_name == 'ags':
        correct_tb = AwayGoalsScored(tb_name)
    elif tb_name == 'conf-points':
        correct_tb = HardcodedTiebreaker(tb_name)
    elif tb_name == 'conf-diff':
        correct_tb = ConfGoalDifference(tb_name)
    elif tb_name == 'conf-gs':
        correct_tb = ConfGoalsScored(tb_name)
    elif tb_name == 'conf-ags':
        correct_tb = ConfAwayGoalsScored(tb_name)
    elif tb_name == 'playoff':
        correct_tb = HardcodedTiebreaker(tb_name)
    elif tb_name == 'playoff-':
        correct_tb = HardcodedTiebreaker(tb_name)
    else:
        print("Error ! Unknown tie-breaker")  # should raise an exception
    return correct_tb
