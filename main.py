from Fonction import *
SOURCE= 0
fichier=choisir_Test()
capacities = lecture_flot(fichier)
cost_matrix = calculer_matrice_couts(capacities)
table_bellman, predecesseurs = bellman(capacities, cost_matrix, SOURCE)

afficher_matrice_capacites(capacities)
afficher_matrice_couts(cost_matrix)
afficher_table_bellman(table_bellman, predecesseurs)
