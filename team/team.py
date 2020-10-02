"""
Created on Fri Sep 25 2020

File defining a generic Team

A Team comes from a Club. A Club has all the information the Club needs: players, name, etc....
However, typically a Club has more players than it needs to play a match, because to play all matches during a season
you usually need more players than just enough for a match (because players will be injured, etc)

So there is a distinction to be made between the Club itself, and the Team playing a match. When a Club has to play a
match, it needs to pick a Team to play the match.

So here this class defines a generic Team. This should be overridden with your own implementation for your own sport

@author: alexa
"""


class Team:
    """
            Defines a generic Team playing in a generic sport match

            Attributes
            ----------
            club : Club
                        The club who the team represents
    """

    def __init__(self, club):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           club : Club
                       The team which needs to select their players for a match

           Returns
           -------
           Team
                The initialized Team, ready to play a match
        """
        self.club = club
