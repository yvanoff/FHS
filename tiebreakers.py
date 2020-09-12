"""
Created on Thu Sep 10 2020

File defining the Tiebreaker class and its subclasses, and a method converting str arguments to appropriate tiebreakers

@author: alexa
"""

def strToTiebreakers(strInput):
    """
        Convert a list of string to a list of adequate Tiebreakers

        Parameters
        ----------
        strInput : list of str
                    The list of tiebreakers to be used
        Returns
        -------
        list of Tiebreakers
                    The list of Tiebreakers corresponding to the input list
    """
    pass

class Tiebreaker:
    """
        Defines a Tiebreaker. Mostly used as a type of interface, to be overridden by Tiebreaker implementations
        (currently three).

        Attributes
        ----------
        teams : list of Teams
                    The list of tied teams to be separated

        Methods
        -------
        tieBreak : None -> list of Team
                    Ranks the teams present in attribute from first to last according to the tie-breaking criteria. If
                    some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
        changeTeams : list of Teams -> None
                    Changes the teams attribute with the list of teals given
    """

class GoalDifference(Tiebreaker):
    """
        Defines the Goal-difference Tiebreaker. Subclass of the Tiebreaker class

        Methods
        -------
        tieBreak : None -> list of Team
                    Ranks the teams present in attribute from first to last according to their goal difference. If some
                    teams are still tied after applying the tie breaking criteria they'll be grouped in a list inside
                    the list
    """


class GoalsScored(Tiebreaker):
    """
        Defines the Goals scored Tiebreaker. Subclass of the Tiebreaker class

        Methods
        -------
        tieBreak : None -> list of Team
                    Ranks the teams present in attribute from first to last according to their number of goals scored.
                    If some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
    """


class Confrontation(Tiebreaker):
    """
        Defines the Goal-difference Tiebreaker. Subclass of the Tiebreaker class

        Attributes
        -------
        results : list of list of Results
                    The list of the matches results, necessary to rank the teams with this criteria
        awayGoalsUsed : bool
                    Flag indicating if the away goals are used to break ties

        Methods
        -------
        tieBreak : None -> list of Team
                    Ranks the teams present in attribute from first to last according to their results against one
                    another. If some teams are still tied after applying the tie breaking criteria they'll be grouped in
                    a list inside the list
    """