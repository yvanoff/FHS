"""
Created on Wed Sep 23 2020

File defining the generic Round class

This define a round of a competition. A round is just what it says: it's a stage of a competition. M teams enter the
round, and once the round is over N teams remain, with M-N teams having been eliminated from the competition.

There are various ways to eliminate teams; rounds may have various structures. This is why this class is generic.
Subclasses implement the actual round types. As defined in the original programs there are only two round types defined
(which should cover most use cases). It is not encouraged to add more Round types because the Competition manager would
then need to be modified, and on top of that the Round class was not defined with other round types than League and
Knockout in mind.

@author: alexa
"""

from club.club import Bye
from club.selection import choose_correct_club
import os
import random


class Round:

    """
        Defines a round. Mostly used as a type of interface, to be overridden by Round implementations
        (currently two).

        A Round takes a list of Clubs, and plays itself to eliminate some of these teams based on matches results.
        These results are saved so that either the Competition manager can access them, or to write them somewhere

        Attributes
        ----------
        names : list of str
                    List of the names used for the individual rounds (list because a round may correspond to
                    numerous actual rounds)
        sport : str
                    The sport played in the round
        points : list of int
                    Number of points gained for a victory, a draw, a loss
        clubsDataPath : str
                    Path to the directory containing the data of teams to be loaded for this round if any (if
                    it is empty - '' - no data will be loaded).
        nbConfrontations : int
                    Number of times two teams play each other
        neutralGround : bool
                    A flag indicating if the matches take place on neutral ground for this round
        results: list of list of list of Result
                    The list of the match results
        clubs : list of Club
                    List of qualified clubs for this round
        isNatImp : bool
                    A flag to tell us if the nationality of teams matter
        isTierImp : bool
                    A flag to tell us if the clubs's tiers matter
        engineCfgPath : str
                    Path to the file containing the parameters used by the engine during the match simulation
        tieBreakers : list of TieBreaker
                    List of the tie breakers criteria to be used ranked in order

        Methods
        -------
        simulate : None -> list of Team
                    Plays the competition, saves the results in results and returns the list of qualified teams
        write : Bool -> Bool -> None
                    Writes the competition results. It uses the Competition's nat and tier parameters to know if
                    those should appear on match reports
        get_clubs : None -> list of Club
                    Gives the list of Club taking place in the round
        _draw_round : list of Team -> int -> bool -> bool -> list of Team
                    Draws teams for a round, taking into account the number of teams in each lot and various parameters
        _load_clubs : str -> list of Clubs
                    Load Team data for the round
        """

    def __init__(self, sport, round_parameters, nat, tier, engine_cfg_path):
        """
           Initializes a round from the adequate part of a competition JSON file

           Parameters
           ----------
           round_parameters : dict
                       The dict containing the round data
           nat : bool
                        Flag indicating if the teams's nationalities matter for this round or not
           tier : bool
                        Flag indicating whether the teams's tiers matter for this round or not
           engine_cfg_path : str
                        Path to the Engine configuration file containing the Engine Configuration used for this round

           Returns
           -------
           Round
                The initialized Round object
        """
        # test for the dict keys
        self.isNatImp = nat
        self.isTierImp = tier
        self.engineCfgPath = engine_cfg_path
        self.sport = sport
        if 'Names' in round_parameters.keys():
            self.names = round_parameters['Names']
        self.clubsDataPath = ''
        if 'Clubs_data' in round_parameters.keys():
            self.clubsDataPath = round_parameters['Clubs_data']
        self.nbConfrontations = 1
        if 'Nb_times_teams_play_each_other' in round_parameters.keys():
            self.nbConfrontations = round_parameters['Nb_times_teams_play_each_other']
        self.neutralGround = False
        if 'Matches_on_neutral_ground' in round_parameters.keys():
            self.neutralGround = round_parameters['Matches_on_neutral_ground']
        self.results = []
        self.clubs = self._load_clubs(self.clubsDataPath)
        self.tieBreakers = []
        self.points = [3, 1, 0]

    def simulate(self, list_added_clubs=None):
        """
           Simulates the round (to be overridden by subclasses implementations)

           Parameters
           ----------
           list_added_clubs : list of Club
                List of clubs to be added to this round

           Returns
           -------
           list of Club
                List of qualified clubs after this round
        """
        pass

    def write(self, nat=None, tier=None):
        """
               Writes the round's results (to be overridden by subclasses implementations)

               Parameters
               ----------
               nat : bool
                    Should the nationality appear in match reports
               tier : bool
                    Should the club's tier appear in match reports
        """
        pass

    def _draw_round(self, nb_groups):
        """
           Draw teams together for a Round

           Basically, n teams are given in input, and these n teams are spread across nb_groups pairings.
           Some parameters (nat and tier) mad modify how the draw is conducted.
           Teams are spread out evenly in all pairings, but if n % nb_groups > 0 some pairings will have 1 more club
           than the others
           Note that if pairings have an odd number of clubs in them, a dummy Bye club is added to ensure parity

           Parameters
           ----------
            nb_groups : int
                The number of pairings to be done

           Returns
           -------
           list of list of Club
                List of the pairings, which consists in list of Club
        """
        # ADD NATIONALITY SUPPORT !!!!
        # for it and same group no draw support:
        # make a list of possible opponents for every team
        # a draw is accepted only if the drawn team is in the accepted opponents of every team already drawn with it
        # and then we also only accept it the teams yet to be drawn still have possible opponents if we draw this one
        # here
        draw = []
        for i in range(nb_groups):
            draw.append([])
        pots = []
        clubs_by_pot = {}
        ok_opponents = {}
        for c in self.clubs:
            if c.pot not in pots:
                pots.append(c.pot)
                clubs_by_pot[c.pot] = [c]
            else:
                clubs_by_pot[c.pot].append(c)
            ok_opponents[c] = []
            for o in self.clubs:
                if o.pot != c.pot:
                    ok_opponents[c].append(o)
        # il faudrait twist les pots, ex: [1,2,3,4] devient [1,2,4,3] (first half + reverse second half)
        pots = sorted(pots)
        if pots[0] == 0:
            pots.append(pots.pop(0))
        current_group = 0
        for p in pots:
            nb_teams_in_pot = len(clubs_by_pot[p])
            for t in range(nb_teams_in_pot):
                chosen_team = random.choice(clubs_by_pot[p])
                clubs_by_pot[p].remove(chosen_team)
                draw[current_group].append(chosen_team)
                current_group += 1
                if current_group == nb_groups:
                    current_group = 0
        if self.isTierImp:
            for i in range(len(draw)):
                if (len(draw[i]) == 2) and (draw[i][0].tier < draw[i][1].tier):
                    draw[i] = [draw[i][1], draw[i][0]]
        for i in range(len(draw)):
            if (len(draw[i]) % 2) == 1:
                draw[i].append(Bye())
        return draw

    def _load_clubs(self, data_path):
        """
           Draw teams together for a Round

           Load club data in a directory

           Parameters
           ----------
           data_path : str
                The directory in which the clubs' data is located

           Returns
           -------
           list of Club
                The clubs loaded and ready to be used by the round
        """
        clubs = []
        if data_path != '':
            for file in os.scandir(data_path):
                if file.name.split(".")[1] == "xml":
                    clubs.append(choose_correct_club(self.sport, file.path))
        return clubs
