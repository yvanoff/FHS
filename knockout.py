"""
Created on Fri Sep 25 2020

File defining the Knockout subclass of the Round class

There is another type of Round which is used in sport: the knockout round.

Basically, it's a round where M teams enter. The M teams are drawn in duel where 2 teams play each other (the number
of matches depend on the competition). Then the team with the best record wins the tie and qualifies; the other team
loses and is eliminated

So we have M teams which enter, and M/2 teams who qualify. Not that this is not exact: the number of teams may be odd,
in which case one random team will be awarded a Bye - it will qualify automatically without playing

A feature of Knockout rounds is that they tend to be chained together until one team wins. For example in the Coupe de
France, 64 teams meet in the round of 64. 32 teams qualify for the round of 32. 16 teams qualify for the round of 16.
8 teams qualify for the quarter finals. 4 teams qualify for the semi finals. 2 teams qualify for the final. 1 team
wins the competition. So the ability to chain together Knockout round is important

@author: alexa
"""

from tiebreaker.selection import choose_correct_tb
from round import Round
from club.club import Bye
from engine.selection import choose_correct_engine
import os


class Knockout(Round):
    """
        A subtype of Round, representing a knockout format competition

        Attributes
        ----------
        nbRounds : int
                    Number of rounds to be played. If >= 2, the teams in the round 2 or afterwards will be the
                    teams who won in the previous round

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
                # s'arrêter si quelqu'un gagne (floor(nb_matches_max/2))+1 matches
                # genre on s'arrête si quelqu'un gagne 4 matchs quand la confrontation se joue sur 7
                # quand un joueur de tennis a gagné 3 sets (2 pour les joueuses)
                # etc
                # MAIS ON S'ARRETE PAS SI UNE EQUIPE A GAGNEE QUE L'ALLER
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
                        res = match_engine.result
                        list_conf.append(res)
                        res.updateClubStats()
                        res.updatePlayerStats()
                    winner = self._determine_tie_winner(m)
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
                        os.mkdir(list_conf[0].home.upper()+"_"+list_conf[0].away.upper())
                        os.chdir(list_conf[0].home.upper()+"_"+list_conf[0].away.upper())
                        for conf_i in range(len(list_conf)):
                            conf = list_conf[conf_i]
                            conf.write(list_conf[:conf_i])
                        os.chdir(new_og_dir)
                    except FileExistsError:
                        print("File already exists; aborting....")
                os.chdir(og_dir)
            except FileExistsError:
                print("File already exists; aborting....")

    def _determine_tie_winner(self, clubs):
        """
           Determines the winner of a tie by applying the round's tie-breakers

           Parameters
           ----------
           clubs : list of Club
                The two clubs to separate

           Returns
           -------
           Team
                The winning club if applicable - none otherwise
        """
        # MODIFY TO HAVE ACTUAL ET/PENS/PLAYOFFS TIE BREAKERS WORKING
        # note: si on fait un playoff, mais le nombre de confrontations est impair
        # jouer le premier playoff pas sur terrain neutre mais chez l'équipe qui a le moins reçu
        winner = None
        i = 0
        while (winner is None) or (i < len(self.tieBreakers)):
            ranking = self.tieBreakers[i].tieBreak(clubs)
            if not isinstance(ranking[0], list):
                winner = ranking[0]
            else:
                winner = clubs[0]
            i += 1
        return winner
