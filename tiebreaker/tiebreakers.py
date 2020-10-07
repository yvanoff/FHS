"""
Created on Thu Sep 10 2020

File defining the generic Tiebreaker class
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


class Tiebreaker:
    """
        Defines a generic Tiebreaker. Mostly used as a type of interface, to be overridden by Tiebreaker implementations.

        Attributes
        ----------
        name : str
                    The Tiebreaker's name
        round_applied : Round
                    The Round in which the Tiebreaker applies (to have access to any relevant data)

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to the tie-breaking criteria. If
                    some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
    """

    def __init__(self, name, cur_round):
        self.name = name
        self.round_applied = cur_round

    def tie_break(self, teams):
        pass

    def _first(self, cur_tuple):
        return cur_tuple[0]
