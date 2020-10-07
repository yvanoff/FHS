"""
Created on Sat Sep 12 2020

Subclass of the Result class, defining a Football's match results.

Also contains Goal and ResPenShootout class, which are used to define a Football match's results

@author: alexa
"""

from result.result import Result
import os


class FootballResult(Result):
    """
            Defines a football match's results.

            Attributes
            ----------
            score : dict of (FootballTeam, int)
                        Tuple containing the number of goals scored by the home and away team respectively
            goals : dict of list of Goal
                        dict of two elements: the list of Goals scored by the home team, and the list of Goals scored by
                        the away team. Each list can be found by their key: the scoring team.
            penShootout : ResPenShootout
                        The result of a penalty shootout if one took place (a possibility in football)
            domination : dict of list of int
                        A dict which stores for each team (the teams being the dict's keys) the number of domination
                        sequences. Useful to pan out how the match went
            nbShots : dict of list of int
                        A dict which stores for each team (the teams being the dict's keys) the number of attempted
                        shots. Useful to pan out how the match unfolded.

            Methods
            -------
            add_goal : -> None
                        Adds a goal scored to the list of goals
    """

    def __init__(self, home_team, away_team):
        """
           Initializes the FootballResult with the basic values - a football match starts at 0-0 with no goals being scored

           Parameters
           ----------
           home_team : FootballTeam
                       The team data for the home team
           away_team : FootballTeam
                        The team data for the away team

           Returns
           -------
           FootballResult
                The initialized FootballResult, ready to store the result of a match by updates to its goal list
        """
        super().__init__(home_team, away_team)
        self.penShootout = None
        self.goals = {home_team: [], away_team: []}
        self.domination = {home_team: 0, away_team: 0}
        self.nbShots = {home_team: 0, away_team: 0}

    def add_goal(self, scoring_team, goalscorer, is_og, is_pen, time, added_time=0):
        """
              Adds a goal to the list of goals. By default there's no added time

              Parameters
              ----------
              scoring_team : FootballTeam
                            The team who scored the goal
              goalscorer : FootballPlayer
                            The goal scorer
              is_og : bool
                            Indicates whether or not the goal is an own goal (scored by a player of the defending team)
              is_pen : bool
                            Indicates whether or not the goal was scored with a penalty kick
              time : int
                            Indicates the time at which the goal was scored
              added_time : int
                            Indicates if the goal was scored in added time and if true, when it was scored
        """
        self.score[scoring_team] += 1
        self.goals[scoring_team].append(Goal(goalscorer, is_og, is_pen, time, added_time))

    def update_club_stats(self, points=None, neutral_ground=False):
        """
           Updates both clubs's stats with the result's data, including an update to their point total according to
           the parameter

           Parameters
           ----------
           points : list of Int
                       The points attributed for a win, a draw and a loss respectively. Used to update the clubs's
                       points total
           neutral_ground : bool
                        Indicates if the match took place on neutral ground
                        (some stats are related to playing home/away)
        """
        if points is None:
            points = [1, 0, 0]
        team1, team2 = self.goals.keys()
        if self.score[team1] > self.score[team2]:
            team1.club.points += points[0]
            team2.club.points += points[2]
            team1.club.nbWin += 1
            team2.club.nbLosses += 1
        elif self.score[team1] < self.score[team2]:
            team2.club.points += points[0]
            team1.club.points += points[2]
            team2.club.nbWin += 1
            team1.club.nbLosses += 1
        else:
            team1.club.points += points[1]
            team2.club.points += points[1]
            team1.club.nbDrawn += 1
            team2.club.nbDrawn += 1
        team1.club.goalsScored += self.score[team1]
        team1.club.goalsConceded += self.score[team2]
        team2.club.goalsScored += self.score[team2]
        team2.club.goalsConceded += self.score[team1]
        if not neutral_ground:
            team2.club.awayGoalsScored += self.score[team2]

    def update_player_stats(self):
        """
           Updates the players's stats with the result's data (goals scored, try scored, etc...)
        """
        for side in self.goals:
            for g in self.goals[side]:
                if not g.isOG:
                    g.goalScorer.goalsScored += 1

    def write(self, nat, tier, path=None, prev_m=None):
        """
           Writes the match's result, either in the current directory or in a specified path

           Parameters
           ----------
           nat : bool
                        Should the clubs's nationalities feature in the written report
           tier : bool
                        Should the club's tiers feature in the report
           path : str
                        The path where the result should be written. If not specified the file is written in the
                        current directory
           prev_m : list of Result
                        A list of previous results we want to write because they give useful information (for example
                        if two teams play each other 7 times, with the team with the most wins qualifying, it's useful
                        to know the result of previous matches when looking at the result of a match)
        """
        if path is not None:
            os.chdir(path)
        team_names = []
        for t in self.goals.keys():
            team_names.append((t, t.club.name))
        prev_str = ""
        if prev_m:
            prev_str = "_"+str(len(prev_m)+1)+"_"
        tier_h_str = ""
        tier_a_str = ""
        nat_h_str = ""
        nat_a_str = ""
        if nat:
            nat_h_str = " ("+team_names[0][0].club.nationality+")"
            nat_a_str = " (" + team_names[1][0].club.nationality + ")"
        if tier:
            tier_h_str = " ("+str(team_names[0][0].club.tier)+")"
            tier_a_str = " (" + str(team_names[1][0].club.tier) + ")"
        filename = team_names[0][1].upper()+"_"+team_names[1][1].upper()+prev_str+".txt"
        file = open(filename, "w+")
        file.write(team_names[0][1]+nat_h_str+tier_h_str+" "+str(self.score[team_names[0][0]])+" - " +
                   str(self.score[team_names[1][0]])+" "+team_names[1][1]+nat_a_str+tier_a_str)
        file.write("\n\n\n\n")
        if len(self.goals[team_names[0][0]])+len(self.goals[team_names[1][0]]) > 0:
            file.write("Goals:\n\n")
        if len(self.goals[team_names[0][0]]) > 0:
            file.write(team_names[0][1]+":"+"\n")
        for g in self.goals[team_names[0][0]]:
            basic_goal = g.goalScorer.name+" "+str(g.time)
            if g.addedTime > 0:
                basic_goal = basic_goal+"+"+str(g.addedTime)
            if g.isOG:
                basic_goal = basic_goal+" o.g."
            elif g.isPen:  # a goal can't be both a goal scored on a penalty kick and an own goal !
                basic_goal = basic_goal+" (pen)"
            file.write(basic_goal+"\n")
        if len(self.goals[team_names[1][0]]) > 0:
            file.write("\n"+team_names[1][1]+":"+"\n")
        for g in self.goals[team_names[1][0]]:
            basic_goal = g.goalScorer.name+" "+str(g.time)
            if g.addedTime > 0:
                basic_goal = basic_goal+"+"+str(g.addedTime)
            if g.isOG:
                basic_goal = basic_goal+" o.g."
            elif g.isPen:  # a goal can't be both a goal scored on a penalty kick and an own goal !
                basic_goal = basic_goal+" (pen)"
            file.write(basic_goal+"\n")
        if prev_m:
            file.write("\n\n\n")
            for i in range(len(prev_m)):
                leg_ht, leg_at = prev_m[i].score.keys()
                str_score = " "+leg_ht.club.name+" "+str(prev_m[i].score[leg_ht])+" - " +\
                    str(prev_m[i].score[leg_at])+" "+leg_at.club.name
                file.write("Leg "+str(i+1)+" result:"+str_score+"\n")
        file.close()


class Goal:
    """
            Defines a goal in the Football sport.

            Attributes
            ----------
            goalScorer : Player
                        The goalscorer
            time : int
                        The minute in which the goal was scored
            addedTime : int
                        Indicates whether the goal was scored in added time
            isPen : bool
                        Flag indicating if the goal was scored on penalty
            isOG : bool
                        Flag indicating it it's an own goal

    """

    def __init__(self, goalscorer, is_og, is_pen, time, added_time):
        """
           Initializes the Goal with all its parameters.

           Parameters
           ----------
           goalscorer : FootballPlayer
                       See the goalScorer attribute
           is_og : bool
                        See the isOG attribute
           is_pen : bool
                        See the isPen attribute
           time : int
                        See the time attribute
           added_time : int
                        See the addedTime attribute

           Returns
           -------
           FootballResult
                The initialized FootballResult, ready to store the result of a match by updates to its goal list
        """
        self.goalScorer = goalscorer
        self.isOG = is_og
        self.isPen = is_pen
        self.time = time
        self.addedTime = added_time


class ResPenShootout:
    """
            Defines the result of a penalty shootout.

            Attributes
            ----------
            score : tuple of (int, int)
                        Tuple containing the number of penalties scored by the home and away team respectively
            homeResults : list of tuple of (Player, bool)
                        The list of shooters for the home team and whether they scored or not
            awayResults : list of tuple of (Player, bool)
                        The list of shooters for the away team and whether they scored or not
    """
    pass
