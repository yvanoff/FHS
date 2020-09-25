"""
Created on Fri Sep 25 2020

File defining the Knockout subclass of the Round class

@author: alexa
"""

from tiebreaker.tiebreakers import choose_correct_tb
from round import Round
from club.club import Bye
from engine.engine import choose_correct_engine
import os


class Knockout(Round):
    """
        A subtype of Round, representing a knockout format competition

        Attributes
        ----------
        nbRounds : int
                    Number of rounds to be played. If >= 2, the teams in the round 2 or afterwards will be the
                    teams who won in the previous round
        extraTimeType : str
                    Indicates the rules used for extra time. Can be "normal" (extra time will be 2 periods of 15
                    minutes each, team who scores the most goals wins), "gg" (golden goal, extra time is maximum
                    30 minutes played in two halves of 15min each but the first team to score wins) or "sg" (silver
                    goal, extra time is also 2 halves of 15 minutes but if a team leads at half time they win) or
                    "none" (no extra time in case of a draw)
        nbReplaysBeforePens : int
                    In case of a draw, number of times the match is replayed before we head to a penalty shootout.
                    If this value is -1 no penalty shootout will be held

        Methods
        -------
        _determine_tie_winner : list of Result -> Club
                    From a list of Result, returns the winning Club or None if nobody won
    """

    def __init__(self, sport, round_parameters, nat, tier, engine_cfg_path):
        """
           Initializes a knockout stage from the adequate part of a competition JSON file

           Parameters
           ----------
           round_parameters : dict
                       The dict containing the round data
           nat : bool
                        Flag indicating if the teams's nationalities matter for this round or not
           tier : bool
                        Flag indicating whether the teams's tiers matter for this round or not
           engine_cfg_path : EngineCfg
                        Engine configuration used for this round

           Returns
           -------
           Knockout
                The initialized Knockout object
        """
        super().__init__(sport, round_parameters, nat, tier, engine_cfg_path)
        self.nbRounds = round_parameters['Round']['Play_x_rounds'] # Number of consecutive rounds to be played
        # extra time type to use if teams are tied
        # possible values are:
        # - "" for no extra time
        # - "normal" for the regular verison
        # - "gg" for golden goal
        # - "sg" for silver goal
        self.extraTimeType = round_parameters['Round']['Extra_time']

        # when to do a penalty shootout
        # - -1 (actually anything smaller than 0) to never hold a pen shootout in case of a tie
        # - 0 to hold a pen shootout immediately in case of a tie (no replay)
        # - n with n>0 to hold a penalty shootout in case of a tie only after the match was replayed n times
        if 'Nb_replays_before_penalty_shootout' in round_parameters['Round'].keys():
            self.nbReplaysBeforePens = round_parameters['Round']['Nb_replays_before_penalty_shootout']
        else:
            self.nbReplaysBeforePens = -1

        self.points = [1, 0, 0]
        self.tieBreakers = []
        for tb in round_parameters['Round']['Tie_breakers']:
            self.tieBreakers.append(choose_correct_tb(tb))

        if 'Is_nationality_important' in round_parameters['Round'].keys():
            self.isNatImp = round_parameters['Round']['Is_nationality_important']
        if 'Is_club_level_important' in round_parameters['Round'].keys():
            self.isTierImp = round_parameters['Round']['Is_club_level_important']

    def simulate(self, list_added_clubs=None):
        """
           Simulates the round according to knockout rules

           Parameters
           ----------
           list_added_clubs : list of Club
                List of clubs to be added to this round

           Returns
           -------
           list of Club
                List of qualified clubs after this round
        """
        # les résultats du round seront présentés par confrontations
        # exemples: quarts de ldc
        # il y aura un dossier "Quarts"
        # avec des sous-dossiers "Barça-Bayern" "Atlético-RBL" etc.... et les résultats dans chacun d'entre eux
        if list_added_clubs is None:
            list_added_clubs = []
        for ac in list_added_clubs:
            self.clubs.append(ac)
        qualified_clubs = []
        self.results = []
        for r in range(self.nbRounds):
            res_round = []
            match_list = self._draw_round(self.clubs, (len(self.clubs) / +1) / 2, self.isNatImp, self.isTierImp)
            qualified_clubs = []
            for m in match_list:
                if not ((type(m[0]) is Bye) or (type(m[1]) is Bye)):
                    list_conf = []
                    for c in range(self.nbConfrontations):
                        if (c % 2 + self.nbConfrontations) == 1:
                            home_t, away_t = m
                        else:
                            away_t, home_t = m
                        match_engine = choose_correct_engine(self.sport, self.engineCfgPath, home_t, away_t,
                                                             self.neutralGround)
                        match_engine.simulateMatch()
                        res = match_engine.getResult()
                        list_conf.append(res)
                        res.updateClubStats(self.points)
                        res.updatePlayerStats()
                    winner = self._determine_tie_winner(m)
                    if winner is None:
                        # extra time case
                        if self.extraTimeType != "":
                            match_engine.simulateExtraTime(self.extraTimeType)
                            res = match_engine.getResult()
                            res.updateClubStats(self.points, True)
                            res.updatePlayerStats(True)  # the flag is here to tell the res to update only the e.t. part
                            list_conf.pop()
                            list_conf.append(res)
                            winner = self._determine_tie_winner(m)
                        if winner is None:
                            # pens/replays needed case
                            while winner is None:
                                nb_replays_done = 0
                                # rajouter un if sport == foot pour l'instant on verra après
                                if (nb_replays_done == self.nbReplaysBeforePens) and (self.sport == "foot"):  # immediate pens if no replays
                                    match_engine.simulateShoutoout()
                                    res = match_engine.getResult()
                                    list_conf.pop()
                                    list_conf.append(res)
                                    winner = res.getPenWinners()
                                elif winner is None:
                                    match_engine = choose_correct_engine(self.sport, self.engineCfgPath, home_t, away_t,
                                                                         True)
                                    home_t, away_t = away_t, home_t
                                    match_engine.simulateMatch()
                                    res = match_engine.getResult()
                                    list_conf.append(res)
                                    res.updateClubStats(self.points)
                                    res.updatePlayerStats()
                                    winner = self._determine_tie_winner(m)
                                    if winner is None:
                                        # extra time case
                                        if self.extraTimeType != "":
                                            match_engine.simulateExtraTime(self.extraTimeType)
                                            res = match_engine.getResult()
                                            res.updateClubStats(self.points, True)
                                            res.updatePlayerStats(True)
                                            list_conf.pop()
                                            list_conf.append(res)
                                            winner = self._determine_tie_winner(m)
                                    nb_replays_done += 1
                                else:
                                    print("Something weird is going on when determining the winner of a tie")
                    res_round.append(list_conf)
                    qualified_clubs.append(winner)
                else:
                    # potentially store the bye in results to write it later
                    if not (type(m[0]) is Bye):
                        qualified_clubs.append(m[0])
                    elif not (type(m[1]) is Bye):
                        qualified_clubs.append(m[1])
                    else:
                        print("Error with the number of teams !")  # would be better to have an exception
                m[0].reset_matches_data()
                m[1].reset_matches_data()
            # and then the list of teams is replaced by qualified_teams for the next
            self.results.append(res_round)
            for qt in qualified_clubs:
                qt.resetPot()
            self.clubs = qualified_clubs
        return qualified_clubs

    def write(self):
        """
               Writes a knockout round's results
        """
        for i_n in range(len(self.names)):
            try:
                n = self.names[i_n]
                og_dir = os.getcwd()
                os.mkdir(n)
                os.chdir(n)
                for list_conf in self.results[i_n]:
                    try:
                        new_og_dir = os.getcwd()
                        os.mkdir(list_conf[0].get_home_club().upper()+"_"+list_conf[0].get_away_club().upper())
                        os.chdir(list_conf[0].get_home_club().upper()+"_"+list_conf[0].get_away_club().upper())
                        for conf in list_conf:
                            conf.write()
                        os.chdir(new_og_dir)
                    except FileExistsError:
                        print("File already exists; aborting....")
                os.chdir(og_dir)
            except FileExistsError:
                print("File already exists; aborting....")

    def _determine_tie_winner(self, clubs):
        """
           Determines the winner of a tie

           Parameters
           ----------
           clubs : list of Club
                The two clubs to separate

           Returns
           -------
           Team
                The winning club if applicable - none otherwise
        """
        winner = None
        i = 0
        while (winner is None) or (i < len(self.tieBreakers)):
            ranking = self.tieBreakers[i].tieBreak(clubs)
            if not isinstance(ranking[0], list):
                winner = ranking[0]
            i += 1
        return winner
