"""
Created on Fri Sep 25 2020

File defining the Away goals scored in direct confrontations Tiebreaker class

It's the same as the AwayGoalsScored tiebreaker, except here it will computes the value of AwayGoalsScored by itself.

Basically what a tiebreaker does is rank a list of Club according to the value of one of their attributes (here,
AwayGoalsScored).

But sometimes, when some clubs are tied on an attribute value, you might want to break the tie by using the attribute
value recomputed on the matches between these teams.

Example: in Football, if two teams are tied on points, you might want to break the tie by looking at the team which
scored the most goals when playing away from home, but only when they were playing each other. So if A and B are tied on
points, A won 2-1 at home and B won 1-0 at home, then B would rank higher because they scored 1 goal away from home
against A while A scored 0 goals away from home when playing against B.

So basically what ConfAwayGoalsScored does is recompute the value of the AwayGoalsScored attribute for each team,
counting only the matches where they were playing each other (using the list of Results which is an attribute
of Club). Then it ranks the clubs according to the recomputed attribute. Of course the original values of the attributes
are backed up and restored afterwards.

@author: alexa
"""

from tiebreaker.away_goals_scored import AwayGoalsScored


class ConfAwayGoalsScored(AwayGoalsScored):
    """
        Defines the Conf Away Goals scored Tiebreaker. Subclass of the Tiebreaker class. Ranks Clubs according
        to the value of their AwayGoalsScored attribute from highest to lowest, but only when playing each other

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their number of away goals
                    scored when they were playing against each other.
                    If some teams are still tied after applying the tie breaking criteria they'll be grouped in a list
                    inside the list
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
