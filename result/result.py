"""
Created on Sat Sep 12 2020

File defining a generic Result class

The Result class define the result of a sport match. Override it with your own subclass when adding in a new sport

@author: alexa
"""


class Result:
    """
            Defines a sport match's results.

            Attributes
            ----------
            score : tuple of (int, int)
                        Tuple containing the number of points scored by the home and away team respectively.
                        Most if not all sports have a score of the format m-n, where m is the number of points
                        scored by the home team and n by the away team (however, there are some caveats - example:
                        tennis, or volley where it kinda works but kinda not - so this might be changed in the future)
            homeTeam : Club
                        The home team
            awayTeam : Club
                        The away team
            homeTeamPlayers : Team
                        The players for the home team
            awayTeamPlayers : Team
                        The players for the away team
            neutralGround : bool
                        Indicates if the match was played on neutral ground or not
update_club_stats: updates Team's stats and add to their results !
write_result

    """
    pass
