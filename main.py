import pygame
import random
import time
from plateau import *

play = True
while play:
    # initialisation de pygame
    pygame.init()

    # personnalisation de la fenêtre
    screen = pygame.display.set_mode(
        (800, 600), pygame.RESIZABLE
    )  # taille de la fenêtre = 800px/600px, redimensionnable
    pygame.display.set_caption("hexpansion")  # titre de la fenêtre
    logo = pygame.image.load("images/logo.png").convert_alpha()
    pygame.display.set_icon(logo)  # initialisation du logo

    # variable
    plateau = Plateau(screen)
    plateau.construire()
    plateau.stress()

    for i in range(1, 7):
        Nb_cellules = len(plateau.cellules)
        cellule = plateau.cellules[random.randint(0, Nb_cellules)]
        cellule.proprietaire = i
        cellule.force = 10

    # début du programme
    play_game = True

    while play_game and play:
        time.sleep(0.05)
        screen.fill((255, 255, 255))  # change la couleur de la fenêtre en blanc

        # test si il y a un évènement pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False  # fermeture du programme
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    plateau.affiche_stress = not plateau.affiche_stress
                if event.key == pygame.K_a:
                    play_game = False
        plateau.deplacement()
        plateau.propagation()
        plateau.recrutement()
        plateau.stress()

        # rafraichissement de la fenêtre
        plateau.afficher()
        pygame.display.flip()

    # fin du programme
    pygame.quit()
