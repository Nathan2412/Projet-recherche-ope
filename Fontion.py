import sys
from collections import deque

def trouver_chemin_augmentant(graphe, n, sommet_initial, sommet_arrivee, parent):
    visités = [False] * n  # Marque si un sommet a été visité
    file = deque()         # File pour le parcours en largeur

    # Initialisation : Ajoute le sommet initial à la file et le marque comme visité
    file.append(sommet_initial)
    visités[sommet_initial] = True
    parent[sommet_initial] = -1  # Aucun parent pour le sommet initial

    # Parcours en largeur
    while file:
        sommet_courant = file.popleft()  # Prend le sommet en tête de la file

        for next in range(n):  # Parcourt tous les sommets voisins
            if not visités[next] and graphe[sommet_courant][next] > 0:
                file.append(next)             # Ajoute le sommet voisin à la file
                parent[next] = sommet_courant # Enregistre le sommet courant comme parent du voisin
                visités[next] = True          # Marque le voisin comme visité
                # Si on atteint le sommet d'arrivée, on a trouvé un chemin augmentant
                if next == sommet_arrivee:
                    return True
    return False  # Aucun chemin augmentant trouvé

def ford_fulkerson(graphe, n, sommet_initial, sommet_arrivee):
    # Graphe pour stocker les capacités complémentaires
    graphe_complementaire = [ligne[:] for ligne in graphe]

    parent = [-1] * n  # Tableau pour suivre les parents dans les chemins augmentants
    flot_max = 0       # Initialisation du flot maximal à 0

    # Trouver des chemins augmentants tant qu'ils existent
    while trouver_chemin_augmentant(graphe_complementaire, n, sommet_initial, sommet_arrivee, parent):
        # Trouve la capacité minimale le long du chemin augmentant trouvé
        flot_chemin = sys.maxsize
        sommet_actuel = sommet_arrivee
        while sommet_actuel != sommet_initial:
            parent_du_sommet = parent[sommet_actuel]
            flot_chemin = min(flot_chemin, graphe_complementaire[parent_du_sommet][sommet_actuel])
            sommet_actuel = parent_du_sommet

        # Met à jour les capacités complémentaires dans le graphe
        sommet_actuel = sommet_arrivee
        while sommet_actuel != sommet_initial:
            parent_du_sommet = parent[sommet_actuel]
            graphe_complementaire[parent_du_sommet][sommet_actuel] -= flot_chemin  # Réduit la capacité sur l'arête directe
            graphe_complementaire[sommet_actuel][parent_du_sommet] += flot_chemin  # Augmente la capacité sur l'arête inverse
            sommet_actuel = parent_du_sommet

        # Ajoute le flot du chemin augmentant au flot total
        flot_max += flot_chemin

    return flot_max  # Retourne le flot maximal trouvé