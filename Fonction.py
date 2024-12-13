import random
import time
from collections import deque
import matplotlib.pyplot as plt


def choisir_Test():
    # Demande à l'utilisateur de choisir un numéro de test et retourne le chemin du fichier correspondant
    x = int(input("Entrer le numero du Test que vous voulez afficher : "))
    fichier = f"Test/Test{x}.txt"
    print(fichier)
    return fichier

def lecture_flot(chemin_fichier):
    # Lit un fichier contenant une matrice de capacités et retourne la matrice
    try:
        with open(chemin_fichier, 'r') as file:
            lines = file.readlines()
            n = int(lines[0].strip())  # Lit le nombre de noeuds
            capacity_matrix = [list(map(int, line.split())) for line in lines[1:]]  # Lit la matrice ligne par ligne
            return capacity_matrix
    except Exception as e:
        # Gère les erreurs de lecture de fichier
        print(f"Erreur de lecture du fichier {chemin_fichier} : {e}")
        return None

def afficher_matrice(matrice, titre):
    # Affiche une matrice avec un titre donné
    print(titre)
    max_len = max(len(f"{val:.2f}" if isinstance(val, float) else f"{val}") for row in matrice for val in row)  # Calcule la largeur maximale pour aligner les colonnes
    for ligne in matrice:
        print(" ".join(f"{val:>{max_len}.2f}" if isinstance(val, float) else f"{val:>{max_len}}" for val in ligne))  # Affiche chaque ligne avec un alignement
    print()

def afficher_matrice_capacites(capacity_matrix):
    # Affiche la matrice des capacités
    afficher_matrice(capacity_matrix, "Matrice des capacités :")

def afficher_matrice_couts(cost_matrix):
    # Affiche la matrice des coûts
    afficher_matrice(cost_matrix, "Matrice des coûts :")

def afficher_table_bellman(table_bellman, predecesseurs):
    # Affiche la table issue de l'algorithme de Bellman
    print("Table issue de l'algorithme de Bellman :")
    print("Noeud  Coût minimal  Prédécesseur")
    for noeud, (cout, pred) in enumerate(zip(table_bellman, predecesseurs)):
        # Affiche le noeud, le coût minimal et son prédécesseur
        print(f"{noeud:<7}{cout:<14.2f}{pred:<10}")
    print()

def calculer_matrice_couts(capacity_matrix):
    # Calcule une matrice des coûts basée sur les capacités
    n = len(capacity_matrix)
    cost_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if capacity_matrix[i][j] > 0:
                cost_matrix[i][j] = round(1 / capacity_matrix[i][j], 2)  # Coût inversement proportionnel à la capacité
            else:
                cost_matrix[i][j] = float('inf')  # Pas d'arc
    return cost_matrix

def bellman(capacity_matrix, cost_matrix, source):
    # Implémente l'algorithme de Bellman pour trouver les coûts minimaux et les prédécesseurs
    n = len(cost_matrix)
    table_bellman = [float('inf')] * n  # Initialisation des coûts à l'infini
    predecesseurs = [-1] * n  # Initialisation des prédécesseurs
    table_bellman[source] = 0

    for _ in range(n - 1):  # Relaxation des arêtes pour n-1 itérations
        for u in range(n):
            for v in range(n):
                if capacity_matrix[u][v] > 0 and table_bellman[u] + cost_matrix[u][v] < table_bellman[v]:
                    table_bellman[v] = table_bellman[u] + cost_matrix[u][v]
                    predecesseurs[v] = u

    # Vérifie la présence de cycles de poids négatif
    for u in range(n):
        for v in range(n):
            if capacity_matrix[u][v] > 0 and table_bellman[u] + cost_matrix[u][v] < table_bellman[v]:
                raise ValueError("Le graphe contient un cycle de poids négatif.")

    return table_bellman, predecesseurs



def bfs(graphe, sommet_initial, sommet_arrivee, predecesseur):#Recherche en largeur pour un chemin de flux maximal.
    visités = [False] * len(graphe)  # Marque les sommets visités
    file = deque([sommet_initial])   # File initialisée avec le sommet source
    visités[sommet_initial] = True   # Marque le sommet source comme visité
    predecesseur[sommet_initial] = -1 # Aucun prédécesseur pour le sommet source

    while file:  # Parcourt les sommets dans la file
        sommet_courant = file.popleft()     # Défile le sommet courant
        for voisin, capacité in enumerate(graphe[sommet_courant]):  # Parcourt les voisins
            if not visités[voisin] and capacité > 0:                # Si voisin non visité et capacité > 0
                file.append(voisin)            # Ajoute le voisin à la file
                predecesseur[voisin] = sommet_courant  # Met à jour le prédécesseur
                visités[voisin] = True         # Marque le voisin comme visité
                if voisin == sommet_arrivee:   # Si on atteint le puits
                    return True                # Chemin trouvé
    return False  # Aucun chemin trouvé

def ford_fulkerson(graphe, sommet_initial, sommet_arrivee):  #Algorithme de Ford-Fulkerson pour calculer le flot maximal.
    graphe_complementaire = [ligne[:] for ligne in graphe]  # Copie le graphe pour capacités restantes
    predecesseur = [-1] * len(graphe)                       # Tableau pour stocker les prédécesseurs
    flot_max = 0                                            # Initialisation du flot maximal

    # Tant qu'on trouve un chemin de flux maximal dans le graphe complémentaire
    while bfs(graphe_complementaire, sommet_initial, sommet_arrivee, predecesseur):
        flot_chemin = float('Inf')  # Flot minimal sur le chemin trouvé
        sommet_actuel = sommet_arrivee

        # Détermine le flot minimal du chemin
        while sommet_actuel != sommet_initial:
            parent = predecesseur[sommet_actuel]  # Récupère le prédécesseur
            flot_chemin = min(flot_chemin, graphe_complementaire[parent][sommet_actuel])  # Met à jour le flot minimal
            sommet_actuel = parent  # Remonte au sommet précédent

        # Met à jour les capacités restantes dans le graphe complémentaire
        sommet_actuel = sommet_arrivee
        while sommet_actuel != sommet_initial:
            parent = predecesseur[sommet_actuel]  # Récupère le prédécesseur
            graphe_complementaire[parent][sommet_actuel] -= flot_chemin  # Réduit la capacité dans le sens du chemin
            graphe_complementaire[sommet_actuel][parent] += flot_chemin  # Augmente la capacité dans le sens inverse
            sommet_actuel = parent  # Remonte au sommet précédent

        flot_max += flot_chemin  # Ajoute le flot trouvé au flot maximal total

    return flot_max  # Retourne le flot maximal

def creation_matrice(nb_sommet):
    C = [[0 for _ in range(nb_sommet)] for _ in range(nb_sommet)]    # Crée une matrice nb_sommet x nb_sommet remplie de 0
    nbr_couples = (nb_sommet * nb_sommet) // 2                        # Détermine le nombre d’arcs (la moitié des paires possibles)

    for _ in range(nbr_couples):
        while True:
            a, b = random.randint(0, nb_sommet - 1), random.randint(0, nb_sommet - 1)  # Choix aléatoire de deux sommets
            if a != b and C[a][b] == 0:                                               # Vérifie pas de boucle ni d'arc existant
                C[a][b] = random.randint(1, 100)                                      # Assigne une capacité entre 1 et 100
                break
    return C
def etudier_complexite():
    tailles = [10, 20, 40, 60, 100]  # Tailles des graphes à tester
    repetitions = 100                # 100 répétitions pour chaque taille
    resultats = []                   # Liste pour stocker (taille, temps moyen)

    for nb_sommet in tailles:  # Pour chaque taille de graphe
        temps = []             # Liste pour stocker les temps d'exécution
        for _ in range(repetitions):  # 100 répétitions
            graphe = creation_matrice(nb_sommet)   # Crée un graphe aléatoire
            start_time = time.time()               # Début du chronométrage
            ford_fulkerson(graphe, 0, nb_sommet - 1)  # Calcule le flot maximal
            temps.append(time.time() - start_time)     # Enregistre le temps d'exécution
        moyenne_temps = sum(temps) / repetitions   # Calcule le temps moyen
        resultats.append((nb_sommet, moyenne_temps))   # Stocke (taille, temps moyen)
        print(f"Taille: {nb_sommet}, Temps moyen: {moyenne_temps:.5f}s")  # Affiche les résultats

    # Affichage des résultats sous forme de graphique
    x, y = zip(*resultats)        # Sépare les tailles et les temps moyens
    plt.plot(x, y, marker='o')    # Trace le graphique
    plt.xlabel("Taille du graphe (nb_sommet)")  # Étiquette axe X
    plt.ylabel("Temps d'exécution moyen (s)")   # Étiquette axe Y
    plt.title("Complexité de Ford-Fulkerson")   # Titre du graphique
    plt.grid(True)               # Ajoute une grille
    plt.show()                   # Affiche le graphique

