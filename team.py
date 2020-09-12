"""
Created on Sat Sep 12 2020

File defining the Team

@author: alexa
"""

class Team:
    """
            Defines a Team.

            Attributes
            ----------
            name : str
                        The team's name
            nationality : str
                        Where the team is from
            tier : int
                        The team's tier
            formations : list of tuple of (str,float)
                        The list of the formations used by the team
            players : list of Player
                        The list of the team's players
            pot : int
                        The team's pot (used for the draw in some competitions)
            nbWin : int
                        Number of matches won by the team (used in leagues)
            nbDrawn : int
                        Number of matches drawn by the team (used in leagues)
            nbLosses : int
                        Number of matches lost by the team (used in leagues)
            goalsScored : int
                        Number of goals scored by the team (used in leagues)
            goalsConceded : int
                        Number of goals conceded by the team (used in leagues)

            Methods
            -------
            exportToXml : str -> None
                        Writes the team's data to an XML file, path given in attribute
            increaseWon : int -> None
                        Increases nbWin by the quantity given in attribute
            increaseDrawn : int -> None
                        Increases nbDrawn by the quantity given in attribute
            increaseLosses : int -> None
                        Increases nbLosses by the quantity given in attribute
            increaseGS : int -> None
                        Increases goalsScored by the quantity given in attribute
            increaseGC : int -> None
                        Increases GoalsConceded by the quantity given in attribute
            resetMatchesData : None -> None
                        Resets the nbWin, nbDrawn, nbLosses, goalsScored and goalsConceded attributes to 0
    """

    def __init__(self, teamData):
        """
           Initializes a team from an XML file

           Parameters
           ----------
           teamData : str
                       The path towards the team data file to be loaded

           Returns
           -------
           Team
                The initialized Team
        """
        # init by loading the file
        pass