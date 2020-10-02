"""
Created on Fri Sep 25 2020

An implementation of Player to define a Football player.

Unlike other subclasses this one defines a lot of stuff since we need to know a lot of information about Football
Players

@author: alexa
"""

from player.player import Player


class FootballPlayer(Player):
    """
            Defines a Football Player. Besides the basic attributes set by the Player class we'll have plenty of
            attributes which define characteristics rather specific to football

            Attributes
            ----------
            name : str
                        The player's name
            nationality : str
                        The player's nationality
            strength : int
                        The player's overall strength, or talent when it comes to playing Football. Defined with a
                        basic scale going from 0 to 100 in mind, where the average Football player in one of Europe's
                        top leagues (England/Spain/Germany/Italy) would be around 75
            penaltyTaker : bool
                        Indicates if the player normally takes penalties
            positionAbilities : list of float
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

    def __init__(self, player_data):
        """
           Initializes a FootballPlayer from data given by the FootballClub constructor, which reads an XML file

           Parameters
           ----------
           player_data : xml.etree.ElementTree.Element
                       The data defining the player as read in then XML file. It's an XML node

           Returns
           -------
           FootballPlayer
                The initialized FootballPlayer
        """
        super().__init__(player_data)
        self.strength = 0
        self.penaltyTaker = False
        self.positionAbilities = [0, 0, 0, 0]
        self.goalsScored = 0

        raw_elements = list(player_data)
        for e in raw_elements:
            if e.tag == 'name':
                self.name = e.text
            elif e.tag == 'country':
                self.nationality = e.text
            elif e.tag == 'strength':
                self.strength = int(e.text)
            elif e.tag == 'pen_shooter':
                self.penaltyTaker = (e.text == "Yes")
            elif e.tag == 'goals':
                self.goalsScored = int(e.text)
            elif e.tag == 'gk_ability':
                self.positionAbilities[0] = float(e.text)
            elif e.tag == 'df_ability':
                self.positionAbilities[1] = float(e.text)
            elif e.tag == 'md_ability':
                self.positionAbilities[2] = float(e.text)
            elif e.tag == 'fw_ability':
                self.positionAbilities[3] = float(e.text)
            else:
                print("Unknown data in the player data ! Ignoring....")
