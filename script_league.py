from championnat import make_championnat
import tkinter as tk
import tkinter.filedialog

nom_saison = tk.filedialog.askdirectory(initialdir = '.', title = "Select data directory")+'/'
nom_res = tk.filedialog.askdirectory(initialdir = '.', title = "Select result directory")+'/'

criterias = ['diff', 'bp', 'conf']

additional_arguments = { 'prolongations' : False,
              'agg_dom' : 0,
              'agg_ext' : 0,
              'buts_ext_2' : False,
              'tab' : False,
              'terrain_neutre' : False,
              'bonus_dom' : 1.025,
              'pen_threshold' : 0.08,
              'proba_csc' : 0.003,
              'penalty_term' : 2.0,
              'proba_but_peno' : 0.7}

make_championnat(nom_saison=nom_saison, resultat_saison=nom_res,
                 criterias=criterias, additional_arguments=additional_arguments)