# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:36:32 2020

@author: user
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from abc import ABCMeta, abstractmethod
import os
from championnat import make_championnat
from coupe import make_cup

def do_nothing():
    return 0

class EditMode:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def edit_mode(self): raise NotImplementedError
    
    @abstractmethod
    def return_data(self): raise NotImplementedError

class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.save_path = '.'
        self.filename = ''
        self.chapeau_0 = False
        self.nb_chapeaux = 0
        self.data = None
        self.chapeau = 0
        self.current_mode = None
        self.menu = None
        self.menu_new = None
        self.menu_edit = None
        self.menu_simulate = None
        self.menu_save_exit = None
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.create_main_menu()

    def create_main_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu_new = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Create new data', menu=self.menu_new)
        self.menu_new.add_cascade(label='Create new team data', command=self.create_team_creator)
        self.menu_new.add_cascade(label='Create new match', command=self.create_match_creator)
        self.menu_new.add_cascade(label='Create new league', command=do_nothing)
        self.menu_new.add_cascade(label='Create new cup', command=do_nothing)
        self.menu_edit = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Edit existing data', menu=self.menu_edit)
        self.menu_edit.add_cascade(label='Edit team data', command=self.create_team_editor)
        self.menu_edit.add_cascade(label='Load match settings', command=do_nothing)
        self.menu_edit.add_cascade(label='Load league settings', command=do_nothing)
        self.menu_edit.add_cascade(label='Load cup settings', command=do_nothing)
        self.menu_simulate = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Simulate competition', menu=self.menu_simulate)
        self.menu_simulate.add_cascade(label='Choose engine paramteres', command=do_nothing)
        self.menu_simulate.add_cascade(label='Launch simulation', command=self.start_simulation)
        self.menu_save_exit = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Finish work', menu=self.menu_save_exit)
        self.menu_save_exit.add_cascade(label='Save team', command=self.save_team_work)
        self.menu_save_exit.add_cascade(label='Save competition', command=self.save_param_work)
        self.menu_save_exit.add_cascade(label='Save team and quit', command=self.save_team_n_quit)
        self.menu_save_exit.add_cascade(label='Save competition and quit', command=self.save_param_n_quit)
        self.menu_save_exit.add_cascade(label='Quit', command=self.master.destroy)
        
    def start_simulation(self):
        self.current_mode.start()

    def create_team_creator(self):
        self.menu_save_exit.entryconfig('Save competition', state=tk.DISABLED)
        self.menu_save_exit.entryconfig('Save competition and quit', state=tk.DISABLED)
        self.menu_save_exit.entryconfig('Save team', state=tk.NORMAL)
        self.menu_save_exit.entryconfig('Save team and quit', state=tk.NORMAL)
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = TeamCreator(ttk.Frame(self.canvas))

    def create_team_editor(self):
        self.menu_save_exit.entryconfig('Save competition', state=tk.DISABLED)
        self.menu_save_exit.entryconfig('Save competition and quit', state=tk.DISABLED)
        self.menu_save_exit.entryconfig('Save team', state=tk.NORMAL)
        self.menu_save_exit.entryconfig('Save team and quit', state=tk.NORMAL)
        data_reader = TeamDataReader(self.master)
        data = data_reader.get_data()
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = TeamCreator(ttk.Frame(self.canvas), data)
        
    def create_match_creator(self):
        self.menu_save_exit.entryconfig('Save team', state=tk.DISABLED)
        self.menu_save_exit.entryconfig('Save team and quit', state=tk.DISABLED)
        self.menu_save_exit.entryconfig('Save competition', state=tk.NORMAL)
        self.menu_save_exit.entryconfig('Save competition and quit', state=tk.NORMAL)
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = MatchCreator(ttk.Frame(self.canvas))
        
    def save_team_work(self):
        dico_postes = {'Goalkeeper' : 'Gardien',
                       'Defender': 'Defenseur',
                       'Midfielder' : 'Milieu',
                       'Forward' : 'Attaquant'}
        data = self.current_mode.return_data()
        save_data = self.current_mode.return_savedir()
        ex_chapeaux = self.current_mode.return_chapeaux()
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
    
    def save_team_n_quit(self):
        self.save_team_work()
        self.master.destroy()
        
    def save_param_work(self):
        return 0
    
    def save_param_n_quit(self):
        self.save_param_work()
        self.master.destroy()
        
class MatchCreator(EditMode):
    def __init__(self, master=None):
        super().__init__()
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
        self.make_gui()
        
    def start(self):
        make_cup(nom_saison=self.data_path+'/', resultat_saison=self.output_path,
                 aller_retour=self.aller_retour.get(), finale_ar=self.aller_retour.get(),
                 buts_ext=self.buts_ext.get(), tab=self.tab.get(), liste_chapeaux=[1,2],
                 un_seul_tour=True, flag_exist=self.flags.get(), terrain_neutre=self.terrain_neutre.get())
        
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
        self.ar_button = ttk.Checkbutton(self.master, text = 'Play over two legs',
                                 variable = self.aller_retour)
        self.ar_button.grid(column = 0, row = 2, columnspan = 3, sticky = 'nsew')
        self.button_extx2 = ttk.Checkbutton(self.master, text = 'Away goals count double',
                                 variable = self.buts_ext)
        self.button_extx2.grid(column = 3, row = 2, columnspan = 3, sticky = 'nsew')
        self.tab_button = ttk.Checkbutton(self.master, text = 'Penalty shootout',
                                 variable = self.tab)
        self.tab_button.grid(column = 0, row = 3, columnspan = 3, sticky = 'nsew')
        self.button_neutral = ttk.Checkbutton(self.master, text = 'Play on neutral ground',
                                 variable = self.terrain_neutre)
        self.button_neutral.grid(column = 3, row = 3, columnspan = 3, sticky = 'nsew')
        self.flag_button = ttk.Checkbutton(self.master, text = 'Flags exist',
                                 variable = self.flags)
        self.flag_button.grid(column = 0, row = 4, columnspan = 3, sticky = 'nsew')
        self.master.pack()
        
class TeamDataReader():
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
        file=open(self.file_path)
        raw_text = file.readlines()
        file.close()
        raw_text.reverse()
        data['team_name'],data['flag'],_ = raw_text.pop().split(";")
        data['df'],data['mf'],data['fw'],_ = raw_text.pop().split(";")
        raw_text.reverse()
        data['player_list'] = raw_text
        return data
        
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

class TeamCreator(EditMode):
    def __init__(self, master=None, data={}):
        super().__init__()
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

def main():
    master = tk.Tk() 
    master.title('Football Simulator v0.3')
    master.geometry("650x750+200+100")
    MainMenu(master)
    master.focus()
    tk.mainloop()
    
if __name__ == "__main__":
    main()