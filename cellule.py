class Cellule:

    def __init__(self, ligne, colonne):
        self.ligne = ligne
        self.colonne = colonne
        self.proprietaire = 0
        self.stress = 0
        self.futur_stress = 0
        self.futur_force = 0
        self.force = 1
        self.voisins = []
        self.list_agresseurs = [0, 0, 0, 0, 0, 0, 0]
