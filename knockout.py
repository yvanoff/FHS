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
from result.result import ByeResult
from round import Round
from club.club import Bye
from engine.selection import choose_correct_engine
import os
import random as rnd


class Knockout(Round):
    """
        A subtype of Round, representing a knockout format competition

        Attributes
        ----------
        nbRounds : int
                    Number of rounds to be played. If >= 2, the teams in the round 2 or afterwards will be the
                    teams who won in the previous round
        exit_pot: int
                    Teams who qualify from this Knckout round will have this pot

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
        # exit pot for knockout
        super().__init__(sport, round_parameters, nat, tier, engine_cfg_path)
        self.nbRounds = 1
        if 'Play_x_rounds' in round_parameters['Round'].keys():
            self.nbRounds = round_parameters['Round']['Play_x_rounds']  # Number of consecutive rounds to be played
        # extra time type to use if teams are tied
        # possible values are:
        # - "" for no extra time
        # - "normal" for the regular version
        # - "gg" for golden goal
        # - "sg" for silver goal

        self.exit_pot = 0
        if 'Exit_pot' in round_parameters['Round'].keys():
            self.exit_pot = round_parameters['Round']['Exit_pot']
        self.tieBreakers = []
        for tb in round_parameters['Round']['Tie_breakers']:
            self.tieBreakers.append(choose_correct_tb(tb, self))
        self.points = [1, 0, 0]

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
        if list_added_clubs is None:
            list_added_clubs = []
        for ac in list_added_clubs:
            self.clubs.append(ac)
        qualified_clubs = []
        for c in self.clubs:
            c.reset_matches_data()
        self.results = []
        for r in range(self.nbRounds):
            res_round = []
            match_list = self._draw_round((len(self.clubs)+1) // 2)
            qualified_clubs = []
            for m in match_list:
                # s'arrêter si quelqu'un gagne (floor(nb_matches_max/2))+1 matches
                # genre on s'arrête si quelqu'un gagne 4 matchs quand la confrontation se joue sur 7
                # quand un joueur de tennis a gagné 3 sets (2 pour les joueuses)
                # etc
                # MAIS ON S'ARRETE PAS SI UNE EQUIPE A GAGNEE QUE L'ALLER
                list_conf = []
                if not ((type(m[0]) is Bye) or (type(m[1]) is Bye)):
                    for c in range(self.nbConfrontations):
                        if (self.nbConfrontations % 2) == 0:
                            if (c % 2) == 1:
                                home_t, away_t = m
                            else:
                                away_t, home_t = m
                        else:
                            if (c % 2) == 0:
                                home_t, away_t = m
                            else:
                                away_t, home_t = m
                        match_engine = choose_correct_engine(self.sport, self.engineCfgPath, home_t, away_t,
                                                             self.neutralGround)
                        match_engine.simulate_match()
                        res = match_engine.result
                        list_conf.append(res)
                        res.update_club_stats(neutral_ground=self.neutralGround)
                        res.update_player_stats()
                    for t_b in m:
                        t_b.backup_data(self, addition=True)
                    winner = self._determine_tie_winner(m)
                    for t_b in m:
                        t_b.restore_backup(self)
                    qualified_clubs.append(winner)
                else:
                    # potentially store the bye in results to write it later
                    if not (type(m[0]) is Bye):
                        qualified_clubs.append(m[0])
                        list_conf.append(ByeResult(m[0], m[0].name+" was awarded a bye this round"))
                    elif not (type(m[1]) is Bye):
                        qualified_clubs.append(m[1])
                        list_conf.append(ByeResult(m[1], m[1].name + " was awarded a bye this round"))
                    else:
                        print("Error with the number of teams !")  # would be better to have an exception
                res_round.append(list_conf)
            # and then the list of teams is replaced by qualified_teams for the next
            self.results.append(res_round)
            for qt in qualified_clubs:
                qt.pot = 0
                qt.exit_group = -1
            self.clubs = qualified_clubs
        for c in qualified_clubs:
            c.pot = self.exit_pot
            c.reset_matches_data()
        return qualified_clubs

    def write(self, nat=None, tier=None):
        """
               Writes a knockout round's results

               Parameters
               ----------
               nat : bool
                    Should the nationality appear in match reports
               tier : bool
                    Should the club's tier appear in match reports
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
                        if type(list_conf[0]) is ByeResult:
                            list_conf[0].write()
                        else:
                            write_ht, write_at = list_conf[0].score.keys()
                            os.mkdir(write_ht.club.name.upper()+"_"+write_at.club.name.upper())
                            os.chdir(write_ht.club.name.upper()+"_"+write_at.club.name.upper())
                            for conf_i in range(len(list_conf)):
                                conf = list_conf[conf_i]
                                conf.write(nat=nat, tier=tier, prev_m=list_conf[:conf_i])
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
        while (winner is None) and (i < len(self.tieBreakers)):
            ranking = self.tieBreakers[i].tie_break(clubs)
            if not isinstance(ranking[0], list):
                winner = ranking[0]
            else:
                winner = clubs[0]
            i += 1
        if winner is None:
            winner = rnd.choice(clubs)
        return winner
    # tie breaker criteria needed for knockout:
    # - number of wins (is number of points with [1,0,0]
    # - goal difference
    # - number of goals scored away
    # - extra time (gg/sg/normal)
    # - x replays (on neutral ground or not)
    # - pen shootout
    # - coin toss

    # pour les playoffs:
    # mettre genre "5playoffs" ou "infplayoffs" dans le json
    # on applique le playoffs x fois
    # en réappliquant les cirtères précédants si il faut
    # eg is on a "win", "diff", "goalscoredaway", "normalET", "5playoff" on aura 5 playoffs avec prolongations normales
    # suffit de rajouter "tab" derrière si on veut des tabs après un certain nombre de tabs
    # tab et prolongations s'appliquent au dernier résultat en mémoire (puisque ça doit être le match courant)
