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

    def __init__(self, name, cur_round):
        super().__init__(name, cur_round)

    def tie_break(self, teams):
        diff_for_each = []
        for t in teams:
            diff_for_each.append((t.goalsScored - t.goalsConceded, t))
        unready_table = sorted(diff_for_each, key=self._first, reverse=True)
        diff_only = [t[0] for t in unready_table]
        final_table = []
        d_i = 0
        while d_i < len(diff_only):
            d = diff_only[d_i]
            occ = diff_only.count(d)
            if occ == 1:
                final_table.append(unready_table[d_i][1])
            else:
                grouping = []
                for occ_i in range(occ):
                    grouping.append(unready_table[d_i+occ_i][1])
                final_table.append(grouping)
            d_i += occ
        return final_table
