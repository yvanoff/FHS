# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 05:29:11 2020

Core program file

@author: alexa
"""

from scheduler import create_schedule
from data_ops import lecture_data, compte_rendu_class
from season_tools import simuler_saison, make_classement, make_buteurs
import os

def make_championnat(nom_saison, resultat_saison, m_retours = True,
                     criterias = ['diff', 'bp', 'conf'], pts = [3,1,0],
                     additional_arguments = {}):

    """
    Simulates a league.

    A league is a type of tournament where every team plays one another at least once (possibly more).

    Results are stored into the output folder, under the form of a .txt file containing the final league table and
    individual folders for each matchday containing each individual match report

    Parameters
    ----------
    nom_saison : str
                The name of the folder where the teams' data to load is located
    resultat_saison : str
                The name of the folder where results will be stored
    m_retours : bool, optional
                The number of times teams play each other - once or twice.
    criterias : list of str, optional
                The tie-breaker criterias to use in case two teams are tied in point total, ranked in order of use.
                The three criterias supported are:
                diff, goal difference
                bp, number of goals scored
                conf, the result of the match(s) between the two tied teams
    pts : list of int, optional
                Number of points for a win, a draw, and a loss, respectively.
    additional_arguments : dict
                Additional arguments to pass onto the football match simulator itself. Possible values detailed in
                match_foot documentation.
    """
    
    
    liste_equipe, data_equipe, stats_saison = lecture_data(nom_saison,
                                                           championnat = True)

    # dirty check to not have an error when creating the output folder
    # should be improved, see Issue #25
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