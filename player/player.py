"""
Created on Sat Sep 12 2020

File defining a generic Player

Players of various sports have various attributes, since all sports don't put emphasis on the same characteristics

So the kid of Player needed depends on the sport, and so a new Player subclass will be required if you want to add
support for a new sport

@author: alexa
"""


class Player:
    """
            Defines a generic Player. Very basic since there's no real generic attributes common to all sports
            beside basic informations about the player

            Attributes
            ----------
            name : str
                        The player's name
            nationality : str
                        The player's nationality

            Methods
            -------
    """

    def __init__(self, player_data):
        """
           Players will be initialized when a Club is being initialized, using the data read by the Club constructor
           in the XML file defining the club. Only Club should be creating Player objects
           Same as for the Club class constructor, it won't be defined because it initializes from a file and we don't
           want to open it twice

           Parameters
           ----------
           player_data : xml.etree.ElementTree.Element
                       The player's data node as read by the Club constructor in the defining XML file.
                       It's the node of the XML tree

           Returns
           -------
           Player
                The initialized Player
        """
        self.name = ''
        self.nationality = ''
