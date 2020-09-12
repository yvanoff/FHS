# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 2020

CLI file

@author: alexa
"""

import competitions

VERSION_NUMBER = 2.0

def main():
    """
        Command Line Interface to use the FHS (Football History Simulator). Temporary to test the program without
        implementing a GUI
    """

    exit = False
    while not exit:
        print("Please choose the desired FHS mode to run:\n")
        print("1: Create, edit, generate or delete team files\n")
        print("2: Create, edit or delete competition files\n")
        print("3: Create, edit or delete engine configuration files\n")
        print("4: Run a competition\n")
        print("5: Exit\n")
        choice = 0
        try:
            choice = int(input("Select the mode to use: "))
        except ValueError:
            print("Please enter a number...\n")
        if (choice == 1):
            pass # Here will go the team editor
        elif (choice == 2):
            pass # Here will go the competition files editor
        elif (choice == 3):
            pass # Here will go the engine configuration files editor
        elif (choice == 4):
            competitionCfgPath = input("Please enter the path to the competition configuration file: ")
            engineCfgPath = input("Please enter the path to the engine configuration file (leave blank if default"
                                  "configuration is used): ")
            competitions.init_competitions(competitionCfgPath, engineCfgPath)
        else:
            print("Please enter a valid value...\n")

if __name__ == "__main__":
    # execute only if run as a script
    main()