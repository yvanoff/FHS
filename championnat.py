# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 05:29:11 2020

@author: alexa
"""

from scheduler import create_schedule
from data_ops import lecture_data, compte_rendu_class
from season_tools import simuler_saison, make_classement, make_buteurs
import os

def make_championnat(nom_saison = '', resultat_saison = '', m_retours = True,
                     criterias = ['diff', 'bp', 'conf'], pts = [3,1,0],
                     additional_arguments = {}):
    
    
    liste_equipe, data_equipe, stats_saison = lecture_data(nom_saison,
                                                           championnat = True)
    if not os.path.isdir(resultat_saison):
        os.mkdir(resultat_saison)
    os.chdir(resultat_saison)
    
    liste_matches = create_schedule(liste_equipe, retour = m_retours)
    
    simuler_saison(liste_matches, liste_equipe, data_equipe, stats_saison,
                   pts_v = pts[0], pts_n = pts[1], pts_d = pts[2],
                   additional_arguments=additional_arguments,
                   tiebreakers = criterias)
    
            
    
    classement = make_classement(liste_equipe, stats_saison,
                                 tiebreakers = criterias)
    
    
    
    podium_buts = make_buteurs(liste_equipe, stats_saison)
                
    
    compte_rendu_class(stats_saison, classement, podium_buts, )
    
    os.chdir('..')