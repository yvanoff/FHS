# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:44:20 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from coupe import make_knockout
from save_window import SaveWindow

class MatchCreator:
    def __init__(self, master=None, cfgfile = None):
        self.master = master
        self.data_path = '.'
        self.display_data_path = tk.StringVar()
        self.output_path = '.'
        self.display_output_path = tk.StringVar()
        self.aller_retour = tk.IntVar()
        self.buts_ext = tk.IntVar()
        self.flags = tk.IntVar()
        self.terrain_neutre = tk.IntVar()
        self.tab = tk.IntVar()
        self.prolongations = tk.IntVar()
        self.name_round = tk.StringVar()
        self.save_dir = tk.StringVar()
        self.filename = tk.StringVar()
        if cfgfile != None:
            file = open(cfgfile,'r')
            data = file.readlines()
            file.close()
            if (data[0][:-1] == 'Config-Match'):
                self.data_path = data[1][:-1]
                self.display_data_path.set('Current data directory: '+self.data_path)
                self.output_path = data[2][:-1]
                self.display_output_path.set('Current data directory: '+self.output_path)
                self.aller_retour.set(data[3][:-1] == 'True')
                self.flags.set(data[4][:-1] == 'True')
                self.prolongations.set(data[5][:-1] == 'True')
                self.tab.set(data[6][:-1] == 'True')
                self.buts_ext.set(data[7][:-1] == 'True')
                self.terrain_neutre.set(data[8][:-1] == 'True')
                self.name_round.set(data[12][:-1])
        self.make_gui()
        
    def dico_params(self):
        dico = {'buts_ext_2' : self.buts_ext.get(),
                'prolongations' : self.prolongations.get(),
                'tab' : self.tab.get(),
                'terrain_neutre' : self.terrain_neutre.get()}
        return dico
        
    def start(self, params_moteur):
        params_moteur['nom tour'] = self.name_round.get()
        make_knockout(nom_saison=self.data_path+'/', resultat_saison=self.output_path,
                 aller_retour=self.aller_retour.get(), finale_ar=self.aller_retour.get(),
                 liste_chapeaux=[1,2], un_seul_tour=True,
                 flag_exist=self.flags.get(), add_args=params_moteur)
        
    def ask_data_dir(self):
        self.data_path = tk.filedialog.askdirectory(initialdir = self.data_path,
                                                    title = "Select directory")
        self.display_data_path.set('Current data directory: '+self.data_path)
        
    def ask_output_dir(self):
        self.output_path = tk.filedialog.askdirectory(initialdir = self.output_path,
                                                    title = "Select directory")
        self.display_output_path.set('Current data directory: '+self.output_path)
    
    def make_gui(self):
        self.label_data_path = ttk.Label(self.master, text = self.data_path)
        self.label_data_path['textvariable'] = self.display_data_path
        self.label_data_path.grid(column = 0, row = 0, columnspan = 3, sticky = 'nsew')
        self.button_data_path = ttk.Button(self.master, command = self.ask_data_dir,
                            text = 'Choose data location')
        self.button_data_path.grid(column = 0, row = 1, columnspan = 3, sticky = 'nsew')
        self.label_output_path = ttk.Label(self.master, text = self.output_path)
        self.label_output_path['textvariable'] = self.display_output_path
        self.label_output_path.grid(column = 3, row = 0, columnspan = 3, sticky = 'nsew')
        self.button_output_path = ttk.Button(self.master, command = self.ask_output_dir,
                            text = 'Choose output directory')
        self.button_output_path.grid(column = 3, row = 1, columnspan = 3, sticky = 'nsew')        
        self.prol_button = ttk.Checkbutton(self.master, text = 'Extra Time',
                                 variable = self.prolongations)
        self.prol_button.grid(column = 0, row = 2, columnspan = 3, sticky = 'nsew')
        self.tab_button = ttk.Checkbutton(self.master, text = 'Penalty shootout',
                                 variable = self.tab)
        self.tab_button.grid(column = 3, row = 2, columnspan = 3, sticky = 'nsew')
        self.button_neutral = ttk.Checkbutton(self.master, text = 'Play on neutral ground',
                                 variable = self.terrain_neutre,
                                 command = self.switch_neutre)
        self.button_neutral.grid(column = 0, row = 3, columnspan = 3, sticky = 'nsew')
        if (self.aller_retour.get() == 1):
            self.button_neutral['state'] = tk.DISABLED
        self.flag_button = ttk.Checkbutton(self.master, text = 'Flags exist',
                                 variable = self.flags)
        self.flag_button.grid(column = 3, row = 3, columnspan = 3, sticky = 'nsew')
        self.ar_button = ttk.Checkbutton(self.master, text = 'Play over two legs',
                                 variable = self.aller_retour,
                                 command = self.switch_ar)
        self.ar_button.grid(column = 0, row = 4, columnspan = 3, sticky = 'nsew')
        if (self.terrain_neutre.get() == 1):
            self.ar_button['state'] = tk.DISABLED
        self.button_extx2 = ttk.Checkbutton(self.master, text = 'Away goals count double',
                                 variable = self.buts_ext)
        self.button_extx2.grid(column = 3, row = 4, columnspan = 3, sticky = 'nsew')
        if (self.aller_retour.get() == 0):
            self.button_extx2['state'] = tk.DISABLED
        self.text_name_round = ttk.Label(self.master, text = 'Name of the round:')
        self.text_name_round.grid(column = 0, row = 5, columnspan = 3, sticky = 'nsew')
        self.name_round_entry = ttk.Entry(self.master, textvariable = self.name_round)
        self.name_round_entry.grid(column = 3, row = 5, columnspan = 3, sticky = 'nsew')
        self.master.pack()
        
    def switch_neutre(self):
        if self.terrain_neutre.get() == 1:
            self.ar_button['state'] = tk.DISABLED
            self.button_extx2['state'] = tk.DISABLED
        else:
            self.ar_button['state'] = tk.NORMAL
            self.button_extx2['state'] = tk.NORMAL
            
    def switch_ar(self):
        if self.aller_retour.get() == 1:
            self.button_neutral['state'] = tk.DISABLED
            self.button_extx2['state'] = tk.NORMAL
        else:
            self.button_neutral['state'] = tk.NORMAL
            self.button_extx2['state'] = tk.DISABLED
    
    def save(self):
        save_prompt = tk.Toplevel(self.master)
        SaveWindow(save_prompt, self)
        self.master.wait_window(save_prompt)
        file = open(self.save_dir.get()+'/'+self.filename.get()+'.mcfg','w')
        file.write("Config-Match\n")
        file.write(self.data_path+'\n')
        file.write(self.output_path+'\n')
        file.write(str(self.aller_retour.get() == 1)+'\n')
        file.write(str(self.flags.get() == 1)+'\n')
        file.write(str(self.prolongations.get() == 1)+'\n')
        file.write(str(self.tab.get() == 1)+'\n')
        file.write(str(self.buts_ext.get() == 1)+'\n')
        file.write(str(self.terrain_neutre.get() == 1)+'\n')
        file.write(self.name_round.get()+'\n')
        file.close()
        
    def receive_info(self, sd, fn):
        self.save_dir.set(sd.get())
        self.filename.set(fn.get())