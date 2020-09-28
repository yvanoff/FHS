"""
Created on Thu Sep 10 2020

File defining the generic Tiebreaker class, as well as a Generic HardcodedTB class,
and a method converting str arguments to appropriate tiebreakers

Tiebreakers are used in a variety of sports to break ties between two teams. Ties can occur in two situations:
- at the end of a match, two teams can be tied (especially in sports that are played in a defined time limit: teams
might be tied at the end of the time limit) but only one team can progress. A tie-breaker criteria will be used to
define which team should advance
- in a league competition, all teams play each other at least once, then a ranking is made using a criteria. Various
sports may use varying criteria, and sometimes this criteria won't be able to rank all teams since some teams will be
tied using this criteria, so a fallback criteria needs to be used to rank these teams

The basic idea is that the tiebreakers deriving from the Tiebreaker class rank a list of Clubs according to a specific
criteria and nothing more. To rank the clubs they only need the list of Club, and all the information needed to rank
these clubs is contained within the Club class

However some tie-breaking criteria require more than just the list of club to make their rankings. These will be
hardcoded inside the competition managers, and recognized because they'll use the HardcodedTB class

There is, similarly to the club/engine modules, a method to initialize the correct kind of Tiebreaker using a string
as input. If you implement a tie-breaking criteria based on the Tiebreaker class, don't forget to modify it

@author: alexa
"""

from tiebreaker.away_goals_scored import AwayGoalsScored
from tiebreaker.conf_away_goals_scored import ConfAwayGoalsScored
from tiebreaker.conf_goal_difference import ConfGoalDifference
from tiebreaker.conf_goals_scored import ConfGoalsScored
from tiebreaker.goal_difference import GoalDifference
from tiebreaker.goals_scored import GoalsScored
from tiebreaker.points import Points


class Tiebreaker:
    """
        Defines a generic Tiebreaker. Mostly used as a type of interface, to be overridden by Tiebreaker implementations.

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


class HardcodedTiebreaker(Tiebreaker):
    """
        Defines a hardoded Tiebreaker. This class is empty because the tie-breaking criteria is hardcoded in the
        competition managers

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
