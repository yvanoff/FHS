# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:45:30 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from player_manager import PlayerWindow
import os

class TeamDataReader:
    def __init__(self, master = None):
        self.master = master
        self.file_path = ''
        self.raw_data = ''
        self.file_path = tk.filedialog.askopenfile(initialdir = ".",
                                  title = "Choose team data to load",
                                           filetypes = (("data files","*.data"),
                                                        ("all files","*.*"))).name
        
    def get_data(self):
        data = {}
        broken_path = self.file_path.split('/')
        data['filename'] = broken_path[-1].split('.')[0]
        if broken_path[-2][:-1] == "chapeau_":
            data['chapeau'] = int(broken_path[-2][-1])
            data['save_path'] = '/'.join(broken_path[:-2]) + '/'
        else:
            data['save_path'] = '/'.join(broken_path[:-1])
        file=open(self.file_path,'r')
        raw_text = file.readlines()
        file.close()
        raw_text.reverse()
        data['team_name'],data['flag'],_ = raw_text.pop().split(";")
        data['df'],data['mf'],data['fw'],_ = raw_text.pop().split(";")
        raw_text.reverse()
        data['player_list'] = raw_text
        return data


class TeamCreator:
    def __init__(self, master=None, data={}):
        self.master = master
        self.save_path = '.'
        self.display_path = tk.StringVar()
        self.team_name = tk.StringVar()
        self.flag = tk.StringVar()
        self.internal_players = ['']
        self.filename = tk.StringVar()
        self.chapeaux_exist = tk.IntVar()
        self.chapeau_0 = tk.IntVar()
        self.nb_chapeaux = tk.IntVar()
        self.chapeau = tk.StringVar(value='None')
        self.nb_df = tk.StringVar()
        self.nb_mf = tk.StringVar()
        self.nb_fw = tk.StringVar()
        self.existing_data = data
        if self.existing_data != {}:
            self.save_path = self.existing_data['save_path']
            self.team_name.set(self.existing_data['team_name'])
            self.flag.set(self.existing_data['flag'])
            self.internal_players = self.init_player_list(data['player_list'])
            self.filename.set(data['filename'])
            if 'chapeau' in self.existing_data:
                self.chapeaux_exist.set(1)
                self.chapeau_0.set(int(self.existing_data['chapeau']==0))
                self.nb_chapeaux.set(max(1,self.existing_data['chapeau']))
                self.chapeau.set(str(self.existing_data['chapeau']))
            self.nb_df = self.existing_data['df']
            self.nb_mf = self.existing_data['mf']
            self.nb_fw = self.existing_data['fw']
        self.list_joueurs = tk.StringVar(value=self.internal_players)
        self.display_path.set('Current save directory: '+self.save_path)
        self.make_gui()
        
    def make_gui(self):
        self.label_path = ttk.Label(self.master, text = self.save_path)
        self.label_path['textvariable'] = self.display_path
        self.label_path.grid(column = 0, row = 0, columnspan = 3, sticky = 'nsew')
        self.button_path = ttk.Button(self.master, command = self.ask_dir,
                            text = 'Choose save directory')
        self.button_path.grid(column = 0, row = 1, columnspan = 3, sticky = 'nsew')
        self.filename_text = ttk.Label(self.master, text = 'Save file as:')
        self.filename_text.grid(column = 0, row = 2, columnspan = 2, sticky = 'nsew')
        self.entry_filename = ttk.Entry(self.master, textvariable = self.filename)
        self.entry_filename.grid(column = 2, row = 2, sticky = 'nsew')
        self.chapeau0_button = ttk.Checkbutton(self.master, text = 'Pot 0 enabled',
                                 variable = self.chapeau_0)
        self.chapeau0_button.grid(column = 4, row = 1, columnspan = 3, sticky = 'nsew')
        self.liste_chapeaux_button = tk.Spinbox(self.master, textvariable = self.nb_chapeaux,
                                           from_ = 1, to = 99)
        self.liste_chapeaux_button.grid(column = 4, row = 2, columnspan = 3, sticky = 'nsew')
        self.chapeau0_button['state']=tk.DISABLED
        self.liste_chapeaux_button['state']=tk.DISABLED
        self.chapeaux_button = ttk.Checkbutton(self.master, text = 'Pots',
                                          variable = self.chapeaux_exist,
                                          command = self.switch_chapeaux)
        self.chapeaux_button.grid(column = 4, row = 0, columnspan = 3, sticky = 'nsew')
        self.text_nom_team = ttk.Label(self.master, text = 'Team name:')
        self.text_nom_team.grid(column = 0, row = 3, sticky = 'nsew')
        self.nom_team_entry = ttk.Entry(self.master, textvariable = self.team_name)
        self.nom_team_entry.grid(column = 1, row = 3, sticky = 'nsew')
        self.text_flag_team = ttk.Label(self.master, text = 'Flag:')
        self.text_flag_team.grid(column = 2, row = 3, sticky = 'nsew')
        self.nom_flag_entry = ttk.Entry(self.master, textvariable = self.flag)
        self.nom_flag_entry.grid(column = 3, row = 3, sticky = 'nsew')
        self.text_nom_team = ttk.Label(self.master, text = 'Pot:')
        self.text_nom_team.grid(column = 4, row = 3, sticky = 'nsew')
        self.nom_pot_entry = ttk.Entry(self.master, textvariable = self.chapeau)
        self.nom_pot_entry.grid(column = 5, row = 3, sticky = 'nsew')
        self.nom_pot_entry['state']=tk.DISABLED
        self.text_nb_df = ttk.Label(self.master, text = 'Number of defenders:')
        self.text_nb_df.grid(column = 0, row = 4, sticky = 'nsew')
        self.nb_df_entry = ttk.Entry(self.master, textvariable = self.nb_df)
        self.nb_df_entry.grid(column = 1, row = 4, sticky = 'nsew')
        self.text_nb_mf = ttk.Label(self.master, text = 'Number of midfielders:')
        self.text_nb_mf.grid(column = 2, row = 4, sticky = 'nsew')
        self.nb_mf_entry = ttk.Entry(self.master, textvariable = self.nb_mf)
        self.nb_mf_entry.grid(column = 3, row = 4, sticky = 'nsew')
        self.text_nb_fw = ttk.Label(self.master, text = 'Number of forwards:')
        self.text_nb_fw.grid(column = 4, row = 4, sticky = 'nsew')
        self.nb_fw_entry = ttk.Entry(self.master, textvariable = self.nb_fw)
        self.nb_fw_entry.grid(column = 5, row = 4, sticky = 'nsew')
        self.list_player = tk.Listbox(self.master,listvariable = self.list_joueurs)
        self.list_player.grid(column = 0, row = 5, columnspan = 6, sticky = 'nsew')
        self.add_player_button = ttk.Button(self.master, command = self.add_player,
                                       text = 'Add player')
        self.add_player_button.grid(column = 0, row = 6, columnspan = 2, sticky = 'nsew')
        self.edit_player_button = ttk.Button(self.master, command = self.edit_player,
                                       text = 'Edit player')
        self.edit_player_button.grid(column = 2, row = 6, columnspan = 2, sticky = 'nsew')
        self.add_player_button = ttk.Button(self.master, command = self.remove_player,
                                       text = 'Remove player')
        self.add_player_button.grid(column = 4, row = 6, columnspan = 2, sticky = 'nsew')
        self.master.pack()
        
    def init_player_list(self, players):
        dico_postes = {'Gardien' : 'Goalkeeper',
               'Defenseur' : 'Defender',
               'Milieu' : 'Midfielder',
               'Attaquant' : 'Forward'}
        list_res = []
        for p in players:
            string_p = ''
            p_split = p.split(";")
            string_p += p_split[0]
            if '/' in p_split[1]:
                pp_split = p_split[1].split('/')
                pp_split.reverse()
                string_p += (", "+dico_postes[pp_split.pop()]+
                             ", "+str(p_split[2]))+", "
                pp_split.reverse()
                for pos in pp_split:
                    if pos != '':
                        string_p += dico_postes[pos]+'/'
                string_p = string_p[:-1]
            else:
                string_p += (", "+dico_postes[p_split[1]]+
                             ", "+str(p_split[2]))
            if p_split[3] == "1":
                string_p += ', Penalty taker'
            list_res.append(string_p)
        return list_res
        
    def switch_chapeaux(self):
        if (self.chapeaux_exist.get() == 0):
            self.chapeau0_button['state']=tk.DISABLED
            self.liste_chapeaux_button['state']=tk.DISABLED
            self.nom_pot_entry['state']=tk.DISABLED
        else:
            self.chapeau0_button['state']=tk.NORMAL
            self.liste_chapeaux_button['state']=tk.NORMAL
            self.nom_pot_entry['state']=tk.NORMAL
            
    def ask_dir(self):
        self.save_path = tk.filedialog.askdirectory(initialdir = self.save_path,
                                                    title = "Select file")
        self.display_path.set('Current save directory: '+self.save_path)
        
    def add_player(self):
        PlayerWindow(self.master, self.internal_players, self.list_joueurs)
        
    def edit_player(self):
        PlayerWindow(self.master, self.internal_players, self.list_joueurs,
                     self.list_player.curselection())
    
    def remove_player(self):
        #pop-up de confirmation ?
        selected = self.list_player.curselection()
        if len(self.internal_players) == 1:
            self.internal_players.append('')
        self.internal_players.pop(selected[0])
        self.list_joueurs.set(self.internal_players)
    
    def return_chapeaux(self):
        return(self.chapeaux_exist.get() == 1, self.chapeau_0.get() == 1,
               self.nb_chapeaux.get())
    
    def return_savedir(self):
        return (self.save_path, self.filename.get(), self.chapeau.get())
    
    def edit_mode(self):
        return 'Team'
    
    def return_data(self):
        dico_data = {'teamname' : self.team_name.get(),
                     'flag' : self.flag.get(),
                     'formation' : [self.nb_df.get(),
                                    self.nb_mf.get(),
                                    self.nb_fw.get()],
                     'joueurs' : self.internal_players
                     }
        return dico_data    
    
    # à revoir suite au déplacement du GUI principal à ici
    # bcp de trucs sont devenus inutiles (ex: les appels à self.savedir())
    def save(self):
        dico_postes = {'Goalkeeper' : 'Gardien',
                       'Defender': 'Defenseur',
                       'Midfielder' : 'Milieu',
                       'Forward' : 'Attaquant'}
        data = self.return_data()
        save_data = self.return_savedir()
        ex_chapeaux = self.return_chapeaux()
        if not os.path.isdir(save_data[0]):
            os.mkdir(save_data[0])
        if ex_chapeaux[0]:
            for i in range(ex_chapeaux[2]):
                if not os.path.isdir(save_data[0]+'/'+'chapeau_'+str(i+1)):
                    os.mkdir(save_data[0]+'/'+'chapeau_'+str(i+1))
            if ex_chapeaux[1] & (not os.path.isdir(save_data[0]+'/'+'chapeau_0')):
                os.mkdir(save_data[0]+'/'+'chapeau_0')
        chapeau = ''
        if save_data[2] != 'None':
            chapeau = 'chapeau_'+save_data[2]+'/'
        file = open(save_data[0]+'/'+chapeau+save_data[1]+'.data','w')
        file.write(data['teamname']+';'+data['flag']+';')
        file.write('\n'+data['formation'][0]+';'+data['formation'][1]+';'+
                   data['formation'][2]+';')
        for j in data['joueurs']:
            player_data = j.split(", ")
            name = player_data[0]
            pos = dico_postes[player_data[1]]
            force = int(player_data[2])
            pen = '1' if "Penalty taker" in player_data else '0'
            if len(player_data) >= 4:
                if player_data[3] != "Penalty taker":
                    if '/' in player_data[3]:
                        for p in player_data[3].split('/'):
                            pos += "/"+dico_postes[p]
                    else:
                        pos += "/"+dico_postes[player_data[3]]
            file.write('\n'+name+";"+pos+";"+str(force)+";"+pen+";")
        file.close()