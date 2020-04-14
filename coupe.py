# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:00:25 2020

Core program file

Generates cups.

Cups are a form of competition where teams play each other until only one remains - this team is the winner.
Unlike a league, in a cup teams don't all play against each other.
The typical format of a cup is the knockout format. The knockout format requires to have precisely 2^n teams qualified
for the cup. Teams will be paired in matchs (there will be 2^(n-1) matches) and the winner of each matchs advances
onto the next round, until only two teams remain. These two teams play each other in the final, with the winner of
the final winning the whole competition.
Note that matches can be played over one or two legs.
One leg: only one match, on neutral ground or not, takes place between two teams and the winner advances.
Two legs: two matches are disputed between the two teams (each team hosting one match), with the team having the best
aggregated score winning. Aggregated score is calculated by summing the number of teams scored by each teams on the two
matches.
In the two legs format a tie breaker often used are away goals: if both teams have scored tjhe same number of goals over
the two matches, they are tied. In this case, the team having scored the most goals when playing away from home is
declared winner.
See also: Coupe de France for a one leg format, UEFA Champions League for a two legs format

Now, the number of qualified teams for a particular competition is more often than not not a power of 2, for various
reasons. In this case, it becomes necessary to whittle down the field by playing preliminary rounds between some teams
until the number of teams is a power of 2 and the aforementioned knockout method can be used. It becomes however
necessary to keep track of the teams which are dispensed of these prelimnary rounds.
See also: preliminary rounds of the UEFA Europa League, Coupe de la Ligue

To solve the aforementioned issue, a group stage can also be used. But most of the time, a group stage is used to avoid
having competitions where teams losing in the first round only play one or two matches. The idea behind a group stage
is to group teams in a small number of groups, which are in effect mini-leagues where every team play each other
once or twice. Then a table is made for each group ranking each team on the basis of their result in the group. The best
teams advance onto the next round (the number of teams in a group and the number of teams qualifying in a group vary
with the competition).
See also: FIFA World Cup


Additionally pots may be used when pairing the teams together. If no pots are used, then it means there are no
restriction in the draw - a team can play any other team (note: not quite true but good enough). But it means that
the best teams can play each other very early in the cup, which usually results in a loss of money (big teams tend to
have a lot of supporters so if their team is eliminated early they won't watch the competition etc). Conversely it means
a smaller team can go far if it is lucky enough to only meet smaller teams (again smaller teams have few fans so this
is not good financially). So pots are used to classify teams according to their strengths: teams in pot 1 are the
strongest, teams in pot 2 are OK, teams in pot 3 are weak etc. Then when the draw is made two teams of the same pot
can't play each other. Note that if matches are drawn, only two pots are necessary (top teams v weaker teams). For a
group stage more pots are used.
See also: UEFA Champions League where a pot system is used to drawn the teams in the group stage, then a pot system
based on results in the group stage is used to draw matches in the round of 16.



Tie-solving: as mentioned previously, if two matches take place for each tie, goals scored away can be used as a
tie-breaker. Otherwise, if two teams are tied nowadays extra-time and a penalty shootout are used to determine one
winner (a penalty shootout always has one winner).
In older times, extra time was used but there were no peanlty shootouts. If a match was still tied after extra time,
a replay would take place: the match would be replayed (at a neutral venue or not). Usually if the two teams were still
tied after a couple replays a coin toss was used.
See: Euro 1968 (no replays but a coin toss used in the semi final); the English FA Cup (who still uses replays but
replaced coin toss with a penalty shootout)

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


    """
    Simulates a groupe stage of a cup.

    See the above documentation to know what is a group stage.

    Results are stored into the output folders. There is one folder per group. In each folder there is a .txt file
    containing the final group table and individual folders for each matchday containing each individual match report

    Parameters
    ----------
    nom_saison : str
                The name of the folder where the teams' data to load is located.
    resultat_saison : str
                The name of the folder where results will be stored.
    coupe_nationale : bool, optional
                This is used internally to determine flags and will have to be changed (see Issues #20 & #21).
                Basically if it is true it considers the flag to be an int and if false to be an str.
    aller_retour : bool, optional
                Determines if teams in a group play each other once or twice.
    liste_chapeaux : list of int, optional
                The list of pots to be used for the draw. Empty list = no pots, free draw. Note that pots should start
                at 1 - pot '0' is a dummy value used for some specific draws.
    nb_qualifies_poule : int, optional
                Number of teams qualifying frome ach group. Default is 2.
    nb_equipe_poule : int, optional
                Number of teams per group. Default is 4.
    pts : list of int, optional
                Number of points given for a win, a draw, and a loss, respectively.
    criterias : list of str, optional
                The tie-breaker criterias to use in case two teams are tied in point total, ranked in order of use.
                The three criterias supported are:
                diff, goal difference
                bp, number of goals scored
                conf, the result of the match(s) between the two tied teams
    flag_exist : bool, optional
                Bandaid boolean indicating if flags exist. Added because of a problem where the data loader tried to
                cast nothing in int or string. This problem should be fixed in a more elegant manner and this argument
                removed. See also Issues #20 & #21
    additional_arguments : dict
                Additional arguments to pass onto the football match simulator itself. Possible values detailed in
                match_foot documentation.

    Returns
    -------
    list of tuple of str, int, int
                It returns the list of qualified teams. Each element of the list is a tuple containing:
                - the name of the team
                - the ranking of the team in the group
                - the group in which the team was playing
    """
    
    
    
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
    compteur_poule = 65 # 65 is char 'A'. Used to name the group
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

    """
    Simulates a kncokout stage or a single round for a cup.

    See the above documentation to know what is a group stage.

    Results are stored into the output folders. There is one folder per stage. Each folder contains each individual
    match report.

    Parameters
    ----------
    nom_saison : str
                The name of the folder where the teams' data to load is located.
    resultat_saison : str
                The name of the folder where results will be stored.
    coupe_nationale : bool, optional
                This is used internally to determine flags and will have to be changed (see Issues #20 & #21).
                Basically if it is true it considers the flag to be an int and if false to be an str.
    aller_retour : bool, optional
                Determines if teams in a group play each other once or twice.
    finale_ar : bool, optional
                Determines if the final is played over one or two legs.
    liste_chapeaux : list of int, optional
                The list of pots to be used for the draw. Empty list = no pots, free draw. Note that pots should start
                at 1 - pot '0' is a dummy value used for some specific draws.
    groupes : dict of int, optional
                A bit special. If the knockout stage is supposed to take place after a groupe stage, then two teams
                coming from the same group can't play each other in the same round. This information is provided
                by thsi argument.
    un_seul_tour : bool, optional
                Should we stop after only one round of match or go all the way to the final
    flag_exist : bool, optional
                Bandaid boolean indicating if flags exist. Added because of a problem where the data loader tried to
                cast nothing in int or string. This problem should be fixed in a more elegant manner and this argument
                removed. See also Issues #20 & #21
    additional_arguments : dict
                Additional arguments to pass onto the football match simulator itself. Possible values detailed in
                match_foot documentation.
                Two arguments are used here.
                If the key 'nom tour' is present in this argument, then the round will be named with the value
                associated to the key. Used to name one-shot rounds.
                If the key 'buts_ext_2' is associated to the value 'True', then away goals are used as a tie breaker.
                See the doc at the top of this file: in case matches are played over two legs, the number of goals
                scored by the teams while playing away can be used as a tie-breaker. THIS SHOULD BE SET TO FALSE IF
                MATCHES ARE PLAYED OVER ONE LEG (or it messes up when the program tries to determine the winner of the
                tie)


    Returns
    -------
    list of str
                The list of qualified teams. If the tournament was played all the way to the final, then the winner
                is returned in a list of one element
    """
    # Defining the name of the rounds. It's incredibly rare to have more than 128 teams at once, though
    # the only importants names are for the final, semi-finals and quarter-finals - the other names could be generated
    # automatically easily. But I'm too lazy for that
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
            # see the doc, if aller_retour is false buts_ext_2 should be false too to avoid problems
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
                if aller_retour & (nb_replays == 0): # if a replay is necessary then we don't play two legs
                    add_args_aller = deepcopy(add_args)
                    # no extra time nor penalty shootouts if the two teams are tied after the first leg !!!
                    add_args_aller['prolongations'] = False
                    add_args_aller['tab'] = False
                    match_a = match_foot(data_equipe[equipe_ext],
                                         data_equipe[equipe_dom], add_args_aller)
                    compte_rendu_match(equipe_dom=equipe_ext, equipe_ext=equipe_dom,
                                       stats_saison=stats_saison, tour=tour_actuel,
                                       resultat=match_a, coupe = True, type_match='aller')
                    agg_dom = match_a[1]
                    agg_ext = match_a[0]
                # ugly, that's used for the match report. That could be more elegant
                marqueur_retour = ''
                if aller_retour:
                    marqueur_retour = 'retour'
                else:
                    marqueur_retour = 'coupe'
                args_match = add_args
                # let's not forget t*o update the score with the score of the first leg
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
                victoire = (vainqueur != 'Personne') # yes, no coin toss here but unlimited replays until there's a winner
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
        