import random as rnd

nb_players = int(input('Number of players: '))
median_strenght_og = int(input('Mean strength of players: '))
variance = float(input('Variance of the distribution (1.0-5.0): '))

median_strength = median_strenght_og

res = []

for i in range(nb_players-1):
    res.append(round(rnd.normalvariate(median_strength,variance)))
    median_strength = ((nb_players*median_strenght_og)-sum(res))/(nb_players-(i+1))

res.append(round(nb_players*median_strenght_og-sum(res)))
print(res)