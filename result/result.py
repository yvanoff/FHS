"""
Created on Sat Sep 12 2020

File defining a generic Result class

The Result class define the result of a sport match. Override it with your own subclass when adding in a new sport

@author: alexa
"""


class Result:
    """
            Defines a sport match's results.

            Attributes
            ----------
            score : dict of (Team, int)
                        Dict containing the number of points scored by the home and away team respectively.
                        Most if not all sports have a score of the format m-n, where m is the number of points
                        scored by the home team and n by the away team (however, there are some caveats - example:
                        tennis, or volley where it kinda works but kinda not - so this might be changed in the future)
                        The team is the key that allows you to find its score
update_club_stats: updates Team's stats and add to their results !
write_result

    """

    def __init__(self, home_team, away_team):
        """
           Initializes the Result with the basic values - a sport match usually starts at 0-0, not points being scored
           by either side

           Parameters
           ----------
           home_team : Team
                       The team data for the home team
           away_team : Team
                        The team data for the away team

           Returns
           -------
           Result
                The initialized Result, ready to store the result of a match
        """
        self.score = {home_team: 0, away_team: 0}

    def update_club_stats(self, points=None):
        """
           Updates both clubs's stats with the result's data, including an update to their point total according to
           the parameter

           Parameters
           ----------
           points : list of Int
                       The points attributed for a win, a draw and a loss respectively. Used to update the clubs's
                       points total
        """
        pass

    def update_player_stats(self):
        """
           Updates the players's stats with the result's data (goals scored, try scored, etc...)
        """
        pass

    def write(self, path=None):
        """
           Writes the match's result, either in the current directory or in a specified path
        """
        pass
