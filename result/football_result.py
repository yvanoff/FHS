"""
Created on Sat Sep 12 2020

Subclass of the Result class, defining a Football's match results.

Also contains Goal and ResPenShootout class, which are used to define a Football match's results

@author: alexa
"""

from result.result import Result


class FootballResult(Result):
    """
            Defines a football match's results.

            Attributes
            ----------
            score : tuple of (int, int)
                        Tuple containing the number of goals scored by the home and away team respectively
            homeTeam : FootballClub
                        The home team
            awayTeam : FootballClub
                        The away team
            homeTeamPlayers : FootballTeam
                        The players for the home team
            awayTeamPlayers : FootballTeam
                        The players for the away team
            goals : tuple of list of Goal
                        Tuple of two elements: first is the list of Goals scored by the home team, then is the list of
                        Goals scored by the away team
            penShootout : ResPenShootout
                        The result of a penalty shootout if one took place (a possibility in football)
            neutralGround : bool
                        Indicates if the match was played on neutral ground or not
updateTeamStats: updates Team's stats and add to their results !
write_results
    """
    pass


class Goal:
    """
            Defines a goal in the Football sport.

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
    pass


class ResPenShootout:
    """
            Defines the result of a penalty shootout.

            Attributes
            ----------
            score : tuple of (int, int)
                        Tuple containing the number of penalties scored by the home and away team respectively
            homeResults : list of tuple of (Player, bool)
                        The list of shooters for the home team and whether they scored or not
            awayResults : list of tuple of (Player, bool)
                        The list of shooters for the away team and whether they scored or not
    """
    pass
