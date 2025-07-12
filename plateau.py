import pygame
import random
from cellule import *


class Plateau:
    def __init__(self, screen):
        self.screen = screen
        self.affiche_stress = False
        self.cellules = []
        self.couleurs = {
            0: (240, 240, 240),
            1: (200, 0, 0),
            2: (0, 200, 0),
            3: (0, 0, 200),
            4: (200, 200, 0),
            5: (0, 200, 200),
            6: (200, 0, 200),
        }

    def construire(self):
        for j in range(49):
            for i in range(28):
                c = Cellule(j, i)
                self.cellules.append(c)
                d = self.trouver_cellules(i - 1 + j % 2, j - 1)
                if d is not None:
                    c.voisins.append(d)
                    d.voisins.append(c)
                d = self.trouver_cellules(i + j % 2, j - 1)
                if d is not None:
                    c.voisins.append(d)
                    d.voisins.append(c)
                d = self.trouver_cellules(i, j - 2)
                if d is not None:
                    c.voisins.append(d)
                    d.voisins.append(c)

    def alt_couleur(self, couleur, niveau):
        niveau = min(max(niveau, 1), 10)  # niveau entre 0 et 10
        r, v, b = couleur
        r = max(0, min(255, 255 - ((255 - r) / 10) * niveau))
        v = max(0, min(255, 255 - ((255 - v) / 10) * niveau))
        b = max(0, min(255, 255 - ((255 - b) / 10) * niveau))
        return int(r), int(v), int(b)

    def afficher(self):
        for c in self.cellules:
            if self.affiche_stress == False:
                couleur = self.alt_couleur(self.couleurs[c.proprietaire], c.force)
            else:
                couleur = self.alt_couleur(self.couleurs[c.proprietaire], c.stress)
            espace = 0
            dx = 15 + (45 + espace) * c.colonne + c.ligne % 2 * 22
            dy = 15 + (13 + espace) * c.ligne
            pygame.draw.polygon(
                self.screen,
                couleur,
                [
                    (15.00 + dx, 0.00 + dy),
                    (7.50 + dx, 12.99 + dy),
                    (-7.50 + dx, 12.99 + dy),
                    (-15.00 + dx, 0.00 + dy),
                    (-7.50 + dx, -12.99 + dy),
                    (7.50 + dx, -12.99 + dy),
                ],
            )
        for c in self.cellules:
            espace = 0
            dx = 15 + (45 + espace) * c.colonne + c.ligne % 2 * 22
            dy = 15 + (13 + espace) * c.ligne
            pygame.draw.polygon(
                self.screen,
                (255, 255, 255),
                [
                    (15.00 + dx, 0.00 + dy),
                    (7.50 + dx, 12.99 + dy),
                    (-7.50 + dx, 12.99 + dy),
                    (-15.00 + dx, 0.00 + dy),
                    (-7.50 + dx, -12.99 + dy),
                    (7.50 + dx, -12.99 + dy),
                ],
                width=3,
            )

    def trouver_cellules(self, colonne, ligne):
        for cellule in self.cellules:
            if cellule.ligne == ligne and cellule.colonne == colonne:
                return cellule

    def propagation(self):
        # Déclaration des combat
        for c in self.cellules:
            if c.proprietaire != 0:
                effectif = 0
                list_cellules_ennemi = []
                for v in c.voisins:
                    if v.proprietaire != c.proprietaire:
                        list_cellules_ennemi.append(v)
                if len(list_cellules_ennemi) > 0:
                    effectif = (c.force / 2) / len(list_cellules_ennemi)
                    c.force -= effectif
                for v in list_cellules_ennemi:
                    v.list_agresseurs[c.proprietaire] += effectif
        # Résolution des combats
        for c in self.cellules:
            total_force = 0
            for i in range(len(c.list_agresseurs)):
                total_force += c.list_agresseurs[i]
            if c.force >= total_force:
                c.force -= total_force
            else:
                force_max_2 = 0
                force_max_1 = 0
                gagnant = 0
                for i in range(len(c.list_agresseurs)):
                    if force_max_1 < c.list_agresseurs[i]:
                        gagnant = i
                        force_max_2 = force_max_1
                        force_max_1 = c.list_agresseurs[i]
                    elif force_max_2 < c.list_agresseurs[i]:
                        force_max_2 = c.list_agresseurs[i]
                c.force = force_max_1 - force_max_2
                c.proprietaire = gagnant
            c.list_agresseurs = [0] * 7

    def recrutement(self):
        prop = 0.08
        for c in self.cellules:
            if c.force < 10 - prop:
                if c.proprietaire > 0:
                    c.force += prop

    def stress(self):
        for c in self.cellules:
            st_max_a = 0
            st_max_e = 0
            for v in c.voisins:
                if v.proprietaire == c.proprietaire:
                    st_max_a = max(st_max_a, v.stress)
                else:
                    st_max_e += v.force
            c.futur_stress = st_max_a * 0.9 + st_max_e
        for c in self.cellules:
            c.stress = round(c.futur_stress, 1)

    def deplacement(self):
        for c in self.cellules:
            if c.proprietaire != 0:
                v_stress_max = c.stress
                destination = []
                for v in c.voisins:
                    if v.proprietaire == c.proprietaire:
                        if v.stress > v_stress_max:
                            v_stress_max = v.stress
                            destination = [v]
                        elif v.stress == v_stress_max:
                            destination.append(v)
                if destination != []:
                    effectif = c.force / (3 * len(destination))
                    for d in destination:
                        d.futur_force += effectif
                        c.futur_force -= effectif
        for c in self.cellules:
            if c.proprietaire != 0:
                c.force += c.futur_force
                c.futur_force = 0
