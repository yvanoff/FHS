# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 05:09:29 2020

A round-robin generator found at: https://gist.github.com/Makistos/7192777

@author: Makistos
"""

#!/usr/bin/python

def create_schedule(list_, retour):
    """ Create a schedule for the teams in the list and return it"""
    s = []

    if len(list_) % 2 == 1: list_ = list_ + ["BYE"]

    for i in range(len(list_)-1):

        mid = int(len(list_) / 2)
        l1 = list_[:mid]
        l2 = list_[mid:]
        l2.reverse()

        # Switch sides after each round
        liste_matchs = []
        if (i % 2 == 0):
            parite = True
        else:
            parite = False
        for eq1, eq2 in zip(l1,l2):
            index = l1.index(eq1)
            if index == 0:
                if parite:
                    liste_matchs.append((eq1,eq2))
                else:
                    liste_matchs.append((eq2,eq1))
            else:
                inversion = (index % 2) == 0
                if inversion:
                    liste_matchs.append((eq2,eq1))
                else:
                    liste_matchs.append((eq1,eq2))
        s.append(liste_matchs)

        list_.insert(1, list_.pop())
    
    if retour:
        s_full = s.copy()
        s_full.reverse()
        first_day = s_full.pop()
        s_full.reverse()
        s_full.append(first_day)
        for round_ in s_full:
            new_round = []
            for match in round_:
                new_round.append((match[1],match[0]))
            s.append(new_round)

    return s