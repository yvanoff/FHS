# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 23:47:25 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from coupe import make_knockout, make_groupStage
from save_window import SaveWindow

how to handle complex cup:
    - the different stages are organised in a listbox
    - there is a button to add a stage, a button to remove a stage, a button to edit a stage
    - a button to move a stage up, a button to move a stage down
    - the list in the listbox contains the name of the stages
    - in parallel there is a dictionary with the list\'s values as keys
    - create/edit stages is done with KnockoutEditor/GroupStageEditor in a new toplevel
    - once a stage is created (with a wait to complete the toplevel) it is added to list and dictionary
    - dictionary values are special items who holds the parameter of the stage
    - note: the save/output directories of each individual stages don\'t matter
    - add an entry for the complex cup input folder
    - an entry for the complex cup output folder
    - intermediary input/output folder for each stage will be handled internally
    - the name of the output directory of a stage will be the name of the stage in the list
    
so basically:
    
class GroupStageHolder:
    #contains the parameters of a group stage
    
class KnockoutHolder:
    #contains the parameters of a knckout round

class ComplexCup:

    def __init__(self, master = None):
        self.list_stages = ['']
        self.dic_stages = {}
        self.display_path.set('Current save directory: ' + self.save_path)
        self.save_path = '.'
        self.display_path = tk.StringVar()
        self.output_path = '.'
        self.display_output_path = tk.StringVar()
        self.make_gui()

    def make_gui(self):
        self.label_path = ttk.Label(self.master, text=self.save_path)
        self.label_path['textvariable'] = self.display_path
        self.label_path.grid(column=0, row=0, columnspan=3, sticky='nsew')
        self.button_path = ttk.Button(self.master, command=self.ask_data_dir,
                                      text='Choose save directory')
        self.button_path.grid(column=0, row=1, columnspan=3, sticky='nsew')
        self.filename_text = ttk.Label(self.master, text='Save file as:')
        self.filename_text.grid(column=0, row=2, columnspan=2, sticky='nsew')
        self.entry_filename = ttk.Entry(self.master, textvariable=self.filename)
        self.entry_filename.grid(column=2, row=2, sticky='nsew')
        self.chapeau0_button = ttk.Checkbutton(self.master, text='Pot 0 enabled',
                                               variable=self.chapeau_0)
        self.chapeau0_button.grid(column=4, row=1, columnspan=3, sticky='nsew')
        self.liste_chapeaux_button = tk.Spinbox(self.master, textvariable=self.nb_chapeaux,
                                                from_=1, to=99)
        self.liste_chapeaux_button.grid(column=4, row=2, columnspan=3, sticky='nsew')
        self.chapeau0_button['state'] = tk.DISABLED
        self.liste_chapeaux_button['state'] = tk.DISABLED
        self.chapeaux_button = ttk.Checkbutton(self.master, text='Pots',
                                               variable=self.chapeaux_exist,
                                               command=self.switch_chapeaux)
        self.chapeaux_button.grid(column=4, row=0, columnspan=3, sticky='nsew')
        self.text_nom_team = ttk.Label(self.master, text='Team name:')
        self.text_nom_team.grid(column=0, row=3, sticky='nsew')
        self.nom_team_entry = ttk.Entry(self.master, textvariable=self.team_name)
        self.nom_team_entry.grid(column=1, row=3, sticky='nsew')
        self.text_flag_team = ttk.Label(self.master, text='Flag:')
        self.text_flag_team.grid(column=2, row=3, sticky='nsew')
        self.nom_flag_entry = ttk.Entry(self.master, textvariable=self.flag)
        self.nom_flag_entry.grid(column=3, row=3, sticky='nsew')
        self.text_nom_team = ttk.Label(self.master, text='Pot:')
        self.text_nom_team.grid(column=4, row=3, sticky='nsew')
        self.nom_pot_entry = ttk.Entry(self.master, textvariable=self.chapeau)
        self.nom_pot_entry.grid(column=5, row=3, sticky='nsew')
        self.nom_pot_entry['state'] = tk.DISABLED
        self.text_nb_df = ttk.Label(self.master, text='Number of defenders:')
        self.text_nb_df.grid(column=0, row=4, sticky='nsew')
        self.nb_df_entry = ttk.Entry(self.master, textvariable=self.nb_df)
        self.nb_df_entry.grid(column=1, row=4, sticky='nsew')
        self.text_nb_mf = ttk.Label(self.master, text='Number of midfielders:')
        self.text_nb_mf.grid(column=2, row=4, sticky='nsew')
        self.nb_mf_entry = ttk.Entry(self.master, textvariable=self.nb_mf)
        self.nb_mf_entry.grid(column=3, row=4, sticky='nsew')
        self.text_nb_fw = ttk.Label(self.master, text='Number of forwards:')
        self.text_nb_fw.grid(column=4, row=4, sticky='nsew')
        self.nb_fw_entry = ttk.Entry(self.master, textvariable=self.nb_fw)
        self.nb_fw_entry.grid(column=5, row=4, sticky='nsew')
        self.list_player = tk.Listbox(self.master, listvariable=self.list_joueurs)
        self.list_player.grid(column=0, row=5, columnspan=6, sticky='nsew')
        self.add_player_button = ttk.Button(self.master, command=self.add_player,
                                            text='Add player')
        self.add_player_button.grid(column=0, row=6, columnspan=2, sticky='nsew')
        self.edit_player_button = ttk.Button(self.master, command=self.edit_player,
                                             text='Edit player')
        self.edit_player_button.grid(column=2, row=6, columnspan=2, sticky='nsew')
        self.add_player_button = ttk.Button(self.master, command=self.remove_player,
                                            text='Remove player')
        self.add_player_button.grid(column=4, row=6, columnspan=2, sticky='nsew')
        self.master.pack()

    def ask_data_dir(self):
        self.data_path = tk.filedialog.askdirectory(initialdir=self.data_path,
                                                    title="Select directory")
        self.display_data_path.set('Current data directory: ' + self.data_path)

    def ask_output_dir(self):
        self.output_path = tk.filedialog.askdirectory(initialdir=self.output_path,
                                                      title="Select directory")
        self.display_output_path.set('Current data directory: ' + self.output_path)
    
    gui: label+button for input and output dir
    listbox
    button to add knockout stage
    button to add group stage
    button to edit and remove are independant of the type of groupe stage
    button to move up/down
    
    start:
        calls each stage one by one with the correct parameters
        gets the qualified teams and move them to the correct directories to feed the next stage