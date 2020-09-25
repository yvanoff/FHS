"""
Created on Fri Sep 25 2020

File defining a football Club

@author: alexa
"""

from club.club import Club


class FootballClub(Club):
    """
            Defines a FootballClub.

            Attributes
            ----------
            name : str
                        The team's name
            nationality : str
                        Where the team is from
            tier : int
                        The team's tier
            players : list of FootballPlayer
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
                        Number of goals scored by the team
            goalsConceded : int
                        Number of goals conceded by the team
            awayGoalsScored : int
                        Number of goals scored by the team when playing away from home
            backUps : list of dict
                        A list of dictionaries used to back up some stats
            matchList : list of FootballResult
                        The Team's results

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
            app_result : Result -> None
                        Adds a Result to the matchList
    """

    def __init__(self, club_data):
        """
           Initializes a football club from an XML file

           Parameters
           ----------
           club_data : str
                       The path towards the club data file to be loaded

           Returns
           -------
           FootballClub
                The initialized FootballClub
        """
        # init by loading the file
        pass
