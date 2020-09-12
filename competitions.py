"""
Created on Thu Sep 10 2020

File defining the Competition class and all related classes, plus an init method to create and run a competition from the
relevant files

@author: alexa
"""


import json
import engine

def init_competitions(competitionCfgPath, engineCfgPath):
    """
        Initializes and run a competition using the configuration from two files given in input.

        Parameters
        ----------
        competitionCfg : str
                    Path to the competition configuration file which defines the competition to be run
        engineCfg : str
                    Path to the engine configuration file to be used when running the competition. Can be empty ("") in
                    which case default configuration will be used

        Returns
        -------
        To be defined (if anything)
    """
    engineCfg = None
    if (engineCfgPath != ''):
        engineCfg = engine.EngineCfg(engineCfgPath)
    else:
        engineCfg = engine.EngineCfg()
    competition = Competition(competitionCfgPath, engineCfg)
    competition.simulate()
    competition.write()


class Competition:
    """
            Defines a competition.

            Attributes
            ----------
            name : str
                        The name of the competition
            outputDir : str
                        Path to the output directory where the results will be written so the user can read them
            outputDir_teams : str
                        Path to the directory where the data of the teams qualified will be written. It is used to chain
                        competitions which can't be logically chained using only one config file. Can be empty ('') in
                        which case no export will take place
            isNatImp : bool
                        A flag to tell us if the nationality of teams matter
            isTierImp : bool
                        A flag to tell us if the clubs's tiers matter
            rounds : list of Round
                        The list of the competition's various rounds, organized from first round to last round
            teams : list of Team
                        The list of the teams currently taking part in the competitions. Will be regularly updated to
                        get rid of eliminated teams or to add teams entering in later rounds
            engineCfg : EngineCfg
                        The parameters used by the engine during the match simulation
            statisticsComputed: list of str
                        List of statistics to be computed when writing the competition

            Methods
            -------
            simulate : None -> Team
                    Plays the competition and returns winning team
            write : None -> None
                    Writes the competition results
            _makeStatistics : None -> None
                    Writes statistics about the competition (currently: only top goalscorer)
    """

    def __init__(self, jsonFilePath, engineCfg):
        """
               Initializes a competition from a configuration file

               Parameters
               ----------
               competitionCfg : str
                           Path to the competition configuration file which defines the competition to be run
               engineCfg : EngineParameters
                           The engine configuration to be used when simulating the matches

               Returns
               -------
               Competition
                    The initialized Competition object
        """
        # all there is to do is to read the JSON file, init the values and create appropriate Rounds as they come
        pass

    def simulate(self):
        """
              Simulate the competition and stores the results in the attributes

              Returns
              -------
              Team
                   The winning team
        """
        # all there is to do is to simulate each round one by one and update the teams list with the list returned
        # by each call
        pass

    def write(self):
        """
              Writes the competition results in the target directory
        """
        # all there is to do is write each round and write statistics if need be
        pass

    def _makeStatistics(self):
        """
              Computes statistics about the competition and writes them
        """
        # all there is to do is go through each team, compute relevant statistics and write them in a file containing
        # these stats
        pass

class Round:
    """
        Defines a round. Mostly used as a type of interface, to be overridden by Round implementations
        (currently two).

        Attributes
        ----------
        names : list of str
                    List of the names used for the individual rounds (list because a round may correspond to
                    numerous actual rounds)
        teamsDataPath : str
                    Path to the directory containing the data of teams to be loaded for this round if any (if
                    it is empty - '' - no data will be loaded).
        nbConfrontations : int
                    Number of times two teams play each other
        awayGoalsUsed : bool
                    A flag to tell us if away goals are used as tie-breakers
        neutralGround : bool
                    A flag indicating if the matches take place on neutral ground for this round
        results: list of list of list of Result
                    The list of the match results
        teams : list of Team
                    List of qualified teams

        Methods
        -------
        simulate : None -> list of Team
                    Plays the competition, saves the results in results and returns the list of qualified teams
        write : None -> None
                    Writes the competition results
        """
    def __init__(self, roundParameters):
        """
           Initializes a round from the adequate part of a competition JSON file

           Parameters
           ----------
           roundParameters : dict
                       The dict containing the round data

           Returns
           -------
           Round
                The initialized Round object
        """
        # all there is to do is init the values with what is in the dict
        pass

    def simulate(self):
        """
           Simulates the round (to be overridden by subclasses implementations)

           Returns
           -------
           list of Team
                List of qualified teams after this round
        """
        pass

    def write(self):
        """
               Writes the round's results (to be overridden by subclasses implementations)
        """
        pass

class League(Round):
    """
        A subtype of Round, representing a league format competition

        Attributes
        ----------
        nbGroups : int
                    Number of groups (leagues to be simulated)
        tieBreakers : list of TieBreaker
                    List of the tie breakers criterias to be used ranked in order
        tableEachRound : bool
                    Flag indicating if a temporary table should be written after each round
        points : list of int
                    Number of points gained for a victory, a draw, a loss
        nbAdvancing : int
                    Number of teams advancing from the league(s)
        potForAdvancing : bool
                    Flag indicating if qualified teams should have a pot (equal to their final ranking) affected to them
        table : list of list of Teams
                    The teams classified from top to bottom according to their results (each league being a separate list)
        Methods
        -------
        None planified, internal methods will likely be needed though (add them here ?)
    """

    def __init__(self, roundParameters):
        """
           Initializes a league from the adequate part of a competition JSON file

           Parameters
           ----------
           roundParameters : dict
                       The dict containing the round data

           Returns
           -------
           League
                The initialized League object
        """
        super().__init__(roundParameters)
        # and then init the parameters exclusive to a league
        pass

    def simulate(self):
        """
           Simulates the round according to league rules

           Returns
           -------
           list of Team
                List of qualified teams after this round
        """
        groups = []
        qualifiedTeams = []
        if self.nbGroups > 1:
            # draw teams in several groups
            pass
        else:
            groups.append(self.teams)

        for g in groups:
            # make a schedule for the group
            schedule = [[],[]]
            for matchday in schedule:
                for match in matchday:
                    # play the match
                    # then update each team's statistics and goalscorer statistics
                    pass
                    # save the match result in self.results
            # make the league table
            leagueTable = []
            self.table.append(leagueTable)
            # then add the qualified teams to the list of qualified teams
            for t in range(self.nbAdvancing):
                qualifiedTeams.append(leagueTable[t])
                # set the team's pot if self.potForAdvancing requires it

    def write(self):
        """
               Writes a league's results
        """
        # it's just about parsing self.results and writing them all in the good subfolder
        # then write the league table at the end
        # if self.tableEachRound requires it, we need to compute the table for each matchday
        pass

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
                    If this value is -1 no penalty shoutoot will be held

        Methods
        -------
        None planified, internal methods will likely be needed though (add them here ?)
    """

    def __init__(self, roundParameters):
        """
           Initializes a knockout stage from the adequate part of a competition JSON file

           Parameters
           ----------
           roundParameters : dict
                       The dict containing the round data

           Returns
           -------
           Knockout
                The initialized Knockout object
        """
        super().__init__(roundParameters)
        # and then init the parameters exclusive to a knckout round
        pass

    def simulate(self):
        """
           Simulates the round according to knockout rules

           Returns
           -------
           list of Team
                List of qualified teams after this round
        """
        for r in range(self.nbRounds):
            # draw the teams in pairs
            matchList = []
            qualifiedTeams = []
            for m in matchList:
                # play each duel
                # number of time each duel must be played is described by self.nbConfrontations
                # loop on that and store each result
                # if for the last match to be played (according to self.nbConfrontations) nobody wins play extra time
                # then if nobody wins still either have a penalty shootout or replay the match on neutral ground
                # until somebody wins
                # and save the result of each match in the correct sublist
                # and add the winning list to the list of qualified teams
                qualifiedTeams.append("winning team")
                pass
            # and then the list of teams is replaced by qualifiedTeams for the next

    def write(self):
        """
               Writes a knockout round's results
        """
        # just loop over the results and write them in the correct directory
        pass