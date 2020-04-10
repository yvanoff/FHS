# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:46:26 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

class PlayerWindow:
    def __init__(self, master = None, list_players = [], listbox_players = None,
                 selected = -1):
        self.master = master
        self.internal_players = list_players
        self.list_joueurs = listbox_players
        self.new_window = tk.Toplevel(self.master)
        self.selection = selected
        self.dico_pos = {'gk' : 'Goalkeeper',
            'df' : 'Defender',
            'mf' : 'Midfielder',
            'fw': 'Forward'}
        self.nom_joueur = tk.StringVar()
        self.main_pos = tk.StringVar()
        self.gb_possible = tk.IntVar()
        self.df_possible = tk.IntVar()
        self.mf_possible = tk.IntVar()
        self.fw_possible = tk.IntVar()
        self.is_pen_taker = tk.IntVar()
        self.force_joueur = tk.IntVar()
        self.action_player()
    
    def action_player(self):
        if self.selection != -1:
            player = self.internal_players[self.selection[0]]
            player_stats = player.split(', ')
            player_name = player_stats[0]
            player_mainpos = player_stats[1]
            player_strength = int(player_stats[2])
            player_pen = "Penalty taker" in player_stats
            player_possible = ['']
            if len(player_stats) >= 4:
                if player_stats[3] != "Penalty taker":
                    if '/' in player_stats[3]:
                        player_possible = player_stats[3].split('/')
                    else:
                        player_possible = [player_stats[3]]
            self.nom_joueur.set(player_name)
            self.main_pos.set(self.findkey(player_mainpos))
            self.gb_possible.set(int('Goalkeeper' in player_possible))
            self.df_possible.set(int('Defender' in player_possible))
            self.mf_possible.set(int('Midfielder' in player_possible))
            self.fw_possible.set(int('Forward' in player_possible))
            self.is_pen_taker.set(int(player_pen))
            self.force_joueur.set(player_strength)
        nom_joueur_text = ttk.Label(self.new_window, text = 'Name of player:')
        nom_joueur_text.pack()
        nom_joueur_entry = ttk.Entry(self.new_window, textvariable =self.nom_joueur)
        nom_joueur_entry.pack()
        pos_joueur_text = ttk.Label(self.new_window, text = 'Player main position:')
        pos_joueur_text.pack()
        main_gb = ttk.Radiobutton(self.new_window, text='GK', variable = self.main_pos, value = 'gk')
        main_gb.pack()
        main_df = ttk.Radiobutton(self.new_window, text='DF', variable = self.main_pos, value = 'df')
        main_df.pack()
        main_mf = ttk.Radiobutton(self.new_window, text='MID', variable = self.main_pos, value = 'mf')
        main_mf.pack()
        main_fw = ttk.Radiobutton(self.new_window, text='FWD', variable = self.main_pos, value = 'fw')
        main_fw.pack()
        force_joueur_text = ttk.Label(self.new_window, text = 'Strength of player:')
        force_joueur_text.pack()
        force_joueur_entry = ttk.Spinbox(self.new_window, textvariable = self.force_joueur,
                                       from_ = 1, to = 99)
        force_joueur_entry.pack()
        pos_joueur_text = ttk.Label(self.new_window, text = 'Player other positions:')
        pos_joueur_text.pack()
        can_into_gb = tk.Checkbutton(self.new_window, text='GK', variable = self.gb_possible)
        can_into_gb.pack()
        can_into_df = tk.Checkbutton(self.new_window, text='DF', variable = self.df_possible)
        can_into_df.pack()
        can_into_mf = tk.Checkbutton(self.new_window, text='MID', variable = self.mf_possible)
        can_into_mf.pack()
        can_into_fw = tk.Checkbutton(self.new_window, text='FWD', variable = self.fw_possible)
        can_into_fw.pack()
        pen_button = tk.Checkbutton(self.new_window, text = "Penalty taker", variable = self.is_pen_taker)
        pen_button.pack()
        action_name = ''
        if self.selection == -1:
            action_name = 'Add player'
        else:
            action_name = 'Edit the player'
        add_button = ttk.Button(self.new_window, text=action_name, command = self.list_action_player)
        add_button.pack()
        cancel_button = ttk.Button(self.new_window, text = 'Cancel', command = self.new_window.destroy)
        cancel_button.pack()
        
    def findkey(self, value):
        for k,v in self.dico_pos.items():
            if v == value:
                return k
        
    def list_action_player(self):
        if '' in self.internal_players:
            self.internal_players.remove('')
        total_string = (self.nom_joueur.get()+", "+
                        self.dico_pos[self.main_pos.get()]+
                        ", "+str(self.force_joueur.get()))
        pos_string = ""
        if self.gb_possible.get() == 1:
            if pos_string != "":
                pos_string += "/"
            pos_string += "Goalkeeper"
        if self.df_possible.get() == 1:
            if pos_string != "":
                pos_string += "/"
            pos_string += "Defender"
        if self.mf_possible.get() == 1:
            if pos_string != "":
                pos_string += "/"
            pos_string += "Midfielder"
        if self.fw_possible.get() == 1:
            if pos_string != "":
                pos_string += "/"
            pos_string += "Forward"
        if pos_string != "":
            pos_string = ", "+pos_string
        total_string += pos_string
        if self.is_pen_taker.get() == 1:
            total_string += ", Penalty taker"
        if self.selection == -1:
            self.internal_players.append(total_string)
        else:
            self.internal_players.pop(self.selection[0])
            self.internal_players.insert(self.selection[0], total_string)
        self.list_joueurs.set(self.internal_players)
        self.new_window.destroy()