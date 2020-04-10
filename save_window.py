# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:55:04 2020

@author: alexa
"""

import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

# Fait apparaître une fenêtre qui demande:
# un path + le nom du fichier à sauvegarder

class SaveWindow:
    
    def __init__(self, master=None, caller=None):
        self.master = master
        self.save_dir = tk.StringVar()
        self.save_dir.set('.')
        self.filename = tk.StringVar()
        self.father=caller
        self.ask_info()
        
    def ask_info(self):
        savedir_selection_button = ttk.Button(self.master, command = self.ask_dir,
                            text = 'Choose save directory')
        savedir_selection_button.grid(sticky = 'nsew')
        text_dir_entry = ttk.Label(self.master, text = 'Current save directory:')
        text_dir_entry.grid(sticky = 'nsew')
        dir_entry = ttk.Label(self.master, textvariable = self.save_dir)
        dir_entry.grid(sticky = 'nsew')
        text_entry = ttk.Label(self.master, text = 'Save file as:')
        text_entry.grid(sticky = 'nsew')
        filename_entry = ttk.Entry(self.master, textvariable = self.filename)
        filename_entry.grid(sticky = 'nsew')
        #un bouton de validation pour fermer la fenêtre
        # un bouton d'annulation
        self.valid = ttk.Button(self.master, command = self.give_info,
                                       text = 'OK')
        self.valid.grid(sticky = 'nsew')
        self.cancel = ttk.Button(self.master, command = self.master.destroy,
                                       text = 'Cancel')
        self.cancel.grid(sticky = 'nsew')
        
    def ask_dir(self):
        save_path = tk.filedialog.askdirectory(initialdir = self.save_dir,
                                                    title = "Select file")
        self.save_dir.set(save_path)
        
    def give_info(self):
        self.father.receive_info(self.save_dir, self.filename)
        self.master.destroy()