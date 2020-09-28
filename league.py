"""
Created on Fri Sep 25 2020

File defining the League subclass of the Round class

This defines a League kind of round. Basically the idea is simple: there are N teams which will play this round, they
will play each other and at the end a ranking will be computed, with the best teams (exact number being a class
attribute) progressing.

Note that teams may be spread out in several smaller leagues at once, which will be played in parallel. For example,
the UEFA Champions League has a group stage: 32 teams are spread out in 8 groups of 4 teams, with the best two teams
of each group progressing. This is a League kind of Round

@author: alexa
"""

from tiebreaker.tiebreakers import choose_correct_tb, HardcodedTiebreaker
from round import Round
from club.club import Bye
from engine.engine import choose_correct_engine


# pour les conf directes on fait une backup des stats des équipes à égalité, on wipe, et on les recalcule sur les confs
# directes
# puis on rétabli les valeurs originales
# pour éviter que le make_table prenne en compte des résultats qui ne se sont pas encore produits avec tableEachRound
# et les confrontations directs
# mais en fait on peut retrouver le nb de matchs joués à partir du nbWin/nbDraw/nbLosses donc c bon


class League(Round):
    """
        A subtype of Round, representing a league format competition

        Attributes
        ----------
        points : list of int
                    Number of points gained for a victory, a draw, a loss
        nbGroups : int
                    Number of groups (leagues to be simulated)
        tableEachRound : bool
                    Flag indicating if a temporary table should be written after each round
        nbAdvancing : int
                    Number of teams advancing from the league(s)
        potForAdvancing : bool
                    Flag indicating if qualified teams should have a pot (equal to their final ranking) affected to them
        table : list of list of Teams
                    The teams classified from top to bottom according to their results (each league being a separate list)
        Methods
        -------
        _make_schedule : list of Team -> int -> list of list of Team
                    Returns a schedule for a group, with each team playing each other n times (n being a parameter)
        _make_table : list of Team -> list of Tiebreaker -> list of Team
                    Returns the league table (teams ordered in a list from top to bottom of the table)
    """

    def __init__(self, sport, round_parameters, nat, tier, engine_cfg_path):
        """
           Initializes a league from the adequate part of a competition JSON file

           Parameters
           ----------
           round_parameters : dict
                       The dict containing the round data
           nat : bool
                        Flag indicating if the teams's nationalities matter for this round or not
           tier : bool
                        Flag indicating whether the teams's tiers matter for this round or not
           engine_cfg_path : str
                        Path to the Engine configuration file to be used for this round

           Returns
           -------
           League
                The initialized League object
        """
        super().__init__(sport, round_parameters, nat, tier, engine_cfg_path)
        self.nbGroups = round_parameters['League']['Nb_groups']
        self.tieBreakers = []
        for tb in round_parameters['League']['Tie_breakers']:
            self.tieBreakers.append(choose_correct_tb(tb))
        self.tableEachRound = round_parameters['League']['Table_each_round']
        self.points = round_parameters['League']['Points_per_result']
        self.nbAdvancing = round_parameters['League']['Nb_qualified']
        self.potForAdvancing = round_parameters['League']['Pots_for_qualified_teams']
        self.table = []

        if 'Is_nationality_important' in round_parameters['League'].keys():
            self.isNatImp = round_parameters['League']['Is_nationality_important']
        if 'Is_club_level_important' in round_parameters['League'].keys():
            self.isTierImp = round_parameters['League']['Is_club_level_important']

    def simulate(self, list_added_clubs=None):
        """
           Simulates the round according to league rules

           Parameters
           ----------
           list_added_clubs : list of Club
                List of clubs to be added to this round

           Returns
           -------
           list of Club
                List of qualified clubs after this round
        """
        # Init vars (making sure no leftover data pollutes everything)
        # and drawing the teams in groups
        if list_added_clubs is None:
            list_added_clubs = []
        for ac in list_added_clubs:
            self.clubs.append(ac)
        qualified_clubs = []
        groups = self._draw_round(self.clubs, self.nbGroups, self.isNatImp)

        # for each group we make a schedule and play each match in it
        # after each match we update the stats which need updating
        # and then we make the table for each group and save the teams qualified
        for g in groups:
            group_results = []
            schedule = self._make_schedule(g, self.nbConfrontations)
            for matchday in schedule:
                matchday_results = []
                for match in matchday:
                    if not ((type(match[0]) is Bye) or (type(match[1]) is Bye)):
                        match_engine = choose_correct_engine(self.sport, self.engineCfgPath, match[0], match[1],
                                                             self.neutralGround)
                        match_engine.simulateMatch()
                        res = match_engine.getResult()
                        matchday_results.append(res)
                        res.updateClubStats(self.points)
                        res.updatePlayerStats()
                group_results.append(matchday_results)
            league_table = self._make_table(g, 0)
            self.table.append(league_table)
            for c in range(self.nbAdvancing):
                qualified_clubs.append(league_table[c])
                if self.potForAdvancing:
                    league_table[c].updatePot(c)
                else:
                    league_table[c].resetPot()
            self.results.append(group_results)
        return qualified_clubs

    def write(self):
        """
               Writes a league's results
        """
        # it's just about parsing self.results and writing them all in the good sub-folder
        # then write the league table at the end
        # if self.tableEachRound requires it, we need to compute the table for each matchday
        pass

    def _make_schedule(self, group, nb_confrontations):
        """
           Makes a schedule for a group of Team

           Parameters
           ----------
           group : list of Club
                List of clubs which need a schedule
            nb_confrontations : int
                The number of times teams play each other

           Returns
           -------
           list of list of Club
                The schedule ready to use
        """
        schedule = []

        for i in range(len(group) - 1):
            middle = int(len(group) / 2)
            first_half = group[:middle]
            second_half = group[middle:]
            second_half.reverse()
            matches_list = []

            parity = (i % 2 == 0)
            for c1, c2 in zip(first_half, second_half):
                index = first_half.index(c1)
                if index == 0:
                    if parity:
                        matches_list.append((c1, c2))
                    else:
                        matches_list.append((c2, c1))
                else:
                    inversion = (index % 2) == 0
                    if inversion:
                        matches_list.append((c2, c1))
                    else:
                        matches_list.append((c1, c2))
            schedule.append(matches_list)
            group.insert(1, group.pop())

        for i in range(nb_confrontations-1):
            schedule_added = []
            for matchday in schedule:
                reversed_matchday = []
                for m in matchday:
                    reversed_matchday.append((m[1],m[0]))
                schedule_added.append(reversed_matchday)
            for j in schedule_added:
                schedule.append(j)

        return schedule

    def _make_table(self, clubs, tiebreaker_used):
        """
           Makes a table ranking the teams from first to last

           Parameters
           ----------
           clubs : list of Club
                Lis of Club to rank

           Returns
           -------
           list of Club
                The clubs ranked according to the tie breakers
        """
        tmp_table = []
        if not isinstance(self.tieBreakers[tiebreaker_used], HardcodedTiebreaker):
            tmp_table = self.tieBreakers[tiebreaker_used].tieBreak(clubs)
        else:
            if self.tieBreakers[tiebreaker_used].name == 'conf-points':
                tmp_table = self._conf_points(clubs)
            elif (self.tieBreakers[tiebreaker_used].name.split('-')[0] == 'playoff') and (len(clubs) == 2):
                # play a playoff match with et and pen parameters after the -
                tmp_table = self._play_playoff(clubs, self.tieBreakers[tiebreaker_used].name)
            else:
                tmp_table = [clubs]
        final_table = []
        for group in tmp_table:
            if isinstance(group, list):
                if (tiebreaker_used+1) < len(self.tieBreakers):
                    broken_group = self._make_table(group, tiebreaker_used+1)
                else:
                    broken_group = group
                for t in broken_group:
                    final_table.append(t)
            else:
                final_table.append(group)

        return final_table
