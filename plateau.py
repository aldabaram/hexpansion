import pygame
import math
from cellule import *


class Plateau:
    def __init__(self, screen, height, width, options):
        self.screen = screen
        self.height = height
        self.menu_width = int(width / 5)
        self.board_width = int(width / 5 * 4)
        self.num_columns = options['nb_colonnes']
        self.display_stress = False
        self.cells = []
        self.num_players = options['nb_joueurs']
        self.remaining_players = self.num_players
        self.show_border = options['bords']  # display borders of the hexagons
        self.hex_size = self.board_width / (3 * self.num_columns)  # side of the hexagon
        self.menu_hex_size = self.menu_width // 13
        self.hex_spacing = self.menu_hex_size * 1.5
        self.hex_height = self.hex_size * math.sqrt(3) / 2  # height of the hexagon
        self.num_rows = int(self.height // self.hex_height)
        self.active_hex = 1
        self.border_color = 'white'
        self.player_colors = {
            0: (240, 240, 240),
            1: (200, 0, 0),
            2: (0, 200, 0),
            3: (0, 0, 200),
            4: (200, 200, 0),
            5: (0, 200, 200),
            6: (200, 0, 200),
        }

        # Initialize fonts (once in the constructor)
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def construire(self):
        """Builds the hexagonal grid and defines neighbor relationships."""
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell = Cellule(row, col)
                self.cells.append(cell)
                # Find and set neighbors
                neighbor_cell = self.find_cell(col - 1 + row % 2, row - 1)
                if neighbor_cell is not None:
                    cell.voisins.append(neighbor_cell)
                    neighbor_cell.voisins.append(cell)
                neighbor_cell = self.find_cell(col + row % 2, row - 1)
                if neighbor_cell is not None:
                    cell.voisins.append(neighbor_cell)
                    neighbor_cell.voisins.append(cell)
                neighbor_cell = self.find_cell(col, row - 2)
                if neighbor_cell is not None:
                    cell.voisins.append(neighbor_cell)
                    neighbor_cell.voisins.append(cell)

    def get_adjusted_color(self, color, level):
        """Returns a lighter/darker version of a color based on a level."""
        if self.display_stress:
            level = level / 10
        else:
            level = min(max(level, 1), 10)  # level between 1 and 10
        r, g, b = color
        r = max(0, min(255, 255 - ((255 - r) / 10) * level))
        g = max(0, min(255, 255 - ((255 - g) / 10) * level))
        b = max(0, min(255, 255 - ((255 - b) / 10) * level))
        return int(r), int(g), int(b)
    
    def get_adjusted_color_menu(self, color, level):
        """Returns a lighter/darker version of a color based on a level."""
        level = min(max(level, 1), 10)  # level between 1 and 10
        r, g, b = color
        r = max(0, min(255, 255 - ((255 - r) / 10) * level))
        g = max(0, min(255, 255 - ((255 - g) / 10) * level))
        b = max(0, min(255, 255 - ((255 - b) / 10) * level))
        return int(r), int(g), int(b)



    def afficher(self):
        """Draws the hexagonal grid on the screen."""
        for cell in self.cells:
            if not self.display_stress:
                color = self.get_adjusted_color(self.player_colors[cell.proprietaire], cell.force)
            else:
                color = self.get_adjusted_color(self.player_colors[cell.proprietaire], cell.stress)
            
            x_offset = (self.hex_size * 3) * cell.colonne + cell.ligne % 2 * self.hex_size * 1.5
            y_offset = (self.hex_height) * cell.ligne
            
            hexagon_points = [
                (self.hex_size / 2 + x_offset, y_offset),
                (self.hex_size * 1.5 + x_offset, y_offset),
                (self.hex_size * 2 + x_offset, self.hex_height + y_offset),
                (self.hex_size * 1.5 + x_offset, self.hex_height * 2 + y_offset),
                (self.hex_size / 2 + x_offset, self.hex_height * 2 + y_offset),
                (x_offset, self.hex_height + y_offset),
            ]
            pygame.draw.polygon(self.screen, color, hexagon_points)
            
        if self.show_border:
            for cell in self.cells:
                x_offset = (self.hex_size * 3) * cell.colonne + cell.ligne % 2 * self.hex_size * 1.5
                y_offset = (self.hex_height) * cell.ligne
                hexagon_points = [
                    (self.hex_size / 2 + x_offset, y_offset),
                    (self.hex_size * 1.5 + x_offset, y_offset),
                    (self.hex_size * 2 + x_offset, self.hex_height + y_offset),
                    (self.hex_size * 1.5 + x_offset, self.hex_height * 2 + y_offset),
                    (self.hex_size / 2 + x_offset, self.hex_height * 2 + y_offset),
                    (x_offset, self.hex_height + y_offset),
                ]
                pygame.draw.polygon(self.screen, 'white', hexagon_points, width=int(self.hex_size / 4))

    def find_cell(self, col, row):
        """Finds a cell by its column and row coordinates."""
        for cell in self.cells:
            if cell.ligne == row and cell.colonne == col:
                return cell
        return None

    def propagation(self):
        """Handles force propagation between cells."""
        players = set()
        for cell in self.cells:
            players.add(cell.proprietaire)
            if cell.proprietaire != 0:
                effectif = 0
                enemy_cells = []
                for neighbor in cell.voisins:
                    if neighbor.proprietaire != cell.proprietaire:
                        enemy_cells.append(neighbor)
                if len(enemy_cells) > 0:
                    effectif = (cell.force / 2) / len(enemy_cells)
                    cell.force -= effectif
                for neighbor in enemy_cells:
                    neighbor.list_agresseurs[cell.proprietaire] += effectif
        self.remaining_players = len(players)

        # Resolve battles
        for cell in self.cells:
            total_force = sum(cell.list_agresseurs)
            if cell.force >= total_force:
                cell.force -= total_force
            else:
                winner_force = 0
                second_force = 0
                winner = 0
                for i in range(len(cell.list_agresseurs)):
                    if winner_force < cell.list_agresseurs[i]:
                        winner = i
                        second_force = winner_force
                        winner_force = cell.list_agresseurs[i]
                    elif second_force < cell.list_agresseurs[i]:
                        second_force = cell.list_agresseurs[i]
                cell.force = winner_force - second_force
                cell.proprietaire = winner
            cell.list_agresseurs = [0] * 7

    def recruitment(self):
        """Recruits new force for each player's cells."""
        recruitment_rate = 0.08
        for cell in self.cells:
            if cell.force < 10 - recruitment_rate:
                if cell.proprietaire > 0:
                    cell.force += recruitment_rate

    def stress(self):
        """Calculates stress levels for each cell."""
        for cell in self.cells:
            max_ally_stress = 0
            total_enemy_force = 0
            for neighbor in cell.voisins:
                if neighbor.proprietaire == cell.proprietaire:
                    max_ally_stress = max(max_ally_stress, neighbor.stress)
                else:
                    if neighbor.proprietaire == self.active_hex and self.active_hex != 1 and cell.proprietaire == 1:
                        total_enemy_force += neighbor.force * 2
                    else:
                        total_enemy_force += neighbor.force
            cell.futur_stress = max_ally_stress * 0.9 + total_enemy_force 
        for cell in self.cells:
            cell.stress = round(cell.futur_stress, 1)

    def deplacement(self):
        """Handles force movement between cells based on stress."""
        for cell in self.cells:
            if cell.proprietaire != 0:
                max_neighbor_stress = cell.stress
                destinations = []
                for neighbor in cell.voisins:
                    if neighbor.proprietaire == cell.proprietaire:
                        if neighbor.stress > max_neighbor_stress:
                            max_neighbor_stress = neighbor.stress
                            destinations = [neighbor]
                        elif neighbor.stress == max_neighbor_stress:
                            destinations.append(neighbor)
                if destinations:
                    force_to_move = cell.force / (3 * len(destinations))
                    for destination in destinations:
                        destination.futur_force += force_to_move
                        cell.futur_force -= force_to_move
        for cell in self.cells:
            if cell.proprietaire != 0:
                cell.force += cell.futur_force
                cell.futur_force = 0

    # Handles the menu on the right side of the board
    def afficher_menu(self):
        """Draws the main menu and its elements."""
        # Draw a large gray rectangle for the menu
        pygame.draw.rect(
            self.screen,
            (230, 230, 230),
            (self.board_width, 0, self.menu_width, self.height)
        )
        
        # Base menu position
        menu_start_y = 20

        # ------------TOGGLE SWITCH---------------
        toggle_width = 80
        toggle_height = 40
        toggle_radius = toggle_height // 2
        circle_radius = toggle_radius - 4

        toggle_center_x = self.board_width + self.menu_width // 2
        toggle_center_y = menu_start_y + 40

        toggle_rect_x = toggle_center_x - (toggle_width // 2 *1.5)
        toggle_rect_y = toggle_center_y - toggle_height // 2

        toggle_rect = pygame.Rect(toggle_rect_x, toggle_rect_y, toggle_width, toggle_height)
        
        if self.display_stress:
            background_color = (100, 150, 255)
            circle_x = toggle_rect.x + toggle_width - toggle_radius
        else:
            background_color = (200, 200, 200)
            circle_x = toggle_rect.x + toggle_radius
        
        pygame.draw.rect(self.screen, background_color, toggle_rect, border_radius=toggle_radius)
        
        circle_y = toggle_center_y
        pygame.draw.circle(self.screen, (255, 255, 255), (int(circle_x), int(circle_y)), circle_radius)
        
        pygame.draw.circle(self.screen, (200, 200, 200), (int(circle_x) + 1, int(circle_y) + 1), circle_radius - 1)
        pygame.draw.circle(self.screen, (255, 255, 255), (int(circle_x), int(circle_y)), circle_radius - 1)

        # ---------------END TOGGLE SWITCH----------------

        # ---------------PARAMETER HEXAGON----------------
        # draws a hexagon centered in the menu
        menu_hex_size = self.menu_width // 3
        hex_center_x = self.board_width + self.menu_width // 2 - 1.25*menu_hex_size
        hex_center_y = self.height //2 - math.sqrt(3) * menu_hex_size / 2
        hex_height = menu_hex_size * math.sqrt(3) / 2
        
        hexagon_points = [
            (hex_center_x + menu_hex_size / 2, hex_center_y - hex_height),
            (hex_center_x + menu_hex_size * 1.5, hex_center_y - hex_height),
            (hex_center_x + menu_hex_size * 2, hex_center_y),
            (hex_center_x + menu_hex_size * 1.5, hex_center_y + hex_height),
            (hex_center_x + menu_hex_size / 2, hex_center_y + hex_height),
            (hex_center_x, hex_center_y),
        ]
        
        color = self.get_adjusted_color_menu(self.player_colors[1], 3)
        pygame.draw.polygon(self.screen, color, hexagon_points)

        # ---------------END PARAMETER HEXAGON----------------

        #----------------ENEMY HEXAGONS----------------

        font = pygame.font.SysFont(None, 24)
        
        text = font.render("Adversaire prioritaire", True, (150, 150, 150))
        text_width, text_height = text.get_size()
        text_rect = text.get_rect(center=(self.board_width + self.menu_width // 2 -( text_width // 4), hex_center_y + hex_height + 40))
        self.screen.blit(text, text_rect)

        # Displays as many hexagons as there are players below.
        player_hex_rects = [] # New list to store clickable rectangles

        if self.num_players > 3:
            num_first_row = math.ceil(self.num_players / 2)
            num_second_row = self.num_players - num_first_row
        else:
            num_first_row = self.num_players
            num_second_row = 0

        # Initial position for the first row of hexagons
        hex_start_x = self.board_width + (self.menu_width - (num_first_row - 1) * (self.menu_hex_size + self.hex_spacing) - 2*self.menu_hex_size) // 2
        hex_start_y = hex_center_y + hex_height + 80
        
        current_x = hex_start_x
        current_y = hex_start_y

        for i in range(1, self.num_players + 1):
            if i > num_first_row and self.num_players > 3:
                # Move to the second row
                if i == num_first_row + 1:
                     current_x = self.board_width + (self.menu_width - (num_second_row - 1) * (self.menu_hex_size + self.hex_spacing) - 2*self.menu_hex_size) // 2
                     current_y += math.sqrt(3) * self.menu_hex_size + self.hex_spacing
                # Adjust index for the second row for correct offset
                offset_index = i - num_first_row
            else:
                offset_index = i

            # Calculate hexagon points
            x_pos = current_x + (self.menu_hex_size + self.hex_spacing) * (offset_index - 1)
            y_pos = current_y - math.sqrt(3) * self.menu_hex_size / 2

            points = [
                (x_pos + self.menu_hex_size / 2, y_pos),
                (x_pos + self.menu_hex_size * 1.5, y_pos),
                (x_pos + self.menu_hex_size * 2, y_pos + math.sqrt(3) * self.menu_hex_size / 2),
                (x_pos + self.menu_hex_size * 1.5, y_pos + math.sqrt(3) * self.menu_hex_size),
                (x_pos + self.menu_hex_size / 2, y_pos + math.sqrt(3) * self.menu_hex_size),
                (x_pos, y_pos + math.sqrt(3) * self.menu_hex_size / 2),
            ]
            
            # Create a rect for the current hexagon and add it to the list
            hex_rect = pygame.Rect(x_pos, y_pos, self.menu_hex_size * 2, self.menu_hex_size * math.sqrt(3))
            player_hex_rects.append({'rect': hex_rect, 'player_id': i})

            color = self.get_adjusted_color_menu(self.player_colors[i], 5)
            if i == 1:
                color = (255, 255, 255)
            pygame.draw.polygon(self.screen, color, points)
            if i == self.active_hex:
                self.border_color = 'black'
            else:
                self.border_color = 'white'
            pygame.draw.polygon(self.screen, self.border_color, points, width=int(self.menu_hex_size / 4))
            
        return toggle_rect, player_hex_rects
    
    def handle_menu_events(self, event, toggle_rect, player_hex_rects):
        """
        Handles mouse events for the menu elements.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check for toggle switch click
            if toggle_rect and toggle_rect.collidepoint(event.pos):
                self.display_stress = not self.display_stress
            
            # Check for player hexagon click
            for hex_data in player_hex_rects:
                if hex_data['rect'].collidepoint(event.pos):
                    self.active_hex = hex_data['player_id']

