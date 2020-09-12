"""
Created on Sat Sep 12 2020

File defining the Player

@author: alexa
"""

class Player:
    class Team:
        """
                Defines a (football) Player.

                Attributes
                ----------
                name : str
                            The player's name
                strength : int
                            The player's overall strength
                penaltyTaker : bool
                            Indicates if the player takes penalties usually
                positionABilities : list of float
                            The list of ability of the player to play at each post. Contains 4 elements: the ability to
                            play as a goalkeeper, defender, midfielder and forward, respectively. The abilities are
                            multipliers ranging from 0 to 1 (both included). If ability for a post is >0, then the player
                            can play at this position and his strength there will be position ability * strength
                goalsScored : int
                            Number of goals scored by the player

                Methods
                -------
                Will probably need something to help a Team convert to XML (the team will need the player's data)
                increaseGS : int -> None
                            Increases goalsScored by the quantity given in attribute
                resetGoals : None -> None
                            Resets goalScored to 0
        """

        def __init__(self, playerData):
            """
               Initializes a team data given by the Team constructor from an XML file

               Parameters
               ----------
               playerData : ?
                           The player initialized

               Returns
               -------
               Player
                    The initialized Team
            """
            # init by loading the file
            pass