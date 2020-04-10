# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 14:59:08 2020

@author: alexa
"""

import os
from moteur import match_foot
from data_ops import compte_rendu_match, compte_rendu_class
from copy import deepcopy
import random as rnd

def make_classement(liste_equipe, stats_saison,
                    tiebreakers = ['diff', 'bp', 'conf']):
    classement_final = []
    for equipe in liste_equipe:
        pts_eq = stats_saison[equipe+'_stats'][5]
        bp_eq = stats_saison[equipe+'_stats'][3]
        bc_eq = stats_saison[equipe+'_stats'][4]
        seek_insert = True
        pos_insert = 0
        for pos in classement_final:
            if seek_insert:
                nom_autre,pts,bp,bc = pos
                if pts > pts_eq:
                    pos_insert += 1
                elif pts == pts_eq:
                    tie_break = {'diff' : (bp - bc) < (bp_eq - bc_eq),
                                 'bp' : bp < bp_eq,
                                 'conf' : False}
                    if (bp - bc) == (bp_eq - bc_eq):
                        tie_break['diff'] = '0'
                    if bp == bp_eq:
                        tie_break['bp'] = '0'
                    own_index = liste_equipe.index(equipe)
                    index_autre = liste_equipe.index(nom_autre)
                    pts_conf = 0
                    bp_conf = 0
                    bc_conf = 0
                    own_b_ext_conf = 0
                    autre_b_ext_conf = 0
                    if stats_saison['res_totaux'][own_index][index_autre] != []:
                        bp_conf, autre_b_ext_conf = stats_saison['res_totaux'][own_index][index_autre]
                        if bp_conf > autre_b_ext_conf:
                            pts_conf += 3
                        elif bp_conf == autre_b_ext_conf:
                            pts_conf += 1
                    if stats_saison['res_totaux'][index_autre][own_index] != []:
                        bc_conf, own_b_ext_conf = stats_saison['res_totaux'][index_autre][own_index]
                        if own_b_ext_conf > bc_conf:
                            pts_conf += 3
                        elif own_b_ext_conf == bc_conf:
                            pts_conf += 1
                        bp_conf += own_b_ext_conf
                    bc_conf += autre_b_ext_conf
                    tie_break['conf'] = ((pts_conf >= 4) |
                            (((pts_conf == 3)|(pts_conf == 2)) & (bp_conf-bc_conf > 0)) |
                            (((pts_conf == 3)|(pts_conf == 2)) & ((bp_conf-bc_conf) == 0) &
                             (own_b_ext_conf > autre_b_ext_conf)))
                    if (((pts_conf == 3)|(pts_conf == 2)) & ((bp_conf-bc_conf) == 0) &
                             (own_b_ext_conf == autre_b_ext_conf)):
                        tie_break['conf'] = '0'
                    if tie_break[tiebreakers[0]] != '0':
                        seek_insert = not tie_break[tiebreakers[0]]
                        if seek_insert:
                            pos_insert += 1
                    elif tie_break[tiebreakers[1]] != '0':
                        seek_insert = not tie_break[tiebreakers[1]]
                        if seek_insert:
                            pos_insert += 1
                    elif tie_break[tiebreakers[2]] != '0':
                        seek_insert = not tie_break[tiebreakers[2]]
                        if seek_insert:
                            pos_insert += 1
                    else:
                        pos_insert += 1
                else:
                    seek_insert = False
        classement_final.insert(pos_insert,(equipe,pts_eq,bp_eq,bc_eq))
    return classement_final

def simuler_saison(liste_matches, liste_equipes, data_equipes, stats_saison,
                    pts_v = 3, pts_n = 1, pts_d = 0, poule = False,
                    additional_arguments = {}, tiebreakers = ['diff', 'bp', 'conf']):
    compteur_journee = 0
    stats_saison['res_totaux'] = []
    tmp = []
    for i in range(len(liste_equipes)):
        tmp.append([])
    for i in range(len(liste_equipes)):
        stats_saison['res_totaux'].append(deepcopy(tmp))
    for journee in liste_matches:
        compteur_journee +=1
        os.mkdir('J'+str(compteur_journee))
        os.chdir('J'+str(compteur_journee))
        for match in journee:
            equipe_dom, equipe_ext = match
            resultat = match_foot(data_equipes[equipe_dom],
                                  data_equipes[equipe_ext], additional_arguments)
            buts_dom = resultat[0]
            buts_ext = resultat[1]
            index_dom = liste_equipes.index(equipe_dom)
            index_ext = liste_equipes.index(equipe_ext)
            stats_saison['res_totaux'][index_dom][index_ext].append(buts_dom)
            stats_saison['res_totaux'][index_dom][index_ext].append(buts_ext)
            victoire_dom = (buts_dom > buts_ext)
            nul = (buts_dom == buts_ext)
            stats_saison[equipe_dom+'_stats'][3] += buts_dom
            stats_saison[equipe_dom+'_stats'][4] += buts_ext
            stats_saison[equipe_ext+'_stats'][3] += buts_ext
            stats_saison[equipe_ext+'_stats'][4] += buts_dom
            if victoire_dom:
                stats_saison[equipe_dom+'_stats'][0] += 1
                stats_saison[equipe_ext+'_stats'][2] += 1
                stats_saison[equipe_dom+'_stats'][5] += pts_v
                stats_saison[equipe_ext+'_stats'][5] += pts_d
            elif nul:
                stats_saison[equipe_dom+'_stats'][1] += 1
                stats_saison[equipe_ext+'_stats'][1] += 1
                stats_saison[equipe_dom+'_stats'][5] += pts_n
                stats_saison[equipe_ext+'_stats'][5] += pts_n
            else:
                stats_saison[equipe_dom+'_stats'][2] += 1
                stats_saison[equipe_ext+'_stats'][0] += 1
                stats_saison[equipe_dom+'_stats'][5] += pts_d
                stats_saison[equipe_ext+'_stats'][5] += pts_v
            if not poule:
                for but in resultat[2]:
                    buteur = but.split(',')[0]
                    for joueur in stats_saison[equipe_dom+'_joueurs']:
                        if (buteur == joueur[0]):
                            joueur[1] += 1
                for but in resultat[3]:
                    buteur = but.split(',')[0]
                    for joueur in stats_saison[equipe_ext+'_joueurs']:
                        if (buteur == joueur[0]):
                            joueur[1] += 1
            compte_rendu_match(equipe_dom, equipe_ext, stats_saison,
                               compteur_journee, resultat, poule)
        class_ = make_classement(liste_equipes, stats_saison, tiebreakers)
        compte_rendu_class(stats_saison, class_, poule=poule, quand = 'J'+str(compteur_journee))
        os.chdir('..')

def make_buteurs(liste_equipe, stats_saison):
    podium = [[[''], -1],
              [[''], -1],
              [[''], -1]]
    for equipe in liste_equipe:
        for joueur in stats_saison[equipe+'_joueurs']:
            nom, nb_buts = joueur
            if nb_buts > podium[0][1]:
                podium[2] = [podium[1][0], podium[1][1]]
                podium[1] = [podium[0][0], podium[0][1]]
                podium[0] = [[nom+','+equipe], nb_buts]
            elif nb_buts == podium[0][1]:
                podium[0][0].append(nom+','+equipe)
            elif nb_buts > podium[1][1]:
                podium[2] = [podium[1][0], podium[1][1]]
                podium[1] = [[nom+','+equipe], nb_buts]
            elif nb_buts == podium[1][1]:
                podium[1][0].append(nom+','+equipe)
            elif nb_buts > podium[2][1]:
                podium[2] = [[nom+','+equipe], nb_buts]
            elif nb_buts == podium[2][1]:
                podium[2][0].append(nom+','+equipe)
    return podium

def tirage_sort(liste_equipe, stats_equipes, equipes_ens = 2,
                is_coupe_nat = True, liste_chapeaux = [], groupes = {},
                flags_exist = True):
    nb_couples = int(len(liste_equipe)/equipes_ens)
    ok_group = False
    while not ok_group:
        liste_res = []
        liste_tirage = deepcopy(liste_equipe)
        for i in range(nb_couples):
            couple_added = []
            banned_flags = []
            for j in range(equipes_ens):
                liste_flags_eq = []
                liste_chapeaux_eq = []
                for k in liste_tirage:
                    liste_flags_eq.append(stats_equipes['flag_'+k])
                    liste_chapeaux_eq.append(stats_equipes['chapeau_'+k])
                bon_tirage = False
                selected_chapeau = (len(liste_chapeaux)>0)-1
                if (len(liste_chapeaux)-j > 0):
                    selected_chapeau = liste_chapeaux[j]
                    if not (selected_chapeau in liste_chapeaux_eq):
                        selected_chapeau = 0
                mandatory_flags = trouver_flags_importants(liste_flags_eq,
                                                           nb_couples - i,
                                                           liste_chapeaux_eq,
                                                           selected_chapeau)
                for f in banned_flags:
                    if f in mandatory_flags:
                        banned_flags.remove(f)
                while not bon_tirage:
                    eq_choisie = rnd.choice(liste_tirage)
                    index_eq = liste_tirage.index(eq_choisie)
                    flag_choisi = liste_flags_eq[index_eq]
                    chapeau_choix = liste_chapeaux_eq[index_eq]
                    bon_tirage = (((not (flag_choisi in banned_flags))|(banned_flags == [])) &
                                  ((flag_choisi in mandatory_flags)|is_coupe_nat|
                                   (mandatory_flags == [])) &
                                  ((chapeau_choix == selected_chapeau)|(liste_chapeaux == []))
                                  )
                if not is_coupe_nat:
                    banned_flags.append(flag_choisi)
                couple_added.append(eq_choisie)
                liste_tirage.remove(eq_choisie)
            if (flags_exist and is_coupe_nat and (equipes_ens == 2) and
                    (int(stats_equipes['flag_'+couple_added[0]]) <
                    int(stats_equipes['flag_'+couple_added[1]]))
                    and liste_chapeaux == []):
                couple_added = [couple_added[1], couple_added[0]]
            liste_res.append(couple_added)
        if groupes == {}:
            ok_group = True
        else:
            ok_group = True
            for m in liste_res:
                for e in m:
                    for f in m:
                        if (groupes[e] == groupes[f]) & (e != f):
                            ok_group = False
    return liste_res
            

            
def trouver_flags_importants(liste_flags, nb_matchups_restants,
                             liste_chapeaux = [],
                             selected_chapeau = -1):
    count_flag = {}
    flags_importants = []
    for i,j in zip(liste_flags,liste_chapeaux):
        if not (i in count_flag.keys()):
            count_flag[i] = [1, False]
        else:
            count_flag[i][0] += 1
        if  (j == selected_chapeau) | (selected_chapeau == -1):
            count_flag[i][1] = True
    for k in count_flag.keys():
        if (count_flag[k][0] >= nb_matchups_restants) & (count_flag[i][1]):
            flags_importants.append(k)
    return flags_importants

def determiner_vainqueur(equipe_dom, equipe_ext, resultat, agg_dom = -1,
                         agg_ext = -1, buts_ext_x2 = False):
    vainqueur = 'Personne'
    pts_dom = 0
    if agg_dom > agg_ext:
        pts_dom += 3
    elif agg_dom == agg_ext:
        pts_dom += 1
    if resultat[0] > resultat[1]:
        pts_dom += 3
    elif resultat[0] == resultat[1]:
        pts_dom += 1
    if pts_dom >= 4:
        vainqueur = equipe_dom
    elif pts_dom <= 1:
        vainqueur = equipe_ext
    else:
        if agg_dom+resultat[0] > agg_ext+resultat[1]:
            vainqueur = equipe_dom
        elif agg_dom+resultat[0] < agg_ext+resultat[1]:
            vainqueur = equipe_ext
        elif (agg_dom > resultat[1]) & buts_ext_x2:
            vainqueur = equipe_dom
        elif (agg_dom < resultat[1]) & buts_ext_x2:
            vainqueur = equipe_ext
        elif (resultat[5]['h'] > 0) | (resultat[5]['a'] > 0):
            vainqueur_tab = max(resultat[5], key=resultat[5].get)
            if vainqueur_tab == 'h':
                vainqueur = equipe_dom
            else:
                vainqueur = equipe_ext
    return vainqueur