"""
Created on Sat Sep 12 2020

File defining a generic Engine and its parameters, and a method selecting the appropriate subclass for a given sport

The Engine is the "core" of FHS - it's what simulates a sport match between two teams.

In the aim to provide support for various sports, this class is just a template which provides a basic structure
for how to create a sport Engine. To add support for a new sport in FHS, simply override this class with a new
implementation. New sport engines should be named after the pattern name of the sport+Engine.

The competition managers will only explicitly use methods defined here, although other internal or external methods
can be created if you so need (they won't be handled by the competition managers unless you modify them too, though).

To help with creating new Engine implementations for various sports, a method exists to initialize the correct Engine
subclass depending on the target sport. Obviously this method should be modified if you add a new Engine subclass

@author: alexa
"""


class Engine:
    """
            Defines a generic Engine. It's very simple, the Engine simulates a sport match so it requires two Teams
            (not Club ! Teams are initialized from Clubs, though) which will play against each other, whichever
            parameters the Engine might requires (this would depend on the sport), and it gives away a result.

            Attributes
            ----------
            parameters : ECfg
                        The engine parameters, using a generic class here (since parameters will depend on the sport.
                        Actually they can even depend on the Engine's implementation. Anyway, here go pretty much any
                        specific parameter your Engine requires which doesn't fit elsewhere. See the ecfg submodule
                        for how it works)
            neutralGround : bool
                        Flag indicating if the match is played on neutral ground or not (can be important if the sport
                        has home advantage - most sports do so this is relevant here)
            homeTeamPlayers : Team
                        The players for the home team
            awayTeamPlayers : Team
                        The players for the away team
            result : Result
                        The match's result, stored here as a generic Result (the specific class will depend on the
                        sport). It's an attribute because it may be modified later so we need to keep track of it.

            Methods
            -------
            simulateMatch : None -> None
                    Plays a sport match between the two teams and saves the result in the result parameter
            simulateExtraTime : str -> None
                    Plays extra time according to the rules passed in Parameters, and updates the result. Relevant here
                    because most if not all sports playing with a time limit have extra time in case of a tie at the end
                    of the match. And sports which end after a Team reaches a certain amount of points can simply
                    not redefine this method since if there is no tie it will never be used
            getResult : None -> Result
                    Returns the Result
    """

    def __init__(self, config_path, home_team, away_team, neutral_ground=False):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           config_path : str
                       Path to the Engine configuration file to load
           home_team : Club
                        Data for the home team
           away_team : Club
                        Data for the away team
           neutral_ground : bool
                        Flag indicating if the match takes place on neutral ground

           Returns
           -------
           Engine
                The initialized Engine
        """
        # init with default values or by loading the file
        pass

    def simulate_match(self):
        """
           Simulates a sport match between two teams, and stores the result of the match in the result attribute
        """
        pass
