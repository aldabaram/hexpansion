import pygame
import random
import time
import menu
from plateau import *

# Ouverture du menu
fenetre_menu = menu.Menu()
options = fenetre_menu.options

# initialisation de pygame
pygame.init()

# personnalisation de la fenêtre
h, w = pygame.display.Info().current_h, pygame.display.Info().current_w
screen = pygame.display.set_mode(
    (w, h), pygame.RESIZABLE
)  # taille de la fenêtre = 800px/600px, redimensionnable
pygame.display.set_caption("hexpansion")  # titre de la fenêtre
logo = pygame.image.load("images/logo.png").convert_alpha()
pygame.display.set_icon(logo)  # initialisation du logo


# variable
plateau = Plateau(screen, h, w, options)
plateau.construire()
plateau.stress()

play_game = True
play = True

for i in range(1, plateau.nb_joueurs + 1):
    id = random.randint(0, len(plateau.cellules))
    c = plateau.cellules[id]
    c.proprietaire = i
    c.force = 10

while play:
    time.sleep(0.1)
    screen.fill((255, 255, 255))  # change la couleur de la fenêtre en blanc

    if plateau.nb_joueurs_restant == 1:
        play = False

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
    """
    while play_game:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_game = False
    """

# fin du programme
pygame.quit()
