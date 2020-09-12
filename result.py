"""
Created on Sat Sep 12 2020

File defining the Result class and classes used by it

@author: alexa
"""

class Result:
    """
            Defines a football match's results.

            Attributes
            ----------
            score : tuple of (int, int)
                        Tuple containing the number of goals scored by the home and away team respectively
            homeTeam : Team
                        The home team
            awayTeam : Team
                        The away team
            homeTeamPlayers : Playing11
                        The players for the home team
            awayTeamPlayers : Playing11
                        The players for the away team
            goals : list of Goal
                        List of the goals scored during the match
            penShootout : ResPenShootout
                        The result of a penalty shootout if one took place


    """

class Goal:
    """
            Defines a goal.

            Attributes
            ----------
            goalScorer : Player
                        The goalscorer
            time : str
                        The minute in which the goal was scored
            isPen : bool
                        Flag indicating if the goal was scored on penalty
            isOG : bool
                        Flag indicating it it's an own goal

    """

class ResPenShootout:
    """
            Defines the result of a penatly shootout.

            Attributes
            ----------
            score : tuple of (int, int)
                        Tuple containing the number of penalties scored by the home and away team respectively
            homeResults : list of tuple of (Player, bool)
                        The list of shooters for the home team and whether they scored or not
            awayResults : list of tuple of (Player, bool)
                        The list of shooters for the away team and whether they scored or not


    """