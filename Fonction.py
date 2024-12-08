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
