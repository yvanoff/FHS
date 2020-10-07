"""
Created on Sat Sep 12 2020

File defining a generic Result class

The Result class define the result of a sport match. Override it with your own subclass when adding in a new sport

It also adds a generic ByeResult class which defines a result in case a team is awarded a bye. Should work for any wsport

@author: alexa
"""

import os


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

            Methods
            ----------
            update_club_stats : list of int -> bool -> None
                        Updates both clubs's stats with the result's data, including an update to their point total
                        according to the parameter
            update_player_stats : None -> None
                        Updates the players's stats with the result's data (goals scored, try scored, etc...)
            write : bool -> bool -> str -> list of Result -> None
                        Writes the match's result, either in the current directory or in a specified path. The clubs's
                        nationalities and tiers are written or not depending on the booleans parameters
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

    def update_club_stats(self, points=None, neutral_ground=False):
        """
           Updates both clubs's stats with the result's data, including an update to their point total according to
           the parameter

           Parameters
           ----------
           points : list of Int
                       The points attributed for a win, a draw and a loss respectively. Used to update the clubs's
                       points total
           neutral_ground : bool
                        Indicates if the match took place on neutral ground
                        (some stats are related to playing home/away)
        """
        pass

    def update_player_stats(self):
        """
           Updates the players's stats with the result's data (goals scored, try scored, etc...)
        """
        pass

    def write(self, nat, tier, path=None, prev_m=None):
        """
           Writes the match's result, either in the current directory or in a specified path

           Parameters
           ----------
           nat : bool
                        Should the clubs's nationalities feature in the written report
           tier : bool
                        Should the club's tiers feature in the report
           path : str
                        The path where the result should be written. If not specified the file is written in the
                        current directory
           prev_m : list of Result
                        A list of previous results we want to write because they give useful information (for example
                        if two teams play each other 7 times, with the team with the most wins qualifying, it's useful
                        to know the result of previous matches when looking at the result of a match)
        """
        pass


class ByeResult:
    """
            Defines a Result when a team is awarded a Bye, to avoid Byes simply not appearing in the written record
            of the competition

            Attributes
            ----------
            club : Club
                        The club which is awarded the Bye
            message : str
                        The message to write in the competition's record

            Methods
            ----------
            write : str -> None
                        Writes the message in a file located in the specified path or in the current directory
    """
    def __init__(self, club, message):
        """
           Creates the ByeResult by initializing its message

           Parameters
           ----------
           team : Team
                        The team which is awarded the Bye
           message : str
                        The message to write to record the Bye
        """
        self.message = message
        self.club = club

    def write(self, path=None):
        """
           Writes the bye's record

           Parameters
           ----------
           path : str
                        The path where the bye should be written. If not specified the file is written in the
                        current directory
        """
        if path is None:
            path = '.'
        og_dir = os.getcwd()
        os.chdir(path)
        bye_res = open(self.club.name.upper()+".txt", "w+")
        bye_res.write(self.message)
        bye_res.close()
