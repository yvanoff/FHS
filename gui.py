# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 17:36:32 2020

@author: user
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from match_manager import MatchCreator
from team_manager import TeamCreator, TeamDataReader
from cup_manager import GroupStageCreator,  KnockoutCreator
from league_manager import LeagueCreator
from save_window import SaveWindow

VERSION_NUMBER = 1.0

def do_nothing():
    return 0

class ParamsSaver:
    def __init__(self):
        self.filename = ""
        self.save_dir = ""
        
    def receive_info(self, sd, fn):
        self.save_dir = sd.get()
        self.filename = fn.get()
        
    def giveaway_info(self):
        return (self.save_dir, self.filename)

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
        self.moteur_params = {}

    def create_main_menu(self):
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu_new = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Create new data', menu=self.menu_new)
        self.menu_new.add_cascade(label='Create new team data', command=self.create_team_creator)
        self.menu_new.add_cascade(label='Create new match', command=self.create_match_creator)
        self.menu_new.add_cascade(label='Create new league', command=self.create_league_creator)
        self.menu_new.add_cascade(label='Create new group stage', command=self.create_group_creator)
        self.menu_new.add_cascade(label='Create new knockout competition', command=self.create_knockout_creator)
        self.menu_new.add_cascade(label='Create new complex cup', command=do_nothing)
        self.menu_edit = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Edit existing data', menu=self.menu_edit)
        self.menu_edit.add_cascade(label='Edit team data', command=self.create_team_editor)
        self.menu_edit.add_cascade(label='Load match settings', command=self.create_match_editor)
        self.menu_edit.add_cascade(label='Load league settings', command=self.create_league_editor)
        self.menu_edit.add_cascade(label='Load group stage settings', command=self.create_group_editor)
        self.menu_edit.add_cascade(label='Load knockout competition settings', command=self.create_knockout_editor)
        self.menu_edit.add_cascade(label='Load grocomplex cup settings', command=do_nothing)
        self.menu_simulate = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Simulate competition', menu=self.menu_simulate)
        self.menu_simulate.add_cascade(label='Choose engine paramteres', command=self.adjust_params)
        self.menu_simulate.add_cascade(label='Launch simulation', command=self.start_simulation)
        self.menu_save_exit = tk.Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label='Finish work', menu=self.menu_save_exit)
        self.menu_save_exit.add_cascade(label='Save', command=self.save_work)
        self.menu_save_exit.add_cascade(label='Save and quit', command=self.save_n_quit)
        self.menu_save_exit.add_cascade(label='Quit', command=self.master.destroy)
        
    def adjust_params(self):
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.bonus_dom = tk.StringVar()
        self.bonus_dom.set("1.025")
        self.pen_threshold = tk.StringVar()
        self.pen_threshold.set("0.08")
        self.proba_csc = tk.StringVar()
        self.proba_csc.set("0.003")
        self.penalty_term = tk.StringVar()
        self.penalty_term.set("2.0")
        self.proba_but_peno = tk.StringVar()
        self.proba_but_peno.set("0.7")
        bonus_dom_label = ttk.Label(self.canvas, text = 'Bonus multiplier to the home team\'s strength:')
        bonus_dom_label.grid(column = 0, row = 0, columnspan = 3, sticky = 'nsew')
        bonus_dom_entry = ttk.Entry(self.canvas, textvariable = self.bonus_dom)
        bonus_dom_entry.grid(column = 3, row = 0, columnspan = 3, sticky = 'nsew')
        bonus_dom_label = ttk.Label(self.canvas, text = 'Percentage of goals scored on penalties in the competition:')
        bonus_dom_label.grid(column = 0, row = 1, columnspan = 3, sticky = 'nsew')
        bonus_dom_entry = ttk.Entry(self.canvas, textvariable = self.pen_threshold)
        bonus_dom_entry.grid(column = 3, row = 1, columnspan = 3, sticky = 'nsew')
        bonus_dom_label = ttk.Label(self.canvas, text = 'Percentage of own goals in the competition:')
        bonus_dom_label.grid(column = 0, row = 2, columnspan = 3, sticky = 'nsew')
        bonus_dom_entry = ttk.Entry(self.canvas, textvariable = self.proba_csc)
        bonus_dom_entry.grid(column = 3, row = 2, columnspan = 3, sticky = 'nsew')
        bonus_dom_label = ttk.Label(self.canvas, text = 'A penalty term affecting the probability to score.\nLower this if teams have low strength, increase if they have high strength\n(range between 1.8-2.0 empirically):')
        bonus_dom_label.grid(column = 0, row = 3, columnspan = 3, sticky = 'nsew')
        bonus_dom_entry = ttk.Entry(self.canvas, textvariable = self.penalty_term)
        bonus_dom_entry.grid(column = 3, row = 3, columnspan = 3, sticky = 'nsew')
        bonus_dom_label = ttk.Label(self.canvas, text = 'Probability to score a penalty (used in penalty shootouts):')
        bonus_dom_label.grid(column = 0, row = 4, columnspan = 3, sticky = 'nsew')
        bonus_dom_entry = ttk.Entry(self.canvas, textvariable = self.proba_but_peno)
        bonus_dom_entry.grid(column = 3, row = 4, columnspan = 3, sticky = 'nsew')
        button_save = ttk.Button(self.canvas, command = self.save_dic,
                            text = 'Save the values')
        button_save.grid(column = 0, row = 5, columnspan = 2, sticky = 'nsew')
        button_export = ttk.Button(self.canvas, command = self.export_dic,
                            text = 'Export the values')
        button_export.grid(column = 2, row = 5, columnspan = 2, sticky = 'nsew')
        button_import = ttk.Button(self.canvas, command = self.import_dic,
                            text = 'Import the values')
        button_import.grid(column = 4, row = 5, columnspan = 2, sticky = 'nsew')
        
    def save_dic(self):
        self.moteur_params['bonus_dom'] = float(self.bonus_dom.get())
        self.moteur_params['pen_threshold'] = float(self.pen_threshold.get())
        self.moteur_params['proba_csc'] = float(self.proba_csc.get())
        self.moteur_params['penalty_term'] = float(self.penalty_term.get())
        self.moteur_params['proba_but_peno'] = float(self.proba_but_peno.get())
    
    def export_dic(self):
        self.save_dic()
        receiver = ParamsSaver()
        save_prompt = tk.Toplevel(self.master)
        SaveWindow(save_prompt, receiver)
        self.master.wait_window(save_prompt)
        savedir, fn = receiver.giveaway_info()
        file = open(savedir+'/'+fn+'.prm','w')
        file.write("Engine Parameters\n")
        file.write(str(self.moteur_params['bonus_dom'])+'\n')
        file.write(str(self.moteur_params['pen_threshold'])+'\n')
        file.write(str(self.moteur_params['proba_csc'])+'\n')
        file.write(str(self.moteur_params['penalty_term'])+'\n')
        file.write(str(self.moteur_params['proba_but_peno'])+'\n')
        file.close()
    
    def import_dic(self):
        source = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",
                                               filetypes = (("prm files","*.prm"),("all files","*.*")))
        file = open(source,'r')
        data = file.readlines()
        file.close()
        if (data[0][:-1] == 'Engine Parameters'):
            self.bonus_dom.set(data[1][:-1])
            self.pen_threshold.set(data[2][:-1])
            self.proba_csc.set(data[3][:-1])
            self.penalty_term.set(data[4][:-1])
            self.proba_but_peno.set(data[5][:-1])
        self.save_dic()
        
    def start_simulation(self):
        params = self.current_mode.dico_params()
        for p in params:
            self.moteur_params[p] = params[p]
            self.moteur_params[p] = params[p]
            self.moteur_params[p] = params[p]
            self.moteur_params[p] = params[p]
        self.current_mode.start(self.moteur_params)

    def create_team_creator(self):
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = TeamCreator(ttk.Frame(self.canvas))

    def create_team_editor(self):
        data_reader = TeamDataReader(self.master)
        data = data_reader.get_data()
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = TeamCreator(ttk.Frame(self.canvas), data)
        
    def create_match_creator(self):
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = MatchCreator(ttk.Frame(self.canvas))
        
    def create_match_editor(self):
        source = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",
                                               filetypes = (("mcfg files","*.mcfg"),("all files","*.*")))
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = MatchCreator(ttk.Frame(self.canvas),source)
        
    def create_league_creator(self):
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = LeagueCreator(ttk.Frame(self.canvas))
        
    def create_league_editor(self):
        source = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",
                                               filetypes = (("lcfg files","*.lcfg"),("all files","*.*")))
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = LeagueCreator(ttk.Frame(self.canvas),source)
        
    def create_group_creator(self):
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = GroupStageCreator(ttk.Frame(self.canvas))
        
    def create_group_editor(self):
        source = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",
                                               filetypes = (("gcfg files","*.gcfg"),("all files","*.*")))
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = GroupStageCreator(ttk.Frame(self.canvas),source)
        
    def create_knockout_creator(self):
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = KnockoutCreator(ttk.Frame(self.canvas))
        
    def create_knockout_editor(self):
        source = tk.filedialog.askopenfilename(initialdir = ".",title = "Select file",
                                               filetypes = (("kcfg files","*.kcfg"),("all files","*.*")))
        self.canvas.destroy()
        self.canvas = tk.Frame(master=self.master)
        self.canvas.pack()
        self.current_mode = KnockoutCreator(ttk.Frame(self.canvas),source)
        
    def save_n_quit(self):
        self.save_work()
        self.master.destroy()
        
    def save_work(self):
        self.current_mode.save()
    
def main():
    master = tk.Tk() 
    master.title('Football Simulator v'+str(VERSION_NUMBER))
    master.geometry("1000x750+200+100")
    MainMenu(master)
    master.focus()
    tk.mainloop()
    
if __name__ == "__main__":
    main()