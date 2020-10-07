"""
Created on Thu Sep 10 2020

File defining the Competition class

The Competition class, unsurprisingly, defines a competition for a given sport, simulates it, stores its
results and can write them somewhere (main way to get the competition's results)

@author: alexa
"""


import json
from league import League
from knockout import Knockout
import os


class Competition:
    """
            Defines a competition, for no particular sport (the hope is that it is usable by any sport).

            Attributes
            ----------
            name : str
                        The name of the competition
            sport : str
                        The sport played in the Competition
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
            clubs : list of Club
                        The list of the clubs currently taking part in the competitions. Will be regularly updated to
                        get rid of eliminated clubs or to add clubs entering in later rounds
            fullClubs : list of Club
                        The full list of all clubs taking part in the competition
            engineCfgPath : str
                        Path to the parameters file used by the engine during the match simulation
            statisticsComputed: list of str
                        List of statistics to be computed when writing the competition

            Methods
            -------
            simulate : None -> List of Club
                    Plays the competition and returns the winning teams
            write : None -> None
                    Writes the competition results
    """

    def __init__(self, json_file_path, engine_cfg_path):
        """
               Initializes a competition from a configuration file

               Parameters
               ----------
               json_file_path : str
                           Path to the competition configuration file which defines the competition to be run
               engine_cfg_path : EngineParameters
                           The engine configuration to be used when simulating the matches

               Returns
               -------
               Competition
                    The initialized Competition object
        """

        comp_cfg_file = open(json_file_path)
        comp_cfg = comp_cfg_file.read()
        comp_cfg_file.close()
        json_cfg = json.loads(comp_cfg)

        self.engineCfgPath = engine_cfg_path
        self.name = ''
        if 'name' in json_cfg.keys():
            self.name = json_cfg['Name']
        self.sport = 'foot'
        if 'Sport' in json_cfg.keys():
            self.sport = json_cfg['Sport']
        self.outputDir = '.'
        if 'Output_directory' in json_cfg.keys():
            self.outputDir = json_cfg['Output_directory']
        self.outputDir_teams = ''
        if 'Output_directory_for_qualified_teams_data' in json_cfg.keys():
            self.outputDir_teams = json_cfg['Output_directory_for_qualified_teams_data']
        self.isNatImp = False
        if 'Is_nationality_important' in json_cfg.keys():
            self.isNatImp = json_cfg['Is_nationality_important']
        self.isTierImp = False
        if 'Is_club_level_important' in json_cfg.keys():
            self.isTierImp = json_cfg['Is_club_level_important']
        self.statisticsComputed = []
        if 'Statistics' in json_cfg.keys():
            self.statisticsComputed = json_cfg['Statistics']
        self.clubs = []

        self.rounds = []
        self.fullClubs = []
        for r in json_cfg['Rounds']:
            if 'League' in r.keys():
                self.rounds.append(League(self.sport, r, self.isNatImp, self.isTierImp, self.engineCfgPath))
            elif 'Round' in r.keys():
                self.rounds.append(Knockout(self.sport, r, self.isNatImp, self.isTierImp, self.engineCfgPath))
            else:
                print("Error with the type of round ! Unknown")  # exception !
            for club in self.rounds[-1].clubs:
                self.fullClubs.append(club)

    def simulate(self):
        """
              Simulate the competition and stores the results in the attributes

              Returns
              -------
              Team
                   The winning team
        """
        for r in self.rounds:
            self.clubs = r.simulate(self.clubs)
        if self.outputDir_teams != '':
            try:
                os.mkdir(self.outputDir_teams)
                os.chdir(self.outputDir_teams)
                for c in self.clubs:
                    # parameters for export_to_xml
                    c.export_to_xml()
            except FileExistsError:
                print("Directory already exists; aborting....")

    def write(self):
        """
              Writes the competition results in the target directory
        """
        try:
            og_dir = os.getcwd()
            os.mkdir(self.outputDir)
            os.chdir(self.outputDir)
            for r in self.rounds:
                r.write(self.isNatImp, self.isTierImp)
            for s in self.statisticsComputed:
                # we should do something here !
                pass
            os.chdir(og_dir)
        except FileExistsError:
            print("Directory already exists; aborting....")
