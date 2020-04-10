# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 21:09:48 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from championnat import make_championnat
from save_window import SaveWindow

class LeagueCreator:
    def __init__(self, master=None, cfgfile = None):
        self.master = master
        self.data_path = '.'
        self.display_data_path = tk.StringVar()
        self.output_path = '.'
        self.display_output_path = tk.StringVar()
        self.aller_retour = tk.IntVar()
        self.pts_v = tk.IntVar()
        self.pts_n = tk.IntVar()
        self.pts_d = tk.IntVar()
        self.convert_dico = {'diff' : 'Difference de buts',
                             'bp' : 'Buts inscrits',
                             'conf' : 'Confrontations directes'}
        self.true_criterias = ['diff', 'bp', 'conf']
        value_tmp = []
        for c in self.true_criterias:
            value_tmp.append(self.convert_dico[c])
        self.display_criterias = tk.StringVar(value=value_tmp)
        self.save_dir = tk.StringVar()
        self.filename = tk.StringVar()
        if cfgfile != None:
            file = open(cfgfile,'r')
            data = file.readlines()
            file.close()
            if (data[0][:-1] == 'Config-League'):
                self.data_path = data[1][:-1]
                self.display_data_path.set('Current data directory: '+self.data_path)
                self.output_path = data[2][:-1]
                self.display_output_path.set('Current data directory: '+self.output_path)
                self.aller_retour.set(data[3][:-1] == 'True')
                self.pts_v.set(int(data[4][:-1]))
                self.pts_n.set(int(data[5][:-1]))
                self.pts_d.set(int(data[6][:-1]))
                self.true_criterias[0] = data[7][:-1]
                self.true_criterias[1] = data[8][:-1]
                self.true_criterias[2] = data[9][:-1]
                value_tmp = []
                for c in self.true_criterias:
                    value_tmp.append(self.convert_dico[c])
                self.display_criterias = tk.StringVar(value=value_tmp)
        self.make_gui()
        
    def dico_params(self):
        return {}
        
    def start(self, params_moteur):
        make_championnat(nom_saison=self.data_path+'/', resultat_saison=self.output_path,
                 m_retours=self.aller_retour.get(), criterias=self.true_criterias,
                 pts=[self.pts_v.get(),self.pts_n.get(), self.pts_d.get()],
                 additional_arguments=params_moteur)
        
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
        self.ar_button = ttk.Checkbutton(self.master, text = 'Home and away matches',
                                 variable = self.aller_retour)
        self.ar_button.grid(column = 0, row = 2, columnspan = 6, sticky = 'nsew')
        label_v = ttk.Label(self.master, text = 'Number of points for a win:')
        label_v.grid(column = 0, row = 3, columnspan = 2, sticky = 'nsew')
        self.box_v = ttk.Spinbox(self.master, textvariable = self.pts_v, from_ = 2, to = 4)
        self.box_v.grid(column = 0, row = 4, columnspan = 2, sticky = 'nsew')
        label_n = ttk.Label(self.master, text = 'Number of points for a draw:')
        label_n.grid(column = 2, row = 3, columnspan = 2, sticky = 'nsew')
        self.box_n = ttk.Spinbox(self.master, textvariable = self.pts_n, from_ = 1, to = 2)
        self.box_n.grid(column = 2, row = 4, columnspan = 2, sticky = 'nsew')
        label_p = ttk.Label(self.master, text = 'Number of points for a loss:')
        label_p.grid(column = 4, row = 3, columnspan = 5, sticky = 'nsew')
        self.box_d = ttk.Spinbox(self.master, textvariable = self.pts_d, from_ = 0, to = 1)
        self.box_d.grid(column = 4, row = 4, columnspan = 2, sticky = 'nsew')
        self.label_crit = ttk.Label(self.master, text = 'Rank the tie-breaking criterias to use:')
        self.label_crit.grid(column = 0, row = 5, columnspan = 6, sticky = 'nsew')
        self.list_crit = tk.Listbox(self.master,listvariable = self.display_criterias)
        self.list_crit.grid(column = 0, row = 6, columnspan = 6, sticky = 'nsew')
        self.button_up = ttk.Button(self.master, command = self.move_up,
                            text = 'Rank up')
        self.button_up.grid(column = 0, row = 7, columnspan = 3, sticky = 'nsew')
        self.button_down = ttk.Button(self.master, command = self.move_down,
                            text = 'Rank down')
        self.button_down.grid(column = 3, row = 7, columnspan = 3, sticky = 'nsew')
        self.master.pack()
        
    def move_up(self):
        selected = self.list_crit.curselection()
        if selected[0]>0:
            self.true_criterias.insert(selected[0]-1,self.true_criterias.pop(selected[0]))
            value_tmp = []
            for c in self.true_criterias:
                value_tmp.append(self.convert_dico[c])
            self.display_criterias.set(value_tmp)
        
    def move_down(self):
        selected = self.list_crit.curselection()
        if selected[0]<len(self.true_criterias)-1:
            self.true_criterias.insert(selected[0]+1,self.true_criterias.pop(selected[0]))
            value_tmp = []
            for c in self.true_criterias:
                value_tmp.append(self.convert_dico[c])
            self.display_criterias.set(value_tmp)
    
    def save(self):
        save_prompt = tk.Toplevel(self.master)
        SaveWindow(save_prompt, self)
        self.master.wait_window(save_prompt)
        file = open(self.save_dir.get()+'/'+self.filename.get()+'.lcfg','w')
        file.write("Config-League\n")
        file.write(self.data_path+'\n')
        file.write(self.output_path+'\n')
        file.write(str(self.aller_retour.get() == 1)+'\n')
        file.write(str(self.pts_v.get())+'\n')
        file.write(str(self.pts_n.get())+'\n')
        file.write(str(self.pts_d.get())+'\n')
        for c in self.true_criterias:
            file.write(c+'\n')
        file.close()
        
    def receive_info(self, sd, fn):
        self.save_dir.set(sd.get())
        self.filename.set(fn.get())