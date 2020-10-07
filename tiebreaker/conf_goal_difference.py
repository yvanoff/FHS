"""
Created on Fri Sep 25 2020

File defining the Goal difference in direct confrontations Tiebreaker class

It's the same as the GoalDifference tiebreaker, except here it will computes the goal difference by itself.

Basically what a tiebreaker does is rank a list of Club according to the value of one of their attributes (here,
the goal difference, which is actually derived from GoalsScored and GoalsConceded).

But sometimes, when some clubs are tied on an attribute value, you might want to break the tie by using the attribute
value recomputed on the matches between these teams.

Example: in Football, if two teams are tied on points, you might want to break the tie by looking at the team which
scored the most goals when playing away from home, but only when they were playing each other. So if A and B are tied on
points, A won 3-1 at home and B won 1-0 at home, then A would rank higher because they have a goal difference of +1
against A while B has a goal difference of -1 when playing against B.

So basically what ConfGoalDifference does is recompute the value of the GoalsScored and GoalsConceded attributes for
each team, counting only the matches where they were playing each other (using the list of Results which is an attribute
of Club). Then it ranks the clubs according to the recomputed attribute. Of course the original values of the attributes
are backed up and restored afterwards.

@author: alexa
"""

from tiebreaker.goal_difference import GoalDifference


class ConfGoalDifference(GoalDifference):
    """
        Defines the Conf Goal Difference Tiebreaker. Subclass of the Tiebreaker class. Ranks Clubs according
        to the value of their Goal difference (which is GoalsScored-GoalsConceded) from highest to lowest, but only when
        playing each other

        Methods
        -------
        tie_break : list of Team -> list of Team
                    Ranks the teams present in attribute from first to last according to their goal difference
                    when they were playing against each other.
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
