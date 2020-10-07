"""
Created on Fri Sep 25 2020

File defining the Points Tiebreaker class

Points are widely used in various sports to rank clubs, with a varying number of points being given depending on a
match's result.

@author: alexa
"""

from tiebreaker.tiebreakers import Tiebreaker


class Points(Tiebreaker):
    """
        Defines the Points Tiebreaker. Subclass of the Tiebreaker class. Ranks Club from highest to lowest point total

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their number of points. If some
                    teams are still tied after applying the tie breaking criteria they'll be grouped in a list inside
                    the list
    """

    def __init__(self, name, cur_round):
        super().__init__(name, cur_round)

    def tie_break(self, teams):
        points_for_each = []
        for t in teams:
            points_for_each.append((t.points, t))
        unready_table = sorted(points_for_each, key=self._first, reverse=True)
        pts_only = [t[0] for t in unready_table]
        final_table = []
        p_i = 0
        while p_i < len(pts_only):
            p = pts_only[p_i]
            occ = pts_only.count(p)
            if occ == 1:
                final_table.append(unready_table[p_i][1])
            else:
                grouping = []
                for occ_i in range(occ):
                    grouping.append(unready_table[p_i+occ_i][1])
                final_table.append(grouping)
            p_i += occ
        return final_table
