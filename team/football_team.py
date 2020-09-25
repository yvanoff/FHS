"""
Created on Fri Sep 25 2020

File defining a football Team

@author: alexa
"""

from team.team import Team


class FootballTeam(Team):
    """
            Defines the Team playing in a sport match

            Attributes
            ----------
            players : list of FootballPlayers
                        The players playing the football match
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
