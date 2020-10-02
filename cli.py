# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 2020

CLI file

This file defines a Command-Line Interface (CLI) for the Football History Simulator project

Just do python cli.py and enjoy !

@author: alexa
"""

from competitions import Competition
from football__club_generator import generator_interface

VERSION_NUMBER = 2.0


def main():

    """
        Command Line Interface to use the FHS (Football History Simulator). Temporary to test the program without
        implementing a GUI
    """

    exit_loop = False
    while not exit_loop:
        print("Please choose the desired FHS mode to run:\n")
        print("1: Create, edit, generate or delete club files\n")
        print("2: Create, edit or delete competition files\n")
        print("3: Create, edit or delete engine configuration files\n")
        print("4: Run a competition\n")
        print("5: Exit\n")
        choice = 0
        try:
            choice = int(input("Select the mode to use: "))
        except ValueError:
            print("Please enter a number...\n")
        if choice == 1:
            path = input("Please type the directory in which files will be generated: ")
            generator_interface(path)
        elif choice == 2:
            pass  # Here will go the competition files editor
        elif choice == 3:
            pass  # Here will go the engine configuration files editor
        elif choice == 4:
            competition_cfg_path = input("Please enter the path to the competition configuration file: ")
            engine_cfg_path = input("Please enter the path to the engine configuration file (leave blank if default"
                                    "configuration is used): ")
            competition = Competition(competition_cfg_path, engine_cfg_path)
            competition.simulate()
            competition.write()
        elif choice == 5:
            exit_loop = True
        else:
            print("Please enter a valid value...\n")


if __name__ == "__main__":
    # execute only if run as a script
    main()
