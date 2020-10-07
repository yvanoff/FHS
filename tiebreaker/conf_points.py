"""
Created on Fri Sep 25 2020

File defining the ConfPoints Tiebreaker class

Points are widely used in various sports to rank clubs, with a varying number of points being given depending on a
match's result.

Here the twist compared to the usual Points tiebreaker is that the number of points of each team is computed over the
direct confrontations between teams

@author: alexa
"""

from tiebreaker.points import Points


class ConfPoints(Points):
    """
        Defines the ConfPoints Tiebreaker. Subclass of the Tiebreaker class. Ranks Club from highest to lowest point
        total, but the point total is recomputed over only the matches between clubs to be ranked

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
        for t in teams:
            t.reset_matches_data()
        for i in self.round_applied.results:
            for j in i:
                for match in j:
                    home, away = match.score.keys()
                    if (home in teams) and (away in teams):
                        match.update_club_stats(self.round_applied.points, self.round_applied.neutralGround)
        final_table = super().tie_break(teams)
        return final_table
