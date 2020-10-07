"""
Created on Fri Sep 25 2020

File defining the Away goals scored Tiebreaker class

This Tiebreaker is defined for any sport where the team have an AwayGoalsScored attribute

It's mostly used in Football where the number of goals scored away from home may be used as a tie breaker,
but it can be used for other sports if applicable

@author: alexa
"""

from tiebreaker.tiebreakers import Tiebreaker


class AwayGoalsScored(Tiebreaker):
    """
        Defines the Away Goals scored Tiebreaker. Subclass of the Tiebreaker class. Ranks Clubs according
        to the value of their AwayGoalsScored attribute from highest to lowest

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their number of away goals scored.
                    If some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
    """
    def __init__(self, name, cur_round):
        super().__init__(name, cur_round)

    def tie_break(self, teams):
        ags_for_each = []
        for t in teams:
            ags_for_each.append((t.awayGoalsScored, t))
        unready_table = sorted(ags_for_each, key=self._first, reverse=True)
        goals_only = [t[0] for t in unready_table]
        final_table = []
        g_i = 0
        while g_i < len(goals_only):
            g = goals_only[g_i]
            occ = goals_only.count(g)
            if occ == 1:
                final_table.append(unready_table[g_i][1])
            else:
                grouping = []
                for occ_i in range(occ):
                    grouping.append(unready_table[g_i+occ_i][1])
                final_table.append(grouping)
            g_i += occ
        return final_table
