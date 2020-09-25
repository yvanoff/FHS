"""
Created on Fri Sep 25 2020

File defining a football Player

@author: alexa
"""

from player.player import Player


class FootballPlayer(Player):
    """
            Defines a Player.

            Attributes
            ----------
            name : str
                        The player's name
            strength : int
                        The player's overall strength
            penaltyTaker : bool
                        Indicates if the player takes penalties usually
            positionAbilities : list of float
                        The list of ability of the player to play at each post. Contains 4 elements: the ability to
                        play as a goalkeeper, defender, midfielder and forward, respectively. The abilities are
                        multipliers ranging from 0 to 1 (both included). If ability for a post is >0, then the player
                        can play at this position and his strength there will be position ability * strength
            goalsScored : int
                        Number of goals scored by the player
            nationality : str
                        The player's nationality

            Methods
            -------
            Will probably need something to help a Team convert to XML (the team will need the player's data)
            increaseGS : int -> None
                        Increases goalsScored by the quantity given in attribute
            resetGoals : None -> None
                        Resets goalScored to 0
    """

    def __init__(self, player_data):
        """
           Initializes a team data given by the Team constructor from an XML file

           Parameters
           ----------
           player_data : ?
                       The player initialized

           Returns
           -------
           FootballPlayer
                The initialized FootballPlayer
        """
        # init by loading the file
        pass
