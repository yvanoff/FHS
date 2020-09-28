"""
Created on Fri Sep 25 2020

Implementation of the Club class in the case of Football (also known as Calcio/Soccer/Fussball)

It uses all the attributes defined for a Club but adds attributes specific to Football

@author: alexa
"""

from club.club import Club


class FootballClub(Club):
    """
            Implementation of the Club class, to fit a Football club.
            The main addition are the goals-related attributes added to the attributes already defined by Club, since
            goals are specific to Football (well, and some other sports as well, but not all sports)

            Attributes
            ----------
            name : str
                        The club's name
            nationality : str
                        Where the club is from
            tier : int
                        The team's tier
            players : list of FootballPlayer
                        The list of the club's players. Obviously in this case they will be FootballPlayer, not generic
                        Player
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
            goalsScored : int
                        Number of goals scored by the club in the competition
            goalsConceded : int
                        Number of goals conceded by the club in the competition
            awayGoalsScored : int
                        Number of goals scored by the club when playing away from home
            backUps : list of dict
                        A list of dictionaries used to back up some stats (namely, the aforementioned ones plus any
                        stats specific to your Club subclass relevant to the sport simulated)
            matchList : list of FootballResult
                        The Club's results. In this case it's not generic Results, but Football results

            Methods
            -------
            export_to_xml : str -> None
                        Writes the team's data to an XML file, path given in attribute
            increase_won : int -> None
                        Increases nbWin by the quantity given in attribute
            increase_drawn : int -> None
                        Increases nbDrawn by the quantity given in attribute
            increase_losses : int -> None
                        Increases nbLosses by the quantity given in attribute
            reset_matches_data : None -> None
                        Resets the nbWin, nbDrawn, nbLosses attributes to 0
            back_up_stats : None -> None
                        Saves the current stats in the back-up list of dicts
            restore_last_backup : None -> None
                        Resets the stats to their value in the latest back-up dict
            get_pot : None -> Int
                        Returns the Team's pot
            get_tier : None -> Int
                        Returns the Team's tier
            app_result : FootballResult -> None
                        Adds a FootballResult (it's a FootballClub) to the matchList
            + methods to handle the goals scored
    """

    def __init__(self, club_data):
        """
           Initializes a Football club from an XML file. Clubs aren't supposed to be initialized by anything else than
           an XML file generated by the FootballClub creation tools

           Parameters
           ----------
           club_data : str
                       The path towards the football club data file to be loaded

           Returns
           -------
           FootballClub
                The initialized FootballClub
        """
        # init by loading the file
        pass
