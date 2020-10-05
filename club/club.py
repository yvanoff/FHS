"""
Created on Sat Sep 12 2020

File defining a generic Club, and a method selecting the appropriate subclass for a given sport

A club is an entity competing in sport. Clubs can compete in various sports (sometime the same clubs compete in
different sports at high level).

The aim here is to provide a generic Club class, that can be used to define a club no matter the sport played.
The club's data will then be used by the competition managers to simulate matches between Clubs and ultimately
give the competition's results.

The aim here is that this class is generic, providing only the basic information all clubs share no matter their sport
To add support for a new sport in FHS, just add a relevant class defining a club for this sport. Naming pattern
should be name of the sport+Club

Since adding a new class requires modifying the competition manager to load the correct class, this file also
provides a method which uses the club's init paramters and a string to initialize the correct Club subclass:
the string tells the method which sport is being simulated (and so which Club subclass should be used).
This method should be modified in case support for a new sport (and so a corresponding Club subclass) is added,
so the correct Club subclass is loaded

@author: alexa
"""


class Club:
    """
            Defines a generic sport Club. All methods (including the constructor) described here should be defined by
            your subclass while respecting these specifications since the competition managers will use them.

            Attributes
            ----------
            name : str
                        The club's name
            nationality : str
                        Where the club is from
            tier : int
                        The club's tier
            players : list of Player
                        The list of the club's players
            pot : int
                        The club's pot (used for the draw in some competitions, leave to 0 if not used)
            nbWin : int
                        Number of matches won by the club
            nbDrawn : int
                        Number of matches drawn by the club
            nbLosses : int
                        Number of matches lost by the club
            points : int
                        Number of points gained by the club. Most sports give a various number of points depending on
                        the result of the match
            backUps : list of dict
                        A list of dictionaries used to back up some stats (namely, the aforementioned ones plus any
                        stats specific to your Club subclass relevant to the sport simulated)
            matchList : list of Result
                        The Club's results in the competition being simulated

            Methods
            -------
            export_to_xml : str -> None
                        Writes the team's data to an XML file, path given in attribute
            reset_matches_data : None -> None
                        Resets the nbWin, nbDrawn, nbLosses attributes to 0
            backup_data : None -> None
                        Stores the current stats in a dict in the BackUps attribute
            restore_last_backup : None -> None
                        Restores the last backup in the BackUps attribute
            app_result : Result -> None
                        Adds a Result to the matchList
    """

    def __init__(self, club_data):
        """
           Initializes a club from an XML file. Clubs aren't supposed to be initialized by anything else than an XML
           file generated by the Club creation tools
           Not implemented because implementing it would make the Club subclasses call it, resulting in the file being
           opened twice (once for the super constructor, and one for the subclass constructor).
           So it just initializes everything to basic values

           Parameters
           ----------
           club_data : str
                       The path towards the club data file to be loaded

           Returns
           -------
           Club
                The initialized Club
        """
        self.name = ""
        self.nationality = ""
        self.tier = 1
        self.players = []
        self.pot = 0
        self.nbWin = 0
        self.nbLosses = 0
        self.nbDrawn = 0
        self.points = 0
        self.backUps = []
        self.matchList = []

    def export_to_xml(self, path=None):
        """
           Exports the club data to an XML file that can then be used by the Competition managers to init a Club

           Parameters
           ----------
           path : str
                       The path at which the output file will be located. If not specified, a file with the name
                       self.name+.xml will be created in the current directory
        """
        pass

    def write_club_data(self):
        """
           Returns the club data under the form of a string, so it can be used to write a table

           Returns
           ----------
           str
                       The string containing the club's relevant data for its ranking. Standardize the format
                       for your own sport
        """
        pass

    def reset_matches_data(self):
        """
           Resets the club's stats (points, number of wins/draws/losses, and anything specific to the sport implemented)
           to 0
        """
        pass


class Bye(Club):
    """
            Defines a dummy club called a bye.
            Used in those cases where there's an odd number of teams in a round so a team doesn't play.
            Since it's a dummy team it doesn't need attributes
    """

    def __init__(self, club_data=None):
        self.name = "bye"
