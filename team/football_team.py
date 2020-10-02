"""
Created on Fri Sep 25 2020

File defining a football Team

A subclass of Team, implementing it to represent a team for a Football match

Currently a bit underdeveloped, but could be expanded on later on if the simulation becomes more accurate

@author: alexa
"""

from team.team import Team
from random import choices


class FootballTeam(Team):
    """
            Defines the Team playing in a football match

            Attributes
            ----------
            club : Club
                        The football club who the team represents
            gk : FootballPlayer
                        The goalkeeper
            df : list of FootballPlayer
                        The list of FootballPlayers playing in defence
            md : list of FootballPlayer
                        The list of FootballPlayers playing in midfield
            fw : list of FootballPlayer
                        The list of FootballPlayers playing as forwards
            pen_takers : list of FootballPlayer
                        The list of FootballPlayers who can take a penalty
    """

    def __init__(self, club):
        """
           Initializes the Team from a Club - in short picks up the players who shall play

           Parameters
           ----------
           club : FootballClub
                       The club which needs to select their 11 players for a football match

           Returns
           -------
           FootballTeam
                The initialized FootballTeam, ready to play a match
        """
        super().__init__(club)
        self.gk = None
        self.df = []
        self.md = []
        self.fw = []
        self.pen_takers = []

        tactic = choices(self.club.tactics, weights=[t.weight for t in self.club.tactics], k=1)[0]
        gk_raw_list = []
        df_raw_list = []
        md_raw_list = []
        fw_raw_list = []
        for p in self.club.players:
            if p.positionAbilities[0] > 0:
                gk_raw_list.append(p)
            if p.positionAbilities[1] > 0:
                df_raw_list.append(p)
            if p.positionAbilities[2] > 0:
                md_raw_list.append(p)
            if p.positionAbilities[3] > 0:
                fw_raw_list.append(p)
        tmp_weights = [p.strength * p.positionAbilities[0] for p in gk_raw_list]
        self.gk = choices(gk_raw_list, weights=[w - 0.8*min(tmp_weights) for w in tmp_weights], k=1)[0]
        if self.gk in df_raw_list:
            df_raw_list.remove(self.gk)
        if self.gk in md_raw_list:
            md_raw_list.remove(self.gk)
        if self.gk in fw_raw_list:
            fw_raw_list.remove(self.gk)
        if self.gk.penaltyTaker:
            self.pen_takers.append(self.gk)
        for i_d in range(tactic.nbDf):
            chosen_one = None
            while chosen_one is None:
                tmp_weights = [p.strength * p.positionAbilities[1] for p in df_raw_list]
                chosen_one = choices(df_raw_list, weights=[w - 0.8*min(tmp_weights) for w in tmp_weights], k=1)[0]
                if ((chosen_one in md_raw_list) and (len(md_raw_list) <= tactic.nbMd)) or (chosen_one in fw_raw_list)\
                        and (len(fw_raw_list) <= tactic.nbFw):
                    df_raw_list.remove(chosen_one)
                    chosen_one = None
            self.df.append(chosen_one)
            df_raw_list.remove(self.df[-1])
            if self.df[-1] in md_raw_list:
                md_raw_list.remove(self.df[-1])
            if self.df[-1] in fw_raw_list:
                fw_raw_list.remove(self.df[-1])
            if chosen_one.penaltyTaker:
                self.pen_takers.append(chosen_one)
        for i_m in range(tactic.nbMd):
            chosen_one = None
            while chosen_one is None:
                tmp_weights = [p.strength * p.positionAbilities[2] for p in md_raw_list]
                chosen_one = choices(md_raw_list, weights=[w - 0.8*min(tmp_weights) for w in tmp_weights], k=1)[0]
                if (chosen_one in fw_raw_list) and (len(fw_raw_list) <= tactic.nbFw):
                    md_raw_list.remove(chosen_one)
                    chosen_one = None
            self.md.append(chosen_one)
            md_raw_list.remove(self.md[-1])
            if self.md[-1] in fw_raw_list:
                fw_raw_list.remove(self.md[-1])
            if chosen_one.penaltyTaker:
                self.pen_takers.append(chosen_one)
        for i_d in range(tactic.nbFw):
            tmp_weights = [p.strength * p.positionAbilities[3] for p in fw_raw_list]
            self.fw.append(choices(fw_raw_list, weights=[w - 0.8*min(tmp_weights) for w in tmp_weights], k=1)[0])
            fw_raw_list.remove(self.fw[-1])
            if self.fw[-1].penaltyTaker:
                self.pen_takers.append(self.fw[-1])
        if not self.pen_takers:
            fw_strength = []
            for fw_i in self.fw:
                fw_strength.append((fw_i.strength * fw_i.positionAbilities[3], fw_i))
            self.pen_takers.append(sorted(fw_strength, key=self._first, reverse=True)[0][1])

    def _first(self, _tuple):
        return _tuple[0]
