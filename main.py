graphe = [
        [0, 16, 13, 0, 0, 0],  # Capacités des arêtes sortant du sommet 0
        [0, 0, 10, 12, 0, 0],  # Capacités des arêtes sortant du sommet 1
        [0, 4, 0, 0, 14, 0],   # Capacités des arêtes sortant du sommet 2
        [0, 0, 9, 0, 0, 20],   # Capacités des arêtes sortant du sommet 3
        [0, 0, 0, 7, 0, 4],    # Capacités des arêtes sortant du sommet 4
        [0, 0, 0, 0, 0, 0]     # Capacités des arêtes sortant du sommet 5
    ]

    n = 6               # Nombre de sommets
    sommet_initial = 0  # Sommet initial (source)
    sommet_arrivee = 5  # Sommet d'arrivée (puits)

    # Calcul du flot maximal avec Ford-Fulkerson
    flot_max = ford_fulkerson(graphe, n, sommet_initial, sommet_arrivee)
    print(f"Le flot maximal est de {flot_max}")  # Affiche le résultat