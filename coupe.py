# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:00:25 2020

Générateur de coupes

@author: alexa
"""

### Meilleur support chapeau

from moteur import match_foot
from data_ops import lecture_data, compte_rendu_class, compte_rendu_match
from season_tools import (tirage_sort, simuler_saison, make_classement,
                          determiner_vainqueur)
from scheduler import create_schedule
import os
from copy import deepcopy

def make_groupStage(nom_saison = '', resultat_saison = '', coupe_nationale = True,
             aller_retour = False, liste_chapeaux = [],
             nb_qualifies_poule = 2, nb_equipe_poule = 4,
             pts = [3,1,0],
             criterias = ['conf', 'diff', 'bp'], flag_exist = True,
             add_args = {}):
    
    
    
    liste_equipe, data_equipe, stats_saison = lecture_data(nom_saison,
                                                           flags = flag_exist,
                                                           chapeaux = liste_chapeaux)
    
    if not os.path.isdir(resultat_saison):
        os.mkdir(resultat_saison)
    os.chdir(resultat_saison)
    print(liste_equipe)

    
    groupes = {}
    
    liste_poules = tirage_sort(liste_equipe, stats_saison, nb_equipe_poule,
                               coupe_nationale, liste_chapeaux, flags_exist = flag_exist)
    compteur_poule = 65
    equipe_qualifiees = []
    for i in liste_poules:
        os.mkdir("Groupe_"+chr(compteur_poule))
        os.chdir("Groupe_"+chr(compteur_poule))
        compteur_poule += 1
        equipes_poule = []
        for j in i:
            groupes[j] = compteur_poule - 65
            equipes_poule.append(j)
        schedule = create_schedule(i, aller_retour)
        simuler_saison(schedule, equipes_poule, data_equipe, stats_saison,
               pts_v = pts[0], pts_n = pts[1], pts_d = pts[2], poule = True, additional_arguments=add_args)
        classement_final = make_classement(equipes_poule, stats_saison, criterias)
        compte_rendu_class(stats_saison, classement_final, poule = True)
        for k in range(nb_qualifies_poule):
            equipe_qualifiee,_,_,_ = classement_final[k]
            equipe_qualifiees.append((equipe_qualifiee,k+1,compteur_poule-65))
        os.chdir('..')
    
    os.chdir("..")
    
    return equipe_qualifiees
    
def make_knockout(nom_saison = '', resultat_saison = '', coupe_nationale = True,
             aller_retour = False, finale_ar = False,
             liste_chapeaux = [], groupes = {}, un_seul_tour = False,
             flag_exist = True, add_args = {}):
    
    nom_tours = {2 : 'Finale',
             4: 'Demis',
             8 : 'Quarts',
             16 : '8emes',
             32 : '16emes',
             64 : '32emes',
             128 : '64emes',
             -1 : 'Tour special'}
    
    if 'nom tour' in add_args:
        nom_tours[-1] = add_args['nom tour']
    
    liste_equipe, data_equipe, stats_saison = lecture_data(nom_saison,
                                                           flags = flag_exist,
                                                           chapeaux = liste_chapeaux)
    
    if not os.path.isdir(resultat_saison):
        os.mkdir(resultat_saison)
    os.chdir(resultat_saison)
    
    
    while len(liste_equipe)>=2:
        if not un_seul_tour:
            tour_actuel = nom_tours[len(liste_equipe)]
        else:
            tour_actuel = nom_tours[-1]
        if tour_actuel == 'Finale':
            aller_retour = finale_ar
            add_args['buts_ext_2'] = (add_args['buts_ext_2']) & (aller_retour)
            if not aller_retour:
                add_args['terrain_neutre'] = True
        os.mkdir(tour_actuel)
        os.chdir(tour_actuel)
        liste_matchs = tirage_sort(liste_equipe, stats_saison,
                                   is_coupe_nat = coupe_nationale,
                                   liste_chapeaux = liste_chapeaux,
                                   groupes = groupes, flags_exist = flag_exist)
        vainqueurs = []
        for m in liste_matchs:
            victoire = False
            nb_replays = 0
            equipe_dom,equipe_ext = m
            while not victoire:
                agg_dom = 0
                agg_ext = 0
                if aller_retour & (nb_replays == 0):
                    add_args_aller = deepcopy(add_args)
                    add_args_aller['prolongations'] = False
                    add_args_aller['tab'] = False
                    match_a = match_foot(data_equipe[equipe_ext],
                                         data_equipe[equipe_dom], add_args_aller)
                    compte_rendu_match(equipe_dom=equipe_ext, equipe_ext=equipe_dom,
                                       stats_saison=stats_saison, tour=tour_actuel,
                                       resultat=match_a, coupe = True, type_match='aller')
                    agg_dom = match_a[1]
                    agg_ext = match_a[0]
                marqueur_retour = ''
                if aller_retour:
                    marqueur_retour = 'retour'
                else:
                    marqueur_retour = 'coupe'
                args_match = add_args
                args_match['agg_dom'] = agg_dom
                args_match['agg_ext'] = agg_ext
                match_r = match_foot(data_equipe[equipe_dom],
                                     data_equipe[equipe_ext],
                                     args_match)
                compte_rendu_match(equipe_dom=equipe_dom, equipe_ext=equipe_ext,
                                   stats_saison=stats_saison, tour=tour_actuel,
                                   resultat=match_r, coupe=True,
                                   type_match=marqueur_retour, agg_dom=agg_dom,
                                   agg_ext=agg_ext, replay = nb_replays)
                vainqueur = determiner_vainqueur(equipe_dom,
                                                 equipe_ext, match_r,
                                                 agg_dom, agg_ext,
                                                 add_args['buts_ext_2'])
                victoire = (vainqueur != 'Personne')
                nb_replays += 1
                equipe_dom, equipe_ext = equipe_ext, equipe_dom
            vainqueurs.append(vainqueur)
        liste_equipe = deepcopy(vainqueurs)
        liste_chapeaux = []
        if un_seul_tour:
            break
        os.chdir('..')
        
    os.chdir("..")
        
    return liste_equipe
        