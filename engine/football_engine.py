"""
Created on Fri Sep 25 2020

Implementation of the Engine class in the case of Football (also known as Calcio/Soccer/Fussball)

It will implement Engine for a Football match, so that a football match between two football teams can be simulated

@author: alexa
"""

from engine.engine import Engine
from engine.ecfg.football_ecfg import FootballECfg
from team.football_team import FootballTeam
from result.football_result import FootballResult
import random as rnd
import math


class FootballEngine(Engine):
    """
            Defines an Engine implementation for a Football Club. No changes in terms of attributes, it's mostly
            the implementation of the methods which is interesting

            Attributes
            ----------
            parameters : FootballECfg
                        The engine parameters. The class is specific to Football, and is designed for use with
                        a FootballEngine
            neutralGround : bool
                        Flag indicating if the match is played on neutral ground or not
            homeTeamPlayers : Team
                        The players for the home team
            awayTeamPlayers : Team
                        The players for the away team
            result : FootballResult
                        The match's result. It's a football match's result

            Methods
            -------
            simulateMatch : None -> None
                    Plays a 90-minutes long football match with both team's data, saves the result in the corresponding
                    attribute
            simulateExtraTime : str -> None
                    Plays 30 minutes of extra time according to the rules passed in Parameters, and updates the result
            simulateShootout : None -> None
                    Simulates a penalty shoutoot and updates the result with its conclusion. Specific to FootballEngine
                    since a lot of sports don't have shootouts in case of ties
            getResult : None -> FootballResult
                    Returns the match's result
    """

    def __init__(self, config_path, home_team, away_team, neutral_ground=False):
        """
           Initializes the engine from the configuration, home/away teams data and neutral ground bool

           Parameters
           ----------
           config_path : str
                       Path to the Engine configuration file to load
           home_team : FootballClub
                        Data for the home team
           away_team : FootballClub
                        Data for the away team
           neutral_ground : bool
                        Flag indicating if the match takes place on neutral ground

           Returns
           -------
           FootballEngine
                The initialized FootballEngine
        """
        self.parameters = FootballECfg(config_path)
        self.neutralGround = neutral_ground
        self.homeTeamPlayers = FootballTeam(home_team)
        self.awayTeamPlayers = FootballTeam(away_team)
        self.result = FootballResult(self.homeTeamPlayers, self.awayTeamPlayers)

    def simulate_match(self):
        """
           Simulates a football match between two teams, and stores the result of the match in the result attribute
        """

        home_bonus = 1.0 if self.neutralGround else self.parameters.bonusHome

        # STATS OF THE TEAMS
        home_team_stats = {'gk_raw_strength': self.homeTeamPlayers.gk.strength *
                           self.homeTeamPlayers.gk.positionAbilities[0],
                           'df_raw_strength': sum([p.strength * p.positionAbilities[1] for p in self.homeTeamPlayers.df]),
                           'mid_raw_strength': sum([p.strength * p.positionAbilities[2] for p in self.homeTeamPlayers.md]),
                           'fw_raw_strength': sum([p.strength * p.positionAbilities[3] for p in self.homeTeamPlayers.fw])
                           }

        away_team_stats = {'gk_raw_strength': self.awayTeamPlayers.gk.strength *
                           self.awayTeamPlayers.gk.positionAbilities[0],
                           'df_raw_strength': sum([p.strength * p.positionAbilities[1] for p in self.awayTeamPlayers.df]),
                           'mid_raw_strength': sum([p.strength * p.positionAbilities[2] for p in self.awayTeamPlayers.md]),
                           'fw_raw_strength': sum([p.strength * p.positionAbilities[3] for p in self.awayTeamPlayers.fw])
                           }

        # COMPUTATION OF SECONDARY STATIS



        # THE BATTLE FOR MIDFIELD

        # the strength in midfield is an average of the midfielders's talents and the proportion of players in midfield
        # who play for the home team (respectively the away team)
        avg_mid_strength = home_team_stats['mid_raw_strength'] / len(self.homeTeamPlayers.md)
        mid_overrun_prop = len(self.homeTeamPlayers.md) / (len(self.homeTeamPlayers.md) + len(self.awayTeamPlayers.md))
        home_team_stats['mid_strength'] = home_bonus * (avg_mid_strength + (mid_overrun_prop * 100)) / 2

        avg_mid_strength = away_team_stats['mid_raw_strength'] / len(self.awayTeamPlayers.md)
        mid_overrun_prop = len(self.awayTeamPlayers.md) / (len(self.homeTeamPlayers.md) + len(self.awayTeamPlayers.md))
        away_team_stats['mid_strength'] = (avg_mid_strength + (mid_overrun_prop * 100)) / 2

        cum_mid = home_team_stats['mid_strength'] + away_team_stats['mid_strength']
        # a rng value will be generated later on, and we'll compare its value to this value to determine if the home
        # team or the away team have the ball
        mid_tipping_point = ((home_team_stats['mid_strength'] / cum_mid + 0.5) ** 6) / 2



        # THEN THE STRENGTH OF THE TWO TEAMS TO ATTACK WITH A POSSESSION SEQUENCE
        # This refers to an attack where the team monopolizes the ball and tries to break down the other team
        # the other team, not having the ball, will be focusing on defending

        # players in midfield also help a bit in these attacking sequences so their talent is taken in account
        full_fw_strength = (2 / 3) * (home_team_stats['fw_raw_strength']/len(self.homeTeamPlayers.fw)) +\
                           (1 / 3) * (home_team_stats['mid_raw_strength']/len(self.homeTeamPlayers.md))
        # then we compute how many players are attacking (for the home team, here) and how many are defending
        # some midfielders will come forward to help the home team attack
        # likewise some midfielders will drop down to help the away team defend
        fw_nb_strength = (len(self.homeTeamPlayers.fw) + (len(self.homeTeamPlayers.md) / 2)) /\
                         (len(self.homeTeamPlayers.fw) + len(self.awayTeamPlayers.df) +
                          (len(self.homeTeamPlayers.md) / 2) + (len(self.awayTeamPlayers.md) / 2))

        # the full attack strength is a mix of the talent and the proportion of players attacking compared to
        # those defending
        home_team_stats['fw_poss_strength'] = home_bonus * (full_fw_strength + (100 * fw_nb_strength)) / 2

        # same reasoning with the away team attacking and the home team defending
        full_fw_strength = (2 / 3) * (away_team_stats['fw_raw_strength']/len(self.awayTeamPlayers.fw)) +\
                           (1 / 3) * (away_team_stats['mid_raw_strength']/len(self.awayTeamPlayers.md))
        fw_nb_strength = (len(self.awayTeamPlayers.fw) + (len(self.awayTeamPlayers.md) / 2)) /\
                         (len(self.awayTeamPlayers.fw) + len(self.homeTeamPlayers.df) +
                          (len(self.homeTeamPlayers.md) / 2) + (len(self.awayTeamPlayers.md) / 2))

        away_team_stats['fw_poss_strength'] = (full_fw_strength + (100 * fw_nb_strength)) / 2



        # STRENGTH OF EACH TEAM ON THE COUNTER
        # Now something that happens often in football is the counter
        # It happens when a team is attacking, but loses the ball
        # Since the team was attacking, its players were forward on the pitch: there's not a lot of players defending
        # so it's a great opportunity for the team who wins the ball to score a goal
        # with a caveat: because the team who just won the ball was defending, most of its players are in defence still
        # in short only a few players (usually very quick) can attack

        # the reasoning will be the same as for attacks with the ball, except the midfielders will be less
        # important here because they'll likely not be positioned at the good place to contribute to defence/attack
        full_fw_strength = (3 / 4) * (home_team_stats['fw_raw_strength']/len(self.homeTeamPlayers.fw)) +\
                           (1 / 4) * (home_team_stats['mid_raw_strength']/len(self.homeTeamPlayers.md))
        fw_nb_strength = ((len(self.homeTeamPlayers.fw) / 2) + (len(self.homeTeamPlayers.md) / 3)) /\
                         ((len(self.homeTeamPlayers.fw) / 2) + (len(self.awayTeamPlayers.df) / 2) +
                          (len(self.homeTeamPlayers.md) / 3) + (len(self.awayTeamPlayers.md) / 3))

        home_team_stats['fw_counter_strength'] = home_bonus * (full_fw_strength + (100 * fw_nb_strength)) / 2

        full_fw_strength = (3 / 4) * (away_team_stats['fw_raw_strength']/len(self.awayTeamPlayers.fw)) +\
                           (1 / 4) * (away_team_stats['mid_raw_strength']/len(self.awayTeamPlayers.md))
        fw_nb_strength = ((len(self.awayTeamPlayers.fw) / 2) + (len(self.awayTeamPlayers.md) / 3)) /\
                         ((len(self.awayTeamPlayers.fw) / 2) + (len(self.homeTeamPlayers.df) / 2) +
                          (len(self.homeTeamPlayers.md) / 3) + (len(self.awayTeamPlayers.md) / 3))

        away_team_stats['fw_counter_strength'] = (full_fw_strength + (100 * fw_nb_strength)) / 2



        # NOW WE NEED TO KNOW HOW WELL EACH TEAM DEFEND
        # FIRST, HOW DO THEY DEFEND AGAINST POSSESSION ATTACKS
        # general principle is the same as for attacks but reversed
        full_df_strength = (2 / 3) * (home_team_stats['df_raw_strength']/len(self.homeTeamPlayers.df)) +\
                           (1 / 3) * (home_team_stats['mid_raw_strength']/len(self.homeTeamPlayers.md))
        df_nb_strength = (len(self.homeTeamPlayers.df) + (len(self.homeTeamPlayers.md) / 2)) /\
                         (len(self.homeTeamPlayers.df) + len(self.awayTeamPlayers.fw) +
                          (len(self.homeTeamPlayers.md) / 2) + (len(self.awayTeamPlayers.md) / 2))

        home_team_stats['df_poss_strength'] = home_bonus * (full_df_strength + (100 * df_nb_strength)) / 2

        full_df_strength = (2 / 3) * (away_team_stats['df_raw_strength']/len(self.awayTeamPlayers.df)) +\
                           (1 / 3) * (away_team_stats['mid_raw_strength']/len(self.awayTeamPlayers.md))
        df_nb_strength = (len(self.awayTeamPlayers.df) + (len(self.awayTeamPlayers.md) / 2)) /\
                         (len(self.awayTeamPlayers.df) + len(self.homeTeamPlayers.fw) +
                          (len(self.homeTeamPlayers.md) / 2) + (len(self.awayTeamPlayers.md) / 2))

        away_team_stats['df_poss_strength'] = (full_df_strength + (100 * df_nb_strength)) / 2



        # DEFENSE STRENGTH AGAINST COUNTER ATTACKS
        full_df_strength = (3 / 4) * (home_team_stats['df_raw_strength']/len(self.homeTeamPlayers.df)) +\
                           (1 / 4) * (home_team_stats['mid_raw_strength']/len(self.homeTeamPlayers.md))
        df_nb_strength = ((len(self.homeTeamPlayers.df) / 2) + (len(self.homeTeamPlayers.md) / 3)) /\
                         ((len(self.homeTeamPlayers.df) / 2) + (len(self.awayTeamPlayers.fw) / 2) +
                          (len(self.homeTeamPlayers.md) / 3) + (len(self.awayTeamPlayers.md) / 3))

        home_team_stats['df_counter_strength'] = home_bonus * (full_df_strength + (100 * df_nb_strength)) / 2

        full_df_strength = (3 / 4) * (away_team_stats['df_raw_strength']/len(self.awayTeamPlayers.df)) +\
                           (1 / 4) * (away_team_stats['mid_raw_strength']/len(self.awayTeamPlayers.md))
        df_nb_strength = ((len(self.awayTeamPlayers.df) / 2) + (len(self.awayTeamPlayers.md) / 3)) /\
                         ((len(self.awayTeamPlayers.df) / 2) + (len(self.homeTeamPlayers.fw) / 2) +
                          (len(self.homeTeamPlayers.md) / 3) + (len(self.awayTeamPlayers.md) / 3))

        away_team_stats['df_counter_strength'] = (full_df_strength + (100 * df_nb_strength)) / 2



        # SHOOTING STRENGTH FOR BOTH TEAMS
        shoot_poss_str = len(self.homeTeamPlayers.fw) /\
                            (len(self.homeTeamPlayers.fw) + len(self.awayTeamPlayers.df) + 1)
        shoot_counter_str = len(self.homeTeamPlayers.fw) /\
                               (len(self.homeTeamPlayers.fw) + (len(self.awayTeamPlayers.df) / 2) + 1)

        home_team_stats['shoot_poss_strength'] =\
            home_bonus * ((home_team_stats['fw_raw_strength']/len(self.homeTeamPlayers.fw)) + (100 * shoot_poss_str))/2
        home_team_stats['shoot_counter_strength'] =\
            home_bonus * ((home_team_stats['fw_raw_strength']/len(self.homeTeamPlayers.fw)) + (100*shoot_counter_str))/2

        shoot_poss_str = len(self.awayTeamPlayers.fw) /\
                            (len(self.awayTeamPlayers.fw) + len(self.homeTeamPlayers.df) + 1)
        shoot_counter_str = len(self.awayTeamPlayers.fw) /\
                               (len(self.awayTeamPlayers.fw) + (len(self.homeTeamPlayers.df) / 2) + 1)

        away_team_stats['shoot_poss_strength'] =\
            (away_team_stats['fw_raw_strength']/len(self.awayTeamPlayers.fw) + (100 * shoot_poss_str)) / 2
        away_team_stats['shoot_counter_strength'] =\
            (away_team_stats['fw_raw_strength']/len(self.awayTeamPlayers.fw) + (100 * shoot_counter_str)) / 2



        # STRENGTH OF EACH TEAM'S GK

        # AGAINST POSSESSION ATTACKS
        gk_strength = (2 / 3) * home_team_stats['gk_raw_strength'] +\
                      (1 / 3) * (home_team_stats['df_raw_strength']/len(self.homeTeamPlayers.df))
        nb_gk_strength = (1 + len(self.homeTeamPlayers.df)) /\
                         (1 + len(self.homeTeamPlayers.df) + len(self.awayTeamPlayers.fw))

        home_team_stats['gk_poss_strength'] = home_bonus * (gk_strength + (100 * nb_gk_strength)) / 2

        gk_strength = (2 / 3) * away_team_stats['gk_raw_strength'] +\
                      (1 / 3) * (away_team_stats['df_raw_strength']/len(self.awayTeamPlayers.df))
        nb_gk_strength = (1 + len(self.awayTeamPlayers.df)) /\
                         (1 + len(self.awayTeamPlayers.df) + len(self.homeTeamPlayers.fw))

        away_team_stats['gk_poss_strength'] = (gk_strength + (100 * nb_gk_strength)) / 2

        # AND AGAINST COUNTER ATTACKS
        gk_strength = (3 / 4) * home_team_stats['gk_raw_strength'] +\
                      (1 / 4) * (home_team_stats['df_raw_strength']/len(self.homeTeamPlayers.df))
        nb_gk_strength = (1 + (len(self.homeTeamPlayers.df) / 2)) /\
                         (1 + (len(self.homeTeamPlayers.df) / 2) + len(self.awayTeamPlayers.fw))

        home_team_stats['gk_counter_strength'] = home_bonus * (gk_strength + (100 * nb_gk_strength)) / 2

        gk_strength = (3 / 4) * away_team_stats['gk_raw_strength'] +\
                      (1 / 4) * (away_team_stats['df_raw_strength']/len(self.awayTeamPlayers.df))
        nb_gk_strength = (1 + (len(self.awayTeamPlayers.df) / 2)) /\
                         (1 + (len(self.awayTeamPlayers.df) / 2) + len(self.homeTeamPlayers.fw))

        away_team_stats['gk_counter_strength'] = (gk_strength + (100 * nb_gk_strength)) / 2



        # AND NOW WE CAN COMPUTE PROBABILITIES OF GETTING A SHOT OUT OF A POSSESSION SPELL/COUNTER ATTACK
        # AND THE PROBABILITY OF EACH SHOT OF GOING IN
        home_team_stats['nb_shots_poss'] =\
            max(0.1, 1 + math.log(home_team_stats['fw_poss_strength'] /
                                  (home_team_stats['fw_poss_strength'] + away_team_stats['df_poss_strength'])))

        home_team_stats['prob_goal_poss'] =\
            home_team_stats['shoot_poss_strength'] /\
            (home_team_stats['shoot_poss_strength'] + away_team_stats['gk_poss_strength'])

        home_team_stats['nb_shots_counter'] =\
            max(0.1, 1 + math.log(home_team_stats['fw_counter_strength'] /
                                  (home_team_stats['fw_counter_strength'] + away_team_stats['df_counter_strength'])))

        home_team_stats['prob_goal_counter'] =\
            home_team_stats['shoot_counter_strength'] /\
            (home_team_stats['shoot_counter_strength'] + away_team_stats['gk_counter_strength'])


        away_team_stats['nb_shots_poss'] =\
            max(0.1, 1 + math.log(away_team_stats['fw_poss_strength'] /
                                  (away_team_stats['fw_poss_strength'] + home_team_stats['df_poss_strength'])))

        away_team_stats['prob_goal_poss'] =\
            away_team_stats['shoot_poss_strength'] /\
            (away_team_stats['shoot_poss_strength'] + home_team_stats['gk_poss_strength'])

        away_team_stats['nb_shots_counter'] =\
            max(0.1, 1 + math.log(away_team_stats['shoot_counter_strength'] /
                                  (away_team_stats['shoot_counter_strength'] + home_team_stats['df_counter_strength'])))

        away_team_stats['prob_goal_counter'] =\
            away_team_stats['shoot_counter_strength'] /\
            (away_team_stats['shoot_counter_strength'] + home_team_stats['gk_counter_strength'])


        # DEFINING THE TIME AND HERE WE GO
        full_time = [range(0, 50, 5), range(0, 50, 5)]
        half_time = 0

        for half in full_time:
            for time in half:
                who_dominates = rnd.random()
                dominator = self.homeTeamPlayers
                counter = self.awayTeamPlayers
                if who_dominates > mid_tipping_point:
                    dominator = self.awayTeamPlayers
                    counter = self.homeTeamPlayers
                self.result.domination[dominator] += 1
                if dominator is self.homeTeamPlayers:
                    nb_shots_poss = round(abs(rnd.random() - 0.5) * home_team_stats['nb_shots_poss'] * 10)
                    nb_shots_counter = round(abs(rnd.random() - 0.5) * away_team_stats['nb_shots_counter'] * 5)
                else:
                    nb_shots_poss = round(abs(rnd.random() - 0.5) * away_team_stats['nb_shots_poss'] * 10)
                    nb_shots_counter = round(abs(rnd.random() - 0.5) * home_team_stats['nb_shots_counter'] * 5)
                self.result.nbShots[dominator] += nb_shots_poss
                self.result.nbShots[counter] += nb_shots_counter
                minutes = []
                for m in range(1, 6):
                    minutes.append(m + time + half_time)
                for i in range(0, nb_shots_poss):
                    if dominator is self.homeTeamPlayers:
                        is_goal = rnd.random() <= home_team_stats['prob_goal_poss'] ** self.parameters.penaltyTerm
                    else:
                        is_goal = rnd.random() <= away_team_stats['prob_goal_poss'] ** self.parameters.penaltyTerm
                    if is_goal:
                        goal_nature = rnd.random()
                        og = goal_nature <= self.parameters.ogProb
                        pen = False
                        goalscorer_pos = rnd.random()
                        if og:
                            if dominator is self.homeTeamPlayers:
                                if goalscorer_pos <= 1 / 11:
                                    goalscorer = self.awayTeamPlayers.gk
                                elif (goalscorer_pos > 1 / 11) and \
                                        (goalscorer_pos <= (1 + len(self.awayTeamPlayers.df)) / 11):
                                    goalscorer = rnd.choice(self.awayTeamPlayers.df)
                                elif (goalscorer_pos > (1 + len(self.awayTeamPlayers.df)) / 11) and\
                                        (goalscorer_pos <= (1 + len(self.awayTeamPlayers.df) +
                                                           len(self.awayTeamPlayers.md)) / 11):
                                    goalscorer = rnd.choice(self.awayTeamPlayers.md)
                                else:
                                    goalscorer = rnd.choice(self.awayTeamPlayers.fw)
                            else:
                                if goalscorer_pos <= 1 / 11:
                                    goalscorer = self.homeTeamPlayers.gk
                                elif (goalscorer_pos > 1 / 11) and \
                                        (goalscorer_pos <= (1 + len(self.homeTeamPlayers.df)) / 11):
                                    goalscorer = rnd.choice(self.homeTeamPlayers.df)
                                elif (goalscorer_pos > (1 + len(self.homeTeamPlayers.df)) / 11) and\
                                        (goalscorer_pos <= (1 + len(self.homeTeamPlayers.df) +
                                                           len(self.homeTeamPlayers.md)) / 11):
                                    goalscorer = rnd.choice(self.homeTeamPlayers.md)
                                else:
                                    goalscorer = rnd.choice(self.homeTeamPlayers.fw)
                        else:
                            pen = goal_nature <= (self.parameters.penProb + self.parameters.ogProb)
                            if pen:
                                if dominator is self.homeTeamPlayers:
                                    goalscorer = rnd.choice(self.homeTeamPlayers.pen_takers)
                                else:
                                    goalscorer = rnd.choice(self.awayTeamPlayers.pen_takers)
                            else:
                                if dominator is self.homeTeamPlayers:
                                    goal_fw = (1.5 * len(self.homeTeamPlayers.fw) / 5)
                                    if goalscorer_pos < goal_fw:
                                        goalscorer = rnd.choice(self.homeTeamPlayers.fw)
                                    elif goalscorer_pos >= 1 - ((1 - goal_fw) / 3):
                                        goalscorer = rnd.choice(self.homeTeamPlayers.df)
                                    else:
                                        goalscorer = rnd.choice(self.homeTeamPlayers.md)
                                else:
                                    goal_fw = (1.5 * len(self.awayTeamPlayers.fw) / 5)
                                    if goalscorer_pos < goal_fw:
                                        goalscorer = rnd.choice(self.awayTeamPlayers.fw)
                                    elif goalscorer_pos >= 1 - ((1 - goal_fw) / 3):
                                        goalscorer = rnd.choice(self.awayTeamPlayers.df)
                                    else:
                                        goalscorer = rnd.choice(self.awayTeamPlayers.md)
                        chosen_minute = rnd.choice(minutes)
                        minutes.remove(chosen_minute)
                        if not minutes:
                            for m in range(1, 6):
                                minutes.append(m + time + half_time)
                        if (half_time == 0 and chosen_minute > 45) or (half_time == 45 and chosen_minute > 90):
                            if half_time == 0:
                                added_time = chosen_minute - 45
                                chosen_minute = 45
                            else:
                                added_time = chosen_minute - 90
                                chosen_minute = 90
                            self.result.add_goal(dominator, goalscorer, og, pen, chosen_minute, added_time)
                        else:
                            self.result.add_goal(dominator, goalscorer, og, pen, chosen_minute)
                for j in range(0, nb_shots_counter):
                    if counter is self.homeTeamPlayers:
                        is_goal = rnd.random() <= home_team_stats['prob_goal_counter'] ** self.parameters.penaltyTerm
                    else:
                        is_goal = rnd.random() <= away_team_stats['prob_goal_counter'] ** self.parameters.penaltyTerm
                    if is_goal:
                        goal_nature = rnd.random()
                        og = goal_nature <= self.parameters.ogProb
                        pen = False
                        goalscorer_pos = rnd.random()
                        if og:
                            goalscorer_pos = rnd.random()
                            if counter is self.homeTeamPlayers:
                                if goalscorer_pos <=\
                                        1 / (len(self.awayTeamPlayers.df) + (len(self.awayTeamPlayers.md) / 2)):
                                    goalscorer = self.awayTeamPlayers.gk
                                elif goalscorer_pos >\
                                        (len(self.awayTeamPlayers.md) / 2) /\
                                        (len(self.awayTeamPlayers.df) + (len(self.awayTeamPlayers.md) / 2)):
                                    goalscorer = rnd.choice(self.awayTeamPlayers.md)
                                else:
                                    goalscorer = rnd.choice(self.awayTeamPlayers.df)
                            else:
                                if goalscorer_pos <=\
                                        1 / (len(self.homeTeamPlayers.df) + (len(self.homeTeamPlayers.md) / 2)):
                                    goalscorer = self.homeTeamPlayers.gk
                                elif goalscorer_pos >\
                                        (len(self.homeTeamPlayers.md) / 2) /\
                                        (len(self.homeTeamPlayers.df) + (len(self.homeTeamPlayers.md) / 2)):
                                    goalscorer = rnd.choice(self.homeTeamPlayers.md)
                                else:
                                    goalscorer = rnd.choice(self.homeTeamPlayers.df)
                        else:
                            pen = goal_nature <= (self.parameters.penProb + self.parameters.ogProb)
                            if pen:
                                if counter is self.homeTeamPlayers:
                                    goalscorer = rnd.choice(self.homeTeamPlayers.pen_takers)
                                else:
                                    goalscorer = rnd.choice(self.awayTeamPlayers.pen_takers)
                            else:
                                if counter is self.homeTeamPlayers:
                                    goal_fw = 2 * len(self.homeTeamPlayers.fw) / 5
                                    if goalscorer_pos < goal_fw:
                                        goalscorer = rnd.choice(self.homeTeamPlayers.fw)
                                    elif goalscorer_pos >= 1 - ((1 - goal_fw) / 6):
                                        goalscorer = rnd.choice(self.homeTeamPlayers.df)
                                    else:
                                        goalscorer = rnd.choice(self.homeTeamPlayers.md)
                                else:
                                    goal_fw = 2 * len(self.awayTeamPlayers.fw) / 5
                                    if goalscorer_pos < goal_fw:
                                        goalscorer = rnd.choice(self.awayTeamPlayers.fw)
                                    elif goalscorer_pos >= 1 - ((1 - goal_fw) / 6):
                                        goalscorer = rnd.choice(self.awayTeamPlayers.df)
                                    else:
                                        goalscorer = rnd.choice(self.awayTeamPlayers.md)
                        chosen_minute = rnd.choice(minutes)
                        minutes.remove(chosen_minute)
                        if not minutes:
                            for m in range(1, 6):
                                minutes.append(m + time + half_time)
                        if (half_time == 0 and chosen_minute > 45) or (half_time == 45 and chosen_minute > 90):
                            if half_time == 0:
                                added_time = chosen_minute - 45
                                chosen_minute = 45
                            else:
                                added_time = chosen_minute - 90
                                chosen_minute = 90
                            self.result.add_goal(counter, goalscorer, og, pen, chosen_minute, added_time)
                        else:
                            self.result.add_goal(counter, goalscorer, og, pen, chosen_minute)
            half_time = 45
