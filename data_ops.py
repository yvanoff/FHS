# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 11:39:46 2020

@author: alexa
"""

import os
from copy import deepcopy

def lecture_data(chemin, championnat = False, flags = False, chapeaux = []):
    liste_equipe = []

    data_equipe = {}
    stats_equipe = {}
    
    if chapeaux == []:
        list_equipe_raw = list(os.scandir(chemin)) 
    else:
        list_equipe_raw = []
        chapeaux_raw = []
        for c in chapeaux:
            scan_result = os.scandir(chemin+'chapeau_'+str(c)+'\\')
            for l in scan_result:
                list_equipe_raw.append(l)
                chapeaux_raw.append(c)
        if os.path.isdir(chemin+'chapeau_0\\') & (not(0 in chapeaux)):
            scan_result = os.scandir(chemin+'chapeau_0\\')
            for l in scan_result:
                list_equipe_raw.append(l)
                chapeaux_raw.append(0)
                
    for l in list_equipe_raw:
        nom_raw = l.name.split('.')[0]
        if l.name.split('.')[-1].lower() == "data":
            liste_equipe.append(nom_raw)
            if chapeaux == []:
                meta_data_file = open(chemin+l.name,'r')
                stats_equipe['chapeau_'+nom_raw] = 0
            else:
                chapeau_equipe = chapeaux_raw[list_equipe_raw.index(l)]
                meta_data_file = open(chemin+'chapeau_'+str(chapeau_equipe)+'\\'+l.name,'r')
                stats_equipe['chapeau_'+nom_raw] = chapeau_equipe
            meta_data = meta_data_file.readlines()
            meta_data_file.close()
            data_equipe[nom_raw] = deepcopy(meta_data)
            meta_data.reverse()
            stats_equipe[nom_raw],flag_eq,_ = meta_data.pop().split(';')
            stats_equipe[nom_raw+'_stats'] = [0,0,0,0,0,0] # V,N,D,BP,BC,pts
            if flags:
                stats_equipe['flag_'+nom_raw] = flag_eq
            else:
                stats_equipe['flag_'+nom_raw] = ''
            if championnat:
                meta_data.pop()
                meta_data.reverse()
                stats_equipe[nom_raw+'_joueurs'] = []
                for j in meta_data:
                    nom_joueur,_,_,_,_ = j.split(';')
                    stats_equipe[nom_raw+'_joueurs'].append([nom_joueur,0])
    return (liste_equipe, data_equipe, stats_equipe)

def compte_rendu_match(equipe_dom, equipe_ext, stats_saison, tour, resultat,
                       coupe = False, type_match = 'Simple', agg_dom = 0,
                       agg_ext = 0, replay = 0):
    marqueur_replay = ''
    marqueur_replay_rapport = ''
    if replay > 0:
        marqueur_replay = "_REPLAY_"+str(replay)
        marqueur_replay_rapport = ', '+str(replay)+'eme replay'
    marqueur_type = ''
    if type_match == 'aller':
        marqueur_type = 'ALLER_'
    elif type_match == 'retour':
        marqueur_type = 'RETOUR_'
    compte_rendu = open(marqueur_type+equipe_dom+'_'+equipe_ext+marqueur_replay+'.txt','w')
    marqueur_tour = ''
    if (type_match == 'coupe'):
        marqueur_tour = tour+marqueur_replay_rapport
    elif type_match == 'aller':
        marqueur_tour = tour+' aller'+marqueur_replay_rapport
    elif type_match == 'retour':
        marqueur_tour = tour + ' retour'+marqueur_replay_rapport
    else:
        marqueur_tour = 'Journee '+str(tour)
    compte_rendu.write(marqueur_tour+'\n')
    flag_d = ''
    flag_e = ''
    if coupe:
        if stats_saison['flag_'+equipe_dom] != '':
            flag_d = ' ('+stats_saison['flag_'+equipe_dom]+')'
        if stats_saison['flag_'+equipe_ext] != '':
            flag_e = ' ('+stats_saison['flag_'+equipe_ext]+')'
    marqueur_prol = ' '
    if resultat[4]:
        marqueur_prol = ' (A.P.) '
    compte_rendu.write(stats_saison[equipe_dom] + flag_d + ' ' + str(resultat[0]) +
                       ' - ' + str(resultat[1]) + marqueur_prol + stats_saison[equipe_ext] +
                       flag_e +'\n')
    if (resultat[0] > 0) | (resultat[1] > 0):
        compte_rendu.write('\n')
        compte_rendu.write('Buteurs:'+'\n')
        compte_rendu.write('\n')
        if resultat[0] > 0:
            compte_rendu.write(stats_saison[equipe_dom]+'\n')
            for but in resultat[2]:
                compte_rendu.write(but+'\n')
            compte_rendu.write('\n')
        if resultat[1] > 0:
            compte_rendu.write(stats_saison[equipe_ext]+'\n')
            for but in resultat[3]:
                compte_rendu.write(but+'\n')
    if type_match == 'retour':
        compte_rendu.write('\n\n')
        compte_rendu.write('Score du match aller: '+str(agg_dom)+' - '+str(agg_ext))
    if (resultat[5]['h'] > 0) | (resultat[5]['a'] > 0):
        compte_rendu.write('\n\n\n')
        compte_rendu.write('Tirs aux buts: '+str(resultat[5]['h']) + ' - '
                           + str(resultat[5]['a']))
        compte_rendu.write('\n\n')
        compte_rendu.write(stats_saison[equipe_dom])
        compte_rendu.write('\n')
        for tireur in resultat[6]['h']:
            compte_rendu.write('\n')
            resultat_tir = 'But' if tireur[1] else 'Echec'
            compte_rendu.write(tireur[0]+': '+resultat_tir)
        compte_rendu.write('\n\n')
        compte_rendu.write(stats_saison[equipe_ext])
        compte_rendu.write('\n')
        for tireur in resultat[6]['a']:
            compte_rendu.write('\n')
            resultat_tir = 'But' if tireur[1] else 'Echec'
            compte_rendu.write(tireur[0]+': '+resultat_tir)
    compte_rendu.close()


def compte_rendu_class(data_saison, classement, podium = [], poule = False,
                       quand = 'final'):
    compte_rendu_saison = open('compte_rendu.txt','w')
    if poule:
        compte_rendu_saison.write('Compte-rendu du groupe\n')
    else:
        compte_rendu_saison.write('Compte-rendu de la saison\n')
    compte_rendu_saison.write('\n')
    compte_rendu_saison.write('Classement ' +quand+'\n')
    current_pos = 0
    for e in classement:
        current_pos += 1
        equipe = data_saison[e[0]]
        e_stats = data_saison[e[0]+'_stats']
        flag_eq = ''
        if poule & (data_saison['flag_'+e[0]]!= ''):
            flag_eq = ' ('+data_saison['flag_'+e[0]]+')'
        compte_rendu_saison.write(str(current_pos)+'. '+equipe+flag_eq+', '+str(e_stats[5])+'pts, '+str(e_stats[0])+'V, '+
                                  str(e_stats[1])+'N, '+str(e_stats[2])+'D, '+str(e_stats[3])+'BP, '+str(e_stats[4])+
                                  'BC, Diff: '+str(e_stats[3]-e_stats[4])+'\n')
    if podium != []:
        compte_rendu_saison.write('\n')
        compte_rendu_saison.write('\n')
        compte_rendu_saison.write('\n')
        compte_rendu_saison.write('Classement des buteurs:\n')
        compte_rendu_saison.write('\n')
        equipe_buteur = ''
        ranking = 0
        for rank in podium:
            ranking += 1
            compte_rendu_saison.write(str(ranking)+'. ')
            for joueur in rank[0]:
                nom, equipe = joueur.split(',')
                if (equipe != equipe_buteur) & (equipe_buteur != ''):
                    compte_rendu_saison.write(' ('+data_saison[equipe_buteur]+'), ')
                elif equipe_buteur != '':
                    compte_rendu_saison.write(', ')
                equipe_buteur = equipe
                compte_rendu_saison.write(nom)
            compte_rendu_saison.write(' ('+data_saison[equipe_buteur]+')')
            compte_rendu_saison.write(', '+str(rank[1])+' buts inscrits\n')
            equipe_buteur = ''
         
    compte_rendu_saison.close()
    return
