# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 21:09:39 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from coupe import make_knockout, make_groupStage
from save_window import SaveWindow

class GroupStageCreator:
    def __init__(self, master=None, cfgfile = None):
        self.master = master
        self.data_path = '.'
        self.display_data_path = tk.StringVar()
        self.output_path = '.'
        self.display_output_path = tk.StringVar()
        self.aller_retour = tk.IntVar()
        self.chapeau_0 = tk.IntVar()
        self.chapeaux_exist = tk.IntVar()
        self.nb_chapeaux = tk.IntVar()
        self.pts_v = tk.IntVar()
        self.pts_n = tk.IntVar()
        self.pts_d = tk.IntVar()
        self.cup_nat = tk.IntVar()
        self.terrain_neutre = tk.IntVar()
        self.flags = tk.IntVar()
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
        self.teams_per_poule = tk.IntVar()
        self.nb_teams_qualified = tk.IntVar()
        if cfgfile != None:
            file = open(cfgfile,'r')
            data = file.readlines()
            file.close()
            if (data[0][:-1] == 'Config-GroupStage'):
                self.data_path = data[1][:-1]
                self.display_data_path.set('Current data directory: '+self.data_path)
                self.output_path = data[2][:-1]
                self.display_output_path.set('Current data directory: '+self.output_path)
                self.aller_retour.set(data[3][:-1] == 'True')
                self.cup_nat.set(data[4][:-1] == 'True')
                self.flags.set(data[5][:-1] == 'True')
                self.chapeaux_exist.set(data[6][:-1] == 'True')
                shift = 0
                if data[6][:-1] == 'True':
                    self.nb_chapeaux.set(int(data[7][:-1]))
                    self.chapeau_0.set(data[8][:-1] == 'True')
                    shift = 2
                self.terrain_neutre.set(data[7+shift][:-1] == 'True')
                self.teams_per_poule.set(int(data[8+shift][:-1]))
                self.nb_teams_qualified.set(int(data[9+shift][:-1]))
                self.pts_v.set(int(data[10+shift][:-1]))
                self.pts_n.set(int(data[11+shift][:-1]))
                self.pts_d.set(int(data[12+shift][:-1]))
                self.true_criterias[0] = data[13+shift][:-1]
                self.true_criterias[1] = data[14+shift][:-1]
                self.true_criterias[2] = data[15+shift][:-1]
                value_tmp = []
                for c in self.true_criterias:
                    value_tmp.append(self.convert_dico[c])
                self.display_criterias = tk.StringVar(value=value_tmp)
        self.make_gui()
        
    def dico_params(self):
        dico = {'terrain_neutre' : self.terrain_neutre.get()}
        return dico
        
    def start(self, params_moteur):
        liste_c = []
        if (self.chapeaux_exist.get()) == 1:
            for i in range(self.nb_chapeaux.get()):
                liste_c.append(i+1)
            if (self.chapeau_0.get() == 1):
                liste_c.append(0)
        make_groupStage(nom_saison=self.data_path+'/', resultat_saison=self.output_path,
                        coupe_nationale = (self.cup_nat.get() == 1),
                 aller_retour=self.aller_retour.get(),
                 liste_chapeaux=liste_c, nb_qualifies_poule=self.nb_teams_qualified.get(),
                 nb_equipe_poule = self.teams_per_poule.get(),
                 pts = [self.pts_v.get(),self.pts_n.get(),self.pts_d.get()],
                 criterias=self.true_criterias,
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
        self.ar_button = ttk.Checkbutton(self.master, text = 'Home and away matches',
                                 variable = self.aller_retour)
        self.ar_button.grid(column = 0, row = 2, columnspan = 2, sticky = 'nsew')
        self.nat_cup_button = ttk.Checkbutton(self.master, text = 'National cup',
                                 variable = self.cup_nat)
        self.nat_cup_button.grid(column = 2, row = 2, columnspan = 2, sticky = 'nsew')
        self.flags_button = ttk.Checkbutton(self.master, text = 'Flags exist',
                                 variable = self.flags)
        self.flags_button.grid(column = 4, row = 2, columnspan = 2, sticky = 'nsew')
        self.chapeau0_button = ttk.Checkbutton(self.master, text = 'Pot 0 enabled',
                                 variable = self.chapeau_0)
        self.chapeau0_button.grid(column = 2, row = 3, columnspan = 2, sticky = 'nsew')
        self.liste_chapeaux_button = tk.Spinbox(self.master, textvariable = self.nb_chapeaux,
                                           from_ = 1, to = 99)
        self.liste_chapeaux_button.grid(column = 4, row = 3, columnspan = 2, sticky = 'nsew')
        if self.chapeaux_exist.get() == 0:
            self.chapeau0_button['state']=tk.DISABLED
            self.liste_chapeaux_button['state']=tk.DISABLED
        self.chapeaux_button = ttk.Checkbutton(self.master, text = 'Pots',
                                          variable = self.chapeaux_exist,
                                          command = self.switch_chapeaux)
        self.chapeaux_button.grid(column = 0, row = 3, columnspan = 2, sticky = 'nsew')
        label_tpp = ttk.Label(self.master, text = 'Number of teams per group:')
        label_tpp.grid(column = 0, row = 4, columnspan = 2, sticky = 'nsew')
        self.box_tpp = ttk.Spinbox(self.master, textvariable = self.teams_per_poule, from_ = 3, to = 16)
        self.box_tpp.grid(column = 0, row = 5, columnspan = 2, sticky = 'nsew')
        label_qtpp = ttk.Label(self.master, text = 'Number of qualified teams per group:')
        label_qtpp.grid(column = 2, row = 4, columnspan = 2, sticky = 'nsew')
        self.box_qtpp = ttk.Spinbox(self.master, textvariable = self.nb_teams_qualified, from_ = 1, to = 16)
        self.box_qtpp.grid(column = 2, row = 5, columnspan = 2, sticky = 'nsew')
        self.button_neutral = ttk.Checkbutton(self.master, text = 'Play on neutral ground',
                                 variable = self.terrain_neutre)
        self.button_neutral.grid(column = 4, row = 4, columnspan = 2, rowspan = 2, sticky = 'nsew')
        label_v = ttk.Label(self.master, text = 'Number of points for a win:')
        label_v.grid(column = 0, row = 6, columnspan = 2, sticky = 'nsew')
        self.box_v = ttk.Spinbox(self.master, textvariable = self.pts_v, from_ = 2, to = 4)
        self.box_v.grid(column = 0, row = 7, columnspan = 2, sticky = 'nsew')
        label_n = ttk.Label(self.master, text = 'Number of points for a draw:')
        label_n.grid(column = 2, row = 6, columnspan = 2, sticky = 'nsew')
        self.box_n = ttk.Spinbox(self.master, textvariable = self.pts_n, from_ = 1, to = 2)
        self.box_n.grid(column = 2, row = 7, columnspan = 2, sticky = 'nsew')
        label_p = ttk.Label(self.master, text = 'Number of points for a loss:')
        label_p.grid(column = 4, row = 6, columnspan = 5, sticky = 'nsew')
        self.box_d = ttk.Spinbox(self.master, textvariable = self.pts_d, from_ = 0, to = 1)
        self.box_d.grid(column = 4, row = 7, columnspan = 2, sticky = 'nsew')
        self.label_crit = ttk.Label(self.master, text = 'Rank the tie-breaking criterias to use:')
        self.label_crit.grid(column = 0, row = 8, columnspan = 6, sticky = 'nsew')
        self.list_crit = tk.Listbox(self.master,listvariable = self.display_criterias)
        self.list_crit.grid(column = 0, row = 9, columnspan = 6, sticky = 'nsew')
        self.button_up = ttk.Button(self.master, command = self.move_up,
                            text = 'Rank up')
        self.button_up.grid(column = 0, row = 10, columnspan = 3, sticky = 'nsew')
        self.button_down = ttk.Button(self.master, command = self.move_down,
                            text = 'Rank down')
        self.button_down.grid(column = 3, row = 10, columnspan = 3, sticky = 'nsew')
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
            
    def switch_chapeaux(self):
        if (self.chapeaux_exist.get() == 0):
            self.chapeau0_button['state']=tk.DISABLED
            self.liste_chapeaux_button['state']=tk.DISABLED
        else:
            self.chapeau0_button['state']=tk.NORMAL
            self.liste_chapeaux_button['state']=tk.NORMAL
    
    def save(self):
        save_prompt = tk.Toplevel(self.master)
        SaveWindow(save_prompt, self)
        self.master.wait_window(save_prompt)
        file = open(self.save_dir.get()+'/'+self.filename.get()+'.gcfg','w')
        file.write("Config-GroupStage\n")
        file.write(self.data_path+'\n')
        file.write(self.output_path+'\n')
        file.write(str(self.aller_retour.get() == 1)+'\n')
        file.write(str(self.cup_nat.get() == 1)+'\n')
        file.write(str(self.flags.get() == 1)+'\n')
        file.write(str(self.chapeaux_exist.get() == 1)+'\n')
        if (self.chapeaux_exist.get() == 1):
            file.write(str(self.nb_chapeaux.get())+'\n')
            file.write(str(self.chapeau_0.get() == 1)+'\n')
        file.write(str(self.terrain_neutre.get() == 1)+'\n')
        file.write(str(self.teams_per_poule.get())+'\n')
        file.write(str(self.nb_teams_qualified.get())+'\n')
        file.write(str(self.pts_v.get())+'\n')
        file.write(str(self.pts_n.get())+'\n')
        file.write(str(self.pts_d.get())+'\n')
        for c in self.true_criterias:
            file.write(c+'\n')
        file.close()
        
    def receive_info(self, sd, fn):
        self.save_dir.set(sd.get())
        self.filename.set(fn.get())
        
class KnockoutCreator:
    def __init__(self, master=None, cfgfile = None):
        self.master = master
        self.data_path = '.'
        self.display_data_path = tk.StringVar()
        self.output_path = '.'
        self.display_output_path = tk.StringVar()
        self.aller_retour = tk.IntVar()
        self.finale_ar = tk.IntVar()
        self.buts_ext = tk.IntVar()
        self.flags = tk.IntVar()
        self.terrain_neutre = tk.IntVar()
        self.tab = tk.IntVar()
        self.prolongations = tk.IntVar()
        self.chapeau_0 = tk.IntVar()
        self.chapeaux_exist = tk.IntVar()
        self.nb_chapeaux = tk.IntVar()
        self.cup_nat = tk.IntVar()
        self.one_round = tk.IntVar()
        self.name_round = tk.StringVar()
        self.save_dir = tk.StringVar()
        self.filename = tk.StringVar()
        if cfgfile != None:
            file = open(cfgfile,'r')
            data = file.readlines()
            file.close()
            if (data[0][:-1] == 'Config-KnockOut'):
                self.data_path = data[1][:-1]
                self.display_data_path.set('Current data directory: '+self.data_path)
                self.output_path = data[2][:-1]
                self.display_output_path.set('Current data directory: '+self.output_path)
                self.aller_retour.set(data[3][:-1] == 'True')
                self.finale_ar.set(data[4][:-1] == 'True')
                self.flags.set(data[5][:-1] == 'True')
                self.cup_nat.set(data[6][:-1] == 'True')
                self.chapeaux_exist.set(data[7][:-1] == 'True')
                shift = 0
                if data[7][:-1] == 'True':
                    self.nb_chapeaux.set(int(data[8][:-1]))
                    self.chapeau_0.set(data[9][:-1] == 'True')
                    shift = 2
                self.prolongations.set(data[8+shift][:-1] == 'True')
                self.tab.set(data[9+shift][:-1] == 'True')
                self.buts_ext.set(data[10+shift][:-1] == 'True')
                self.terrain_neutre.set(data[11+shift][:-1] == 'True')
                self.one_round.set(data[12+shift][:-1] == 'True')
                if data[12+shift][:-1] == 'True':
                    self.name_round.set(data[13+shift][:-1])
        self.make_gui()
        
    def dico_params(self):
        dico = {'buts_ext_2' : self.buts_ext.get(),
                'prolongations' : self.prolongations.get(),
                'tab' : self.tab.get(),
                'terrain_neutre' : self.terrain_neutre.get()}
        return dico
        
    def start(self, params_moteur):
        if (self.one_round.get() == 1):
            params_moteur['nom tour'] = self.name_round.get()
        liste_c = []
        if (self.chapeaux_exist.get()) == 1:
            for i in range(self.nb_chapeaux.get()):
                liste_c.append(i+1)
            if (self.chapeau_0.get() == 1):
                liste_c.append(0)
        make_knockout(nom_saison=self.data_path+'/', resultat_saison=self.output_path,
                      coupe_nationale = (self.cup_nat.get() == 1),
                 aller_retour=self.aller_retour.get(), finale_ar=self.finale_ar.get(),
                 liste_chapeaux=liste_c, un_seul_tour=(self.one_round.get()==1),
                 flag_exist=(self.flags.get()==1), add_args=params_moteur)
        
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
        
        self.chapeau0_button = ttk.Checkbutton(self.master, text = 'Pot 0 enabled',
                                 variable = self.chapeau_0)
        self.chapeau0_button.grid(column = 2, row = 2, columnspan = 2, sticky = 'nsew')
        self.liste_chapeaux_button = tk.Spinbox(self.master, textvariable = self.nb_chapeaux,
                                           from_ = 1, to = 99)
        self.liste_chapeaux_button.grid(column = 4, row = 2, columnspan = 2, sticky = 'nsew')
        if (self.chapeaux_exist.get() == 0):
            self.chapeau0_button['state']=tk.DISABLED
            self.liste_chapeaux_button['state']=tk.DISABLED
        self.chapeaux_button = ttk.Checkbutton(self.master, text = 'Pots',
                                          variable = self.chapeaux_exist,
                                          command = self.switch_chapeaux)
        self.chapeaux_button.grid(column = 0, row = 2, columnspan = 2, sticky = 'nsew')
        
        self.prol_button = ttk.Checkbutton(self.master, text = 'Extra Time',
                                 variable = self.prolongations)
        self.prol_button.grid(column = 0, row = 3, columnspan = 3, sticky = 'nsew')
        self.tab_button = ttk.Checkbutton(self.master, text = 'Penalty shootout',
                                 variable = self.tab)
        self.tab_button.grid(column = 3, row = 3, columnspan = 3, sticky = 'nsew')
        
        self.button_neutral = ttk.Checkbutton(self.master, text = 'Play on neutral ground',
                                 variable = self.terrain_neutre)
        self.button_neutral.grid(column = 0, row = 4, columnspan = 2, sticky = 'nsew')
        self.nat_cup_button = ttk.Checkbutton(self.master, text = 'National cup',
                                 variable = self.cup_nat)
        self.nat_cup_button.grid(column = 2, row = 4, columnspan = 2, sticky = 'nsew')
        self.flag_button = ttk.Checkbutton(self.master, text = 'Flags exist',
                                 variable = self.flags)
        self.flag_button.grid(column = 4, row = 4, columnspan = 2, sticky = 'nsew')
        
        self.ar_button = ttk.Checkbutton(self.master, text = 'Play over two legs',
                                 variable = self.aller_retour, command = self.switch_finale)
        self.ar_button.grid(column = 0, row = 5, columnspan = 2, sticky = 'nsew')
        self.finale_ar_button = ttk.Checkbutton(self.master, text = 'Play final over two legs',
                                 variable = self.finale_ar)
        self.finale_ar_button.grid(column = 2, row = 5, columnspan = 2, sticky = 'nsew')
        if (self.aller_retour.get() == 0):
            self.finale_ar_button['state']=tk.DISABLED
        self.button_extx2 = ttk.Checkbutton(self.master, text = 'Away goals count double',
                                 variable = self.buts_ext)
        self.button_extx2.grid(column = 4, row = 5, columnspan = 5, sticky = 'nsew')
        if (self.aller_retour.get() == 0):
            self.button_extx2['state']=tk.DISABLED
        
        self.one_round_button = ttk.Checkbutton(self.master, text = 'One round only',
                                          variable = self.one_round,
                                          command = self.switch_round)
        self.one_round_button.grid(column = 0, row = 6, columnspan = 2, sticky = 'nsew')
        self.text_name_round = ttk.Label(self.master, text = 'Name of the round:')
        self.text_name_round.grid(column = 2, row = 6, columnspan = 2, sticky = 'nsew')
        self.name_round_entry = ttk.Entry(self.master, textvariable = self.name_round)
        self.name_round_entry.grid(column = 4, row = 6, columnspan = 2, sticky = 'nsew')
        if (self.one_round.get() == 0):
            self.name_round_entry['state']=tk.DISABLED
        self.master.pack()
        
    def switch_chapeaux(self):
        if (self.chapeaux_exist.get() == 0):
            self.chapeau0_button['state']=tk.DISABLED
            self.liste_chapeaux_button['state']=tk.DISABLED
        else:
            self.chapeau0_button['state']=tk.NORMAL
            self.liste_chapeaux_button['state']=tk.NORMAL
            
    def switch_round(self):
        if (self.one_round.get() == 0):
            self.name_round_entry['state']=tk.DISABLED
        else:
            self.name_round_entry['state']=tk.NORMAL
            
    def switch_finale(self):
        if (self.aller_retour.get() == 0):
            self.finale_ar_button['state']=tk.DISABLED
            self.button_extx2['state']=tk.DISABLED
        else:
            self.finale_ar_button['state']=tk.NORMAL
            self.button_extx2['state']=tk.NORMAL
    
    def save(self):
        save_prompt = tk.Toplevel(self.master)
        SaveWindow(save_prompt, self)
        self.master.wait_window(save_prompt)
        file = open(self.save_dir.get()+'/'+self.filename.get()+'.kcfg','w')
        file.write("Config-KnockOut\n")
        file.write(self.data_path+'\n')
        file.write(self.output_path+'\n')
        file.write(str(self.aller_retour.get() == 1)+'\n')
        file.write(str(self.finale_ar.get() == 1)+'\n')
        file.write(str(self.flags.get() == 1)+'\n')
        file.write(str(self.cup_nat.get() == 1)+'\n')
        file.write(str(self.chapeaux_exist.get() == 1)+'\n')
        if (self.chapeaux_exist.get() == 1):
            file.write(str(self.nb_chapeaux.get())+'\n')
            file.write(str(self.chapeau_0.get() == 1)+'\n')
        file.write(str(self.prolongations.get() == 1)+'\n')
        file.write(str(self.tab.get() == 1)+'\n')
        file.write(str(self.buts_ext.get() == 1)+'\n')
        file.write(str(self.terrain_neutre.get() == 1)+'\n')
        file.write(str(self.one_round.get() == 1)+'\n')
        if (self.one_round.get() == 1):
            file.write(self.name_round.get()+'\n')
        file.close()
        
    def receive_info(self, sd, fn):
        self.save_dir.set(sd.get())
        self.filename.set(fn.get())