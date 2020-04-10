# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 02:11:25 2020

Moteur de match de foot

@author: alexa
"""
import random as rnd
import math
from copy import deepcopy


### NOM DES EQUIPES A CHARGER

# replace the argument list with a dictionary containinbg the parameters

def match_foot(metadata_dom, metadata_ext, arguments = {}):
    """
    Génère un match de foot
    Prend en entrée:
        - les données de l'équipe à domicile
        - les données de l'équipe à l'extérieur
        - est-ce que les prolongations sont autorisées
        - si il y a prolongations, y a-t-il un match aller à prendre en compte
        - si il y a un match aller à prendre en compte, y a-t-il avantage aux
        buts marqués à l'extérieur
        - les tirs aux buts sont-ils autorisés
        - le match se déroule-t-il sur terrain neutre
    En sortie il renvoie un tuple contenant:
        - le nombre de buts inscrits par l'équipe à domicile
        - le nombre de buts inscrits par l'équipe à l'extérieur
        - le détails des buts inscrits par l'équipe jouant à domicile
        - le détails des buts inscrits par l'équipe jouant à l'extérieur
        - le résultat des tirs aux buts
        - le détail de la séance des tirs aux buts
    """
    params = { 'prolongations' : False,
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
    
    for k in arguments:
        params[k] = arguments[k]
        
        
    if params['terrain_neutre']:
        params['bonus_dom'] = 1.000
    
    
    
    
    ### LECTURE DES FICHIERS AYANT LES INFOS DES DEUX EQUIPES
    
    
    metadata_dom_copy = deepcopy(metadata_dom)
    metadata_ext_copy = deepcopy(metadata_ext)
    h=['','','','','']
    a=['','','','','']
    
    joueurs_h = [[],
                 [],
                 [],
                 []
                 ]
    joueurs_a = [[],
                 [],
                 [],
                 []
    ]

    
    
    ### EQUIPE DOMICILE
    
    
    metadata_dom_copy.reverse()
    h[0],_,_ = metadata_dom_copy.pop().split(';')
    nb_df,nb_mil,nb_att,_ = metadata_dom_copy.pop().split(';')
    formation_h = [1,int(nb_df),int(nb_mil),int(nb_att)]
    metadata_dom_copy.reverse()
    
    niv_joueurs_h_tmp = [{},{},{},{}]
    pen_joueurs_h_tmp = [{},{},{},{}]
    poids_joueurs_h = [{},{},{},{}]
    tireurs_pen_h = []
    for l in metadata_dom_copy:
        nom, poste, niveau, tireur_peno,_ = l.split(';')
        if '/' in poste:
            postes_possibles = poste.split('/')
        else:
            postes_possibles = poste
        if 'Gardien' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Gardien") == 0 else 0.8
            poids_joueurs_h[0][nom] = int(niveau) * modifier
            niv_joueurs_h_tmp[0][nom] = niveau
            pen_joueurs_h_tmp[0][nom] = (tireur_peno == '1')
        if 'Defenseur' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Defenseur") == 0 else 0.8
            poids_joueurs_h[1][nom] = int(niveau) * modifier
            niv_joueurs_h_tmp[1][nom] = niveau
            pen_joueurs_h_tmp[1][nom] = (tireur_peno == '1')
        if 'Milieu' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Milieu") == 0 else 0.8
            poids_joueurs_h[2][nom] = int(niveau) * modifier
            niv_joueurs_h_tmp[2][nom] = niveau
            pen_joueurs_h_tmp[2][nom] = (tireur_peno == '1')
        if 'Attaquant' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Attaquant") == 0 else 0.8
            poids_joueurs_h[3][nom] = int(niveau) * modifier
            niv_joueurs_h_tmp[3][nom] = niveau
            pen_joueurs_h_tmp[3][nom] = (tireur_peno == '1')
    for p in poids_joueurs_h:
        value = round(0.8*min(p.values()))
        for i in p:
            p[i] = p[i]-value
    force_joueurs = [[],[],[],[]]
    bon_choix = False
    while not bon_choix:
        joueur_choisi = rnd.choices(list(niv_joueurs_h_tmp[0].keys()),
                                    weights=list(poids_joueurs_h[0].values()), k=1)[0]
        bon_choix = True
        for ij in range(len(poids_joueurs_h)):
            if ((joueur_choisi in poids_joueurs_h[ij]) &
                (len(poids_joueurs_h[ij])==formation_h[ij]) & (ij > 0)):
                bon_choix = False
    joueurs_h[0].append(joueur_choisi)
    h[1] = int(niv_joueurs_h_tmp[0][joueur_choisi])
    if pen_joueurs_h_tmp[0][joueur_choisi]:
        tireurs_pen_h.append(joueur_choisi)
    for d in poids_joueurs_h:
        d.pop(joueur_choisi, None)
    for d in niv_joueurs_h_tmp:
        d.pop(joueur_choisi, None)
    for j in range(0,int(nb_df)):
        bon_choix = False
        while not bon_choix:
            joueur_choisi = rnd.choices(list(niv_joueurs_h_tmp[1].keys()),
                                    weights=list(poids_joueurs_h[1].values()), k=1)[0]
            bon_choix = True
            for ij in range(len(poids_joueurs_h)):
                if ((joueur_choisi in poids_joueurs_h[ij]) &
                    (len(poids_joueurs_h[ij])==formation_h[ij]) & (ij > 1)):
                    bon_choix = False
        joueurs_h[1].append(joueur_choisi)
        force_joueurs[1].append(int(niv_joueurs_h_tmp[1][joueur_choisi]))
        if pen_joueurs_h_tmp[1][joueur_choisi]:
            tireurs_pen_h.append(joueur_choisi)
        for d in poids_joueurs_h:
            d.pop(joueur_choisi, None)
        for d in niv_joueurs_h_tmp:
            d.pop(joueur_choisi, None)
    for j in range(0,int(nb_mil)):
        bon_choix = False
        while not bon_choix:
            joueur_choisi = rnd.choices(list(niv_joueurs_h_tmp[2].keys()),
                                    weights=list(poids_joueurs_h[2].values()), k=1)[0]
            bon_choix = True
            for ij in range(len(poids_joueurs_h)):
                if ((joueur_choisi in poids_joueurs_h[ij]) &
                    (len(poids_joueurs_h[ij])==formation_h[ij]) & (ij > 2)):
                    bon_choix = False
        joueurs_h[2].append(joueur_choisi)
        force_joueurs[2].append(int(niv_joueurs_h_tmp[2][joueur_choisi]))
        if pen_joueurs_h_tmp[2][joueur_choisi]:
            tireurs_pen_h.append(joueur_choisi)
        for d in poids_joueurs_h:
            d.pop(joueur_choisi, None)
        for d in niv_joueurs_h_tmp:
            d.pop(joueur_choisi, None)
    for j in range(0,int(nb_att)):
        joueur_choisi = rnd.choices(list(niv_joueurs_h_tmp[3].keys()),
                                weights=list(poids_joueurs_h[3].values()), k=1)[0]
        joueurs_h[3].append(joueur_choisi)
        force_joueurs[3].append(int(niv_joueurs_h_tmp[3][joueur_choisi]))
        if pen_joueurs_h_tmp[3][joueur_choisi]:
            tireurs_pen_h.append(joueur_choisi)
        for d in poids_joueurs_h:
            d.pop(joueur_choisi, None)
        for d in niv_joueurs_h_tmp:
            d.pop(joueur_choisi, None)
    if tireurs_pen_h == []:
        tireurs_pen_h = [rnd.choice(joueurs_h[3])]
    h[2] = nb_df+'x'+str(sum(force_joueurs[1])/int(nb_df))
    h[3] = nb_mil+'x'+str(sum(force_joueurs[2])/int(nb_mil))
    h[4] = nb_att+'x'+str(sum(force_joueurs[3])/int(nb_att))
    
    
    ### EQUIPE EXTERIEURE
    
    
    metadata_ext_copy.reverse()
    a[0],_,_ = metadata_ext_copy.pop().split(';')
    nb_df,nb_mil,nb_att,_ = metadata_ext_copy.pop().split(';')
    formation_a = [1,int(nb_df),int(nb_mil),int(nb_att)]
    metadata_ext_copy.reverse()
    
    niv_joueurs_a_tmp = [{},{},{},{}]
    pen_joueurs_a_tmp = [{},{},{},{}]
    poids_joueurs_a = [{},{},{},{}]
    tireurs_pen_a = []
    for l in metadata_ext_copy:
        nom, poste, niveau, tireur_peno,_ = l.split(';')
        if '/' in poste:
            postes_possibles = poste.split('/')
        else:
            postes_possibles = poste
        if 'Gardien' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Gardien") == 0 else 0.8
            poids_joueurs_a[0][nom] = int(niveau) * modifier
            niv_joueurs_a_tmp[0][nom] = niveau
            pen_joueurs_a_tmp[0][nom] = (tireur_peno == '1')
        if 'Defenseur' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Defenseur") == 0 else 0.8
            poids_joueurs_a[1][nom] = int(niveau) * modifier
            niv_joueurs_a_tmp[1][nom] = niveau
            pen_joueurs_a_tmp[1][nom] = (tireur_peno == '1')
        if 'Milieu' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Milieu") == 0 else 0.8
            poids_joueurs_a[2][nom] = (int(niveau) * modifier)
            niv_joueurs_a_tmp[2][nom] = niveau
            pen_joueurs_a_tmp[2][nom] = (tireur_peno == '1')
        if 'Attaquant' in postes_possibles:
            modifier = 1.0 if postes_possibles.index("Attaquant") == 0 else 0.8
            poids_joueurs_a[3][nom] = (int(niveau) * modifier)
            niv_joueurs_a_tmp[3][nom] = niveau
            pen_joueurs_a_tmp[3][nom] = (tireur_peno == '1')
    for p in poids_joueurs_a:
        value =round(0.8*min(p.values()))
        for i in p:
            p[i] = p[i]-value
    force_joueurs = [[],[],[],[]]
    bon_choix = False
    while not bon_choix:
        joueur_choisi = rnd.choices(list(niv_joueurs_a_tmp[0].keys()),
                                    weights=list(poids_joueurs_a[0].values()), k=1)[0]
        bon_choix = True
        for ij in range(len(poids_joueurs_a)):
            if ((joueur_choisi in poids_joueurs_a[ij]) &
                (len(poids_joueurs_a[ij])==formation_a[ij]) & (ij > 0)):
                bon_choix = False
    joueurs_a[0].append(joueur_choisi)
    a[1] = int(niv_joueurs_a_tmp[0][joueur_choisi])
    if pen_joueurs_a_tmp[0][joueur_choisi]:
        tireurs_pen_a.append(joueur_choisi)
    for d in poids_joueurs_a:
        d.pop(joueur_choisi, None)
    for d in niv_joueurs_a_tmp:
        d.pop(joueur_choisi, None)
    for j in range(0,int(nb_df)):
        bon_choix = False
        while not bon_choix:
            joueur_choisi = rnd.choices(list(niv_joueurs_a_tmp[1].keys()),
                                    weights=list(poids_joueurs_a[1].values()), k=1)[0]
            bon_choix = True
            for ij in range(len(poids_joueurs_a)):
                if ((joueur_choisi in poids_joueurs_a[ij]) &
                    (len(poids_joueurs_a[ij])==formation_a[ij]) & (ij > 1)):
                    bon_choix = False
        joueurs_a[1].append(joueur_choisi)
        force_joueurs[1].append(int(niv_joueurs_a_tmp[1][joueur_choisi]))
        if pen_joueurs_a_tmp[1][joueur_choisi]:
            tireurs_pen_a.append(joueur_choisi)
        for d in poids_joueurs_a:
            d.pop(joueur_choisi, None)
        for d in niv_joueurs_a_tmp:
            d.pop(joueur_choisi, None)
    for j in range(0,int(nb_mil)):
        bon_choix = False
        while not bon_choix:
            joueur_choisi = rnd.choices(list(niv_joueurs_a_tmp[2].keys()),
                                    weights=list(poids_joueurs_a[2].values()), k=1)[0]
            bon_choix = True
            for ij in range(len(poids_joueurs_a)):
                if ((joueur_choisi in poids_joueurs_a[ij]) &
                    (len(poids_joueurs_a[ij])==formation_a[ij]) & (ij > 2)):
                    bon_choix = False
        joueurs_a[2].append(joueur_choisi)
        force_joueurs[2].append(int(niv_joueurs_a_tmp[2][joueur_choisi]))
        if pen_joueurs_a_tmp[2][joueur_choisi]:
            tireurs_pen_a.append(joueur_choisi)
        for d in poids_joueurs_a:
            d.pop(joueur_choisi, None)
        for d in niv_joueurs_a_tmp:
            d.pop(joueur_choisi, None)
    for j in range(0,int(nb_att)):
        joueur_choisi = rnd.choices(list(niv_joueurs_a_tmp[3].keys()),
                                weights=list(poids_joueurs_a[3].values()), k=1)[0]
        joueurs_a[3].append(joueur_choisi)
        force_joueurs[3].append(int(niv_joueurs_a_tmp[3][joueur_choisi]))
        if pen_joueurs_a_tmp[3][joueur_choisi]:
            tireurs_pen_a.append(joueur_choisi)
        for d in poids_joueurs_a:
            d.pop(joueur_choisi, None)
        for d in niv_joueurs_a_tmp:
            d.pop(joueur_choisi, None)
    if tireurs_pen_a == []:
        tireurs_pen_a = [rnd.choice(joueurs_a[3])]
    a[2] = nb_df+'x'+str(sum(force_joueurs[1])/int(nb_df))
    a[3] = nb_mil+'x'+str(sum(force_joueurs[2])/int(nb_mil))
    a[4] = nb_att+'x'+str(sum(force_joueurs[3])/int(nb_att))
    
    
    ### STATS DES EQUIPES
    statistiques_h = { 'niveau_gb' : float(h[1]),
                       'niveau_df' : float(h[2].split('x')[1]),
                       'nb_df' : int(h[2].split('x')[0]),
                       'niveau_mil' : float(h[3].split('x')[1]),
                       'nb_mil' : int(h[3].split('x')[0]),
                       'niveau_att' : float(h[4].split('x')[1]),
                       'nb_att' : int(h[4].split('x')[0])
    }
    
    statistiques_a = { 'niveau_gb' : float(a[1]),
                       'niveau_df' : float(a[2].split('x')[1]),
                       'nb_df' : int(a[2].split('x')[0]),
                       'niveau_mil' : float(a[3].split('x')[1]),
                       'nb_mil' : int(a[3].split('x')[0]),
                       'niveau_att' : float(a[4].split('x')[1]),
                       'nb_att' : int(a[4].split('x')[0])
    }
    
    
    
    ### DEFINITION DE STATISTIQUES DERIVEES
    
    ### TOUT D'ABORD LA BATAILLE DU MILIEU
    statistiques_h['force_milieu'] = params['bonus_dom']*(statistiques_h['niveau_mil'] +
                  ((statistiques_h['nb_mil']/(statistiques_h['nb_mil']+statistiques_a['nb_mil']))*100))/2
    statistiques_a['force_milieu'] = (statistiques_a['niveau_mil'] +
                  ((statistiques_a['nb_mil']/(statistiques_h['nb_mil']+statistiques_a['nb_mil']))*100))/2
    
    repartition_m = ((statistiques_h['force_milieu']/(statistiques_h['force_milieu']+statistiques_a['force_milieu'])+0.5)**6)/2
    
    
    
    ### ENSUITE LA FORCE D'ATTAQUE PLACEE DES DEUX EQUIPES
    force_att_brute_h = (2/3)*statistiques_h['niveau_att'] + (1/3)*statistiques_h['niveau_mil']
    force_att_nb_h = ((statistiques_h['nb_att']+(statistiques_h['nb_mil']/2)) /
                      (statistiques_h['nb_att']+statistiques_a['nb_df']+(statistiques_h['nb_mil']/2)+(statistiques_a['nb_mil']/2)))
    
    statistiques_h['force_att_domin'] = params['bonus_dom']*(force_att_brute_h+(100*force_att_nb_h))/2
    
    force_att_brute_a = (2/3)*statistiques_a['niveau_att'] + (1/3)*statistiques_a['niveau_mil']
    force_att_nb_a = ((statistiques_a['nb_att']+(statistiques_a['nb_mil']/2)) /
                      (statistiques_a['nb_att']+statistiques_h['nb_df']+(statistiques_h['nb_mil']/2)+(statistiques_a['nb_mil']/2)))
    
    statistiques_a['force_att_domin'] = (force_att_brute_a+(100*force_att_nb_a))/2
    
    
    
    ### LA FORCE DE CONTRE DE CHAQUE EQUIPE
    force_att_brute_h = (3/4)*statistiques_h['niveau_att'] + (1/4)*statistiques_h['niveau_mil']
    force_att_nb_h = (((statistiques_h['nb_att']/2)+(statistiques_h['nb_mil']/3)) /
                      ((statistiques_h['nb_att']/2)+(statistiques_a['nb_df']/2)+(statistiques_h['nb_mil']/3)+(statistiques_a['nb_mil']/3)))
    
    statistiques_h['force_att_contre'] = params['bonus_dom']*(force_att_brute_h+(100*force_att_nb_h))/2
    
    force_att_brute_a = (3/4)*statistiques_a['niveau_att'] + (1/4)*statistiques_a['niveau_mil']
    force_att_nb_a = (((statistiques_a['nb_att']/2)+(statistiques_a['nb_mil']/3)) /
                      ((statistiques_a['nb_att']/2)+(statistiques_h['nb_df']/2)+(statistiques_h['nb_mil']/3)+(statistiques_a['nb_mil']/3)))
    
    statistiques_a['force_att_contre'] = (force_att_brute_a+(100*force_att_nb_a))/2
    
    
    
    ### FORCE DE DEFENSE D'ATTAQUE PLACEES
    force_df_brute_h = (2/3)*statistiques_h['niveau_df'] + (1/3)*statistiques_h['niveau_mil']
    force_df_nb_h = ((statistiques_h['nb_df']+(statistiques_h['nb_mil']/2)) /
                     (statistiques_h['nb_df']+statistiques_a['nb_att']+(statistiques_h['nb_mil']/2)+(statistiques_a['nb_mil']/2)))
    
    statistiques_h['force_df_domin'] = params['bonus_dom']*(force_df_brute_h+(100*force_df_nb_h))/2
    
    force_df_brute_a = (2/3)*statistiques_a['niveau_df'] + (1/3)*statistiques_a['niveau_mil']
    force_df_nb_a = ((statistiques_a['nb_df']+(statistiques_a['nb_mil']/2)) /
                     (statistiques_a['nb_df']+statistiques_h['nb_att']+(statistiques_h['nb_mil']/2)+(statistiques_a['nb_mil']/2)))
    
    statistiques_a['force_df_domin'] = (force_df_brute_a+(100*force_df_nb_a))/2
    
    
    
    ### FORCE DE DEFENSE SUR CONTRES
    force_df_brute_h = (3/4)*statistiques_h['niveau_df'] + (1/4)*statistiques_h['niveau_mil']
    force_df_nb_h = (((statistiques_h['nb_df']/2)+(statistiques_h['nb_mil']/3)) /
                     ((statistiques_h['nb_df']/2)+(statistiques_a['nb_att']/2)+(statistiques_h['nb_mil']/3)+(statistiques_a['nb_mil']/3)))
    
    statistiques_h['force_df_contre'] = params['bonus_dom']*(force_df_brute_h+(100*force_df_nb_h))/2
    
    force_df_brute_a = (3/4)*statistiques_a['niveau_df'] + (1/4)*statistiques_a['niveau_mil']
    force_df_nb_a = (((statistiques_a['nb_df']/2)+(statistiques_a['nb_mil']/3)) /
                     ((statistiques_a['nb_df']/2)+(statistiques_h['nb_att']/2)+(statistiques_h['nb_mil']/3)+(statistiques_a['nb_mil']/3)))
    
    statistiques_a['force_df_contre'] = (force_df_brute_a+(100*force_df_nb_a))/2
    
    
    
    ### LES FORCES DE TIRS DES DEUX EQUIPES
    force_tir_domin_h = statistiques_h['nb_att']/(statistiques_h['nb_att']+statistiques_a['nb_df']+1)
    force_tir_contre_h = statistiques_h['nb_att']/(statistiques_h['nb_att']+(statistiques_a['nb_df']/2)+1)
    
    statistiques_h['force_tir_domin'] = params['bonus_dom']*(statistiques_h['niveau_att']+(100*force_tir_domin_h))/2
    statistiques_h['force_tir_contre'] = params['bonus_dom']*(statistiques_h['niveau_att']+(100*force_tir_contre_h))/2
    
    force_tir_domin_a = statistiques_a['nb_att']/(statistiques_a['nb_att']+statistiques_h['nb_df']+1)
    force_tir_contre_a = statistiques_a['nb_att']/(statistiques_a['nb_att']+(statistiques_h['nb_df']/2)+1)
    
    statistiques_a['force_tir_domin'] = (statistiques_a['niveau_att']+(100*force_tir_domin_a))/2
    statistiques_a['force_tir_contre'] = (statistiques_a['niveau_att']+(100*force_tir_contre_a))/2
    
    
    
    ### LES FORCES DE GARDIEN DES DEUX EQUIPES
    
    ### D'ABORD CONTRES DES ATATQUES PLACESS
    force_gb_brute_h = (2/3)*statistiques_h['niveau_gb'] + (1/3)*statistiques_h['niveau_df']
    force_gb_nb_h = (1+statistiques_h['nb_df'])/(1+statistiques_h['nb_df']+statistiques_a['nb_att'])
    
    statistiques_h['force_gb_domin'] = params['bonus_dom']*(force_gb_brute_h+(100*force_df_nb_h))/2
    
    force_gb_brute_a = (2/3)*statistiques_a['niveau_gb'] + (1/3)*statistiques_a['niveau_df']
    force_gb_nb_a = (1+statistiques_a['nb_df'])/(1+statistiques_a['nb_df']+statistiques_h['nb_att'])
    
    statistiques_a['force_gb_domin'] = (force_gb_brute_a+(100*force_df_nb_a))/2
    
    ### ENSUITE FACE A DES CONTRES
    force_gb_brute_h = (3/4)*statistiques_h['niveau_gb'] + (1/4)*statistiques_h['niveau_df']
    force_gb_nb_h = (1+(statistiques_h['nb_df']/2))/(1+(statistiques_h['nb_df']/2)+statistiques_a['nb_att'])
    
    statistiques_h['force_gb_contre'] = params['bonus_dom']*(force_gb_brute_h+(100*force_gb_nb_h))/2
    
    force_gb_brute_a = (3/4)*statistiques_a['niveau_gb'] + (1/4)*statistiques_a['niveau_df']
    force_gb_nb_a = (1+(statistiques_a['nb_df']/2))/(1+(statistiques_a['nb_df']/2)+statistiques_h['nb_att'])
    
    statistiques_a['force_gb_contre'] = (force_gb_brute_a+(100*force_gb_nb_a))/2
    
    
    
    ### CE QUI DONNE DES PROBABILITES DE MARQUER ET D'OBTENIR UN CERTAIN NOMBRE DE TIRS
    statistiques_h['nb_tir_domin'] = max(0.1,1 + math.log(statistiques_h['force_att_domin'] /
                  (statistiques_h['force_att_domin']+statistiques_a['force_df_domin'])))
    statistiques_h['chance_but_domin'] = (statistiques_h['force_tir_domin'] /
                  (statistiques_h['force_tir_domin']+statistiques_a['force_gb_domin']))
    statistiques_h['nb_tir_contre'] = max(0.1,1 + math.log(statistiques_h['force_att_contre'] /
                  (statistiques_h['force_att_contre']+statistiques_a['force_df_contre'])))
    statistiques_h['chance_but_contre'] = (statistiques_h['force_tir_contre'] /
                  (statistiques_h['force_tir_contre']+statistiques_a['force_gb_contre']))
    
    statistiques_a['nb_tir_domin'] = max(0.1,1 + math.log(statistiques_a['force_att_domin'] /
                  (statistiques_a['force_att_domin']+statistiques_h['force_df_domin'])))
    statistiques_a['chance_but_domin'] = (statistiques_a['force_tir_domin'] /
                  (statistiques_a['force_tir_domin']+statistiques_h['force_gb_domin']))
    statistiques_a['nb_tir_contre'] = max(0.1,1 + math.log(statistiques_a['force_att_contre'] /
                  (statistiques_a['force_att_contre']+statistiques_h['force_df_contre'])))
    statistiques_a['chance_but_contre'] = (statistiques_a['force_tir_contre'] /
                  (statistiques_a['force_tir_contre']+statistiques_h['force_gb_contre']))
    
    
    
    
    ### DEFINITION DU SCORE ET DU TEMPS
    score = {'h': 0, 'a': 0}
    
    temps=[range(0,50,5),range(0,50,5)]
    
    
    
    ### ON VA AUSSI ENREGISTRER QUELQUES STATS SUR LE MATCH
    statistiques_h['nb tirs'] = 0
    statistiques_h['domination'] = 0
    statistiques_h['buteurs'] = []
    
    statistiques_a['nb tirs'] = 0
    statistiques_a['domination'] = 0
    statistiques_a['buteurs'] = []
    
    mi_temps = 0
    
    for half in temps:
        for time in half:
            who_dominates = rnd.random()
            dominator = 'h'
            counter = 'a'
            dico_domin = statistiques_h
            dico_contre = statistiques_a
            joueurs_domin = joueurs_h
            joueurs_contre = joueurs_a
            pen_domin = tireurs_pen_h
            pen_contre = tireurs_pen_a
            if who_dominates > repartition_m:
                dominator = 'a'
                counter = 'h'
                dico_domin = statistiques_a
                dico_contre = statistiques_h
                joueurs_domin = joueurs_a
                joueurs_contre = joueurs_h
                pen_domin = tireurs_pen_a
                pen_contre = tireurs_pen_h
            dico_domin['domination'] += 1
            nb_tir_domin = round(abs(rnd.random() - 0.5)*dico_domin['nb_tir_domin']*10)
            dico_domin['nb tirs'] += nb_tir_domin
            nb_tir_contre = round(abs(rnd.random() - 0.5)*dico_contre['nb_tir_contre']*5)
            dico_contre['nb tirs'] += nb_tir_contre
            minutes = []
            for m in range(1,6):
                minutes.append(m+time+mi_temps)
            for i in range(0,nb_tir_domin):
                is_but = rnd.random() <= dico_domin['chance_but_domin']**params['penalty_term']
                if is_but:
                    score[dominator]+=1
                    csc = rnd.random() <= params['proba_csc']
                    marker = ''
                    poste_buteur = rnd.random()
                    if csc:
                        marker = ' c.s.c.'
                        if poste_buteur <= 1/11:
                            buteur = joueurs_contre[0][0]
                        elif (poste_buteur > 1/11) & (poste_buteur <= (1+dico_contre['nb_df'])/11):
                            buteur = rnd.choice(joueurs_contre[1])
                        elif (poste_buteur > (1+dico_contre['nb_df'])/11) & (poste_buteur > (1+dico_contre['nb_df']+
                            dico_contre['nb_att'])/11):
                            buteur = rnd.choice(joueurs_contre[2])
                        else:
                            buteur = rnd.choice(joueurs_contre[3])
                    else:
                        pen = rnd.random() <= params['pen_threshold']
                        if pen:
                            marker = ' s.p.'
                            buteur = rnd.choice(pen_domin)
                        else:
                            but_att = (1.5*statistiques_h['nb_att']/5)
                            if poste_buteur < but_att:
                                buteur = rnd.choice(joueurs_domin[3])
                            elif poste_buteur >= 1-((1-but_att)/3):
                                buteur = rnd.choice(joueurs_domin[1])
                            else:
                                buteur = rnd.choice(joueurs_domin[2])
                    chosen_minute = rnd.choice(minutes)
                    minutes.remove(chosen_minute)
                    if minutes == []:
                        for m in range(1,6):
                                minutes.append(m+time+mi_temps)
                    if (mi_temps == 0 and chosen_minute > 45) or (mi_temps == 45 and chosen_minute > 90):
                        dico_domin['buteurs'].append(buteur+', '+str(mi_temps+45)+'+'+
                                  str(chosen_minute-(mi_temps+45))+marker)
                    else:
                        dico_domin['buteurs'].append(buteur+', '+str(chosen_minute)+marker)
            for j in range(0,nb_tir_contre):
                is_but = rnd.random() <= dico_contre['chance_but_contre']**params['penalty_term']
                if is_but:
                    score[counter]+=1
                    csc = rnd.random() <= params['proba_csc']
                    marker = ''
                    poste_buteur = rnd.random()
                    if csc:
                        marker = ' c.s.c.'
                        poste_buteur = rnd.random()
                        if poste_buteur <= 1/(dico_domin['nb_df']+(dico_domin['nb_mil']/2)):
                            buteur = joueurs_domin[0][0]
                        elif poste_buteur > (dico_domin['nb_mil']/2)/(dico_domin['nb_df']+(dico_domin['nb_mil']/2)):
                            buteur = rnd.choice(joueurs_domin[2])
                        else:
                            buteur = rnd.choice(joueurs_domin[1])
                    else:
                        pen = rnd.random() <= params['pen_threshold']
                        if pen:
                            marker = ' s.p.'
                            buteur = rnd.choice(pen_contre)
                        else:
                            but_att = 2*statistiques_h['nb_att']/5
                            if poste_buteur < but_att:
                                buteur = rnd.choice(joueurs_contre[3])
                            elif poste_buteur >= 1-((1-but_att)/6):
                                buteur = rnd.choice(joueurs_contre[1])
                            else:
                                buteur = rnd.choice(joueurs_contre[2])
                    chosen_minute = rnd.choice(minutes)
                    minutes.remove(chosen_minute)
                    if minutes == []:
                        for m in range(1,6):
                                minutes.append(m+time+mi_temps)
                    if (mi_temps == 0 and chosen_minute > 45) or (mi_temps == 45 and chosen_minute > 90):
                        dico_contre['buteurs'].append(buteur+', '+str(mi_temps+45)+'+'+str(chosen_minute-(mi_temps+45))+marker)
                    else:
                        dico_contre['buteurs'].append(buteur+', '+str(chosen_minute)+marker)
        mi_temps = 45
        
    a_p = False
    if params['prolongations']:
        if (((not params['buts_ext_2']) & (params['agg_dom']+score['h'] == params['agg_ext']+score['a'])) |
        ((params['buts_ext_2']) & (params['agg_dom'] == score['a'])
        & (params['agg_ext'] == score['h']))):
            a_p = True
            temps_prol=[range(0,15,5),range(0,15,5)]
            prol_mi_temps = 0
            for half in temps_prol:
                for time in half:
                    who_dominates = rnd.random()
                    dominator = 'h'
                    counter = 'a'
                    dico_domin = statistiques_h
                    dico_contre = statistiques_a
                    joueurs_domin = joueurs_h
                    joueurs_contre = joueurs_a
                    pen_domin = tireurs_pen_h
                    pen_contre = tireurs_pen_a
                    if who_dominates > repartition_m:
                        dominator = 'a'
                        counter = 'h'
                        dico_domin = statistiques_a
                        dico_contre = statistiques_h
                        joueurs_domin = joueurs_a
                        joueurs_contre = joueurs_h
                        pen_domin = tireurs_pen_a
                        pen_contre = tireurs_pen_h
                    dico_domin['domination'] += 1
                    nb_tir_domin = round(abs(rnd.random() - 0.5)*dico_domin['nb_tir_domin']*10)
                    dico_domin['nb tirs'] += nb_tir_domin
                    nb_tir_contre = round(abs(rnd.random() - 0.5)*dico_contre['nb_tir_contre']*5)
                    dico_contre['nb tirs'] += nb_tir_contre
                    minutes = []
                    for m in range(1,6):
                        minutes.append(m+time+90+prol_mi_temps)
                    for i in range(0,nb_tir_domin):
                        is_but = rnd.random() <= dico_domin['chance_but_domin']**params['penalty_term']
                        if is_but:
                            score[dominator]+=1
                            csc = rnd.random() <= params['proba_csc']
                            marker = ''
                            poste_buteur = rnd.random()
                            if csc:
                                marker = ' c.s.c.'
                                if poste_buteur <= 1/11:
                                    buteur = joueurs_contre[0][0]
                                elif (poste_buteur > 1/11) & (poste_buteur <= (1+dico_contre['nb_df'])/11):
                                    buteur = rnd.choice(joueurs_contre[1])
                                elif (poste_buteur > (1+dico_contre['nb_df'])/11) & (poste_buteur > (1+dico_contre['nb_df']+
                                    dico_contre['nb_att'])/11):
                                    buteur = rnd.choice(joueurs_contre[2])
                                else:
                                    buteur = rnd.choice(joueurs_contre[3])
                            else:
                                pen = rnd.random() <= params['pen_threshold']
                                if pen:
                                    marker = ' s.p.'
                                    buteur = rnd.choice(pen_domin)
                                else:
                                    but_att = (1.5*statistiques_h['nb_att']/5)
                                    if poste_buteur < but_att:
                                        buteur = rnd.choice(joueurs_domin[3])
                                    elif poste_buteur >= 1-((1-but_att)/3):
                                        buteur = rnd.choice(joueurs_domin[1])
                                    else:
                                        buteur = rnd.choice(joueurs_domin[2])
                            chosen_minute = rnd.choice(minutes)
                            minutes.remove(chosen_minute)
                            if minutes == []:
                                for m in range(1,6):
                                        minutes.append(m+time+prol_mi_temps+90)
                            dico_domin['buteurs'].append(buteur+', '+str(chosen_minute)+marker)
                    for j in range(0,nb_tir_contre):
                        is_but = rnd.random() <= dico_contre['chance_but_contre']**params['penalty_term']
                        if is_but:
                            score[counter]+=1
                            csc = rnd.random() <= params['proba_csc']
                            marker = ''
                            poste_buteur = rnd.random()
                            if csc:
                                marker = ' c.s.c.'
                                poste_buteur = rnd.random()
                                if poste_buteur <= 1/(dico_domin['nb_df']+(dico_domin['nb_mil']/2)):
                                    buteur = joueurs_domin[0][0]
                                elif poste_buteur > (dico_domin['nb_mil']/2)/(dico_domin['nb_df']+(dico_domin['nb_mil']/2)):
                                    buteur = rnd.choice(joueurs_domin[2])
                                else:
                                    buteur = rnd.choice(joueurs_domin[1])
                            else:
                                pen = rnd.random() <= params['pen_threshold']
                                if pen:
                                    marker = ' s.p.'
                                    buteur = rnd.choice(pen_contre)
                                else:
                                    but_att = 2*statistiques_h['nb_att']/5
                                    if poste_buteur < but_att:
                                        buteur = rnd.choice(joueurs_contre[3])
                                    elif poste_buteur >= 1-((1-but_att)/6):
                                        buteur = rnd.choice(joueurs_contre[1])
                                    else:
                                        buteur = rnd.choice(joueurs_contre[2])
                            chosen_minute = rnd.choice(minutes)
                            minutes.remove(chosen_minute)
                            if minutes == []:
                                for m in range(1,6):
                                        minutes.append(m+time+prol_mi_temps+90)
                            dico_contre['buteurs'].append(buteur+', '+str(chosen_minute)+marker)
                prol_mi_temps = 15
    
    score_tabs = {'h' : 0,
                  'a': 0}
    res_tireurs = {'h' : [],
                   'a' : []}
    if params['tab']:
        if (((not params['buts_ext_2']) & (params['agg_dom']+score['h'] == params['agg_ext']+score['a'])) |
        ((params['buts_ext_2']) & (params['agg_dom'] == score['a'])
        & (params['agg_ext'] == score['h']))):
            
            premiere_equipe = rnd.choice(['h', 'a'])
            equipe_actuelle = premiere_equipe
            equipe_attendant = 'h' if (equipe_actuelle == 'a') else 'a'
            nb_tirs = 0
            victoire = False
            
            tireurs = { 'h' : joueurs_h[1]+joueurs_h[2]+joueurs_h[3],
                       'a' : joueurs_a[1]+joueurs_a[2]+joueurs_a[3]}
            
            rnd.shuffle(tireurs['h'])
            rnd.shuffle(tireurs['a'])
            tireurs['h'] = tireurs['h']+joueurs_h[0]
            tireurs['a'] = tireurs['a']+joueurs_a[0]
            
            while victoire == False:
                if premiere_equipe == equipe_actuelle:
                    nb_tirs += 1
                but = rnd.random() <= params['proba_but_peno']
                if but:
                    score_tabs[equipe_actuelle] += 1
                res_tireurs[equipe_actuelle].append([tireurs[equipe_actuelle][(nb_tirs-1)%11], but])
                if ((nb_tirs == 3) & (premiere_equipe != equipe_actuelle) &
                    (abs(score_tabs[equipe_actuelle]-score_tabs[equipe_attendant]) == 3)):
                    victoire = True
                elif ((nb_tirs == 4) & (premiere_equipe == equipe_actuelle) &
                      ((score_tabs[equipe_actuelle]-score_tabs[equipe_attendant] > 2) |
                              (score_tabs[equipe_attendant]-score_tabs[equipe_actuelle] >= 2))):
                    victoire = True
                elif ((nb_tirs == 4) & (premiere_equipe != equipe_actuelle) &
                      (abs(score_tabs[equipe_actuelle]-score_tabs[equipe_attendant]) > 1)):
                    victoire = True
                elif ((nb_tirs == 5) & (premiere_equipe == equipe_actuelle) &
                      ((score_tabs[equipe_actuelle]-score_tabs[equipe_attendant] > 1) |
                              (score_tabs[equipe_attendant]-score_tabs[equipe_actuelle] >= 1))):
                    victoire = True
                elif ((nb_tirs >= 5) & (premiere_equipe != equipe_actuelle) &
                      (score_tabs[equipe_actuelle] != score_tabs[equipe_attendant])):
                    victoire = True
                equipe_actuelle, equipe_attendant = equipe_attendant, equipe_actuelle
    return(score['h'],score['a'],statistiques_h['buteurs'],statistiques_a['buteurs'],
           a_p, score_tabs, res_tireurs)