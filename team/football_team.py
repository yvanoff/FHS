"""
Created on Fri Sep 25 2020

File defining a football Team

A subclass of Team, implementing it to represent a team for a Football match

@author: alexa
"""

from team.team import Team


class FootballTeam(Team):
    """
            Defines the Team playing in a sport match

            Attributes
            ----------
            players : list of tuple (FootballPlayer, str)
                        The players playing, along with their position on the pitch (in Football players may play in
                        various positions)
    """

    def __init__(self, club):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           club : FootballClub
                       The team which needs to select their 11 players

           Returns
           -------
           FootballTeam
                The initialized FootballTeam, ready to play a match
        """
        # init with default values or by loading the file
        pass
