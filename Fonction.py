def read_flow_problem(chemin_fichier):
    try:
        with open(chemin_fichier, 'r') as file:
            lines = file.readlines()
            n = int(lines[0].strip())  # Nombre de noeud
            capacity_matrix = []
            for line in lines[1:]:
                row = list(map(int, line.split()))
                capacity_matrix.append(row)
            return capacity_matrix
    except Exception as e:
        print(f"Error reading file {chemin_fichier}: {e}")
        return None