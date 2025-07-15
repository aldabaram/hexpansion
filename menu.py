import tkinter as tk
from tkinter import ttk

class Menu:
    def __init__(self):
        self.tk = tk.Tk()
        self.options = dict()
        self.tk.title("Menu hexpansion")
        self.tk.geometry("400x200")
        self.tk.resizable(False, False)

        # Style pour les widgets ttk pour un look plus moderne et plat
        style = ttk.Style()
        style.theme_use('clam') # Le thème 'clam' est généralement plat
        style.configure('TFrame', background="#ffffff")
        style.configure('TLabel', background="#ffffff", font=('Verdana', 10))

        # Style pour le bouton : plat, sans bordure, et sans focus visuel
        style.configure('TButton', font=('Verdana', 10, 'bold'),
                        relief='flat',
                        borderwidth=0,
                        focusthickness=0,
                        focuscolor='none'
                       )
        # Changement de couleur au survol pour le bouton
        style.map('TButton',
                  background=[('active', '#e0e0e0'), ('!disabled', '#d0d0d0')],
                  foreground=[('active', 'black'), ('!disabled', 'black')]
                 )

        # Style pour la case à cocher : supprime le pointillé (focus ring)
        style.configure('TCheckbutton', focuscolor=style.lookup('TCheckbutton', 'background'), font=('Verdana', 10))

        # Style pour la zone de texte : plat avec une bordure minimale
        style.configure('TEntry',
                        fieldbackground='white',
                        bordercolor='lightgray',
                        borderwidth=1,
                        relief='flat',
                        font=('Verdana', 10)
                       )

        # Style pour le menu déroulant (TMenubutton) : plat, sans bordure, et sans focus visuel
        style.configure('TMenubutton',
                        relief='flat',
                        borderwidth=0,
                        focusthickness=0,
                        focuscolor='none',
                        background='white', # Couleur de fond du bouton du menu déroulant
                        arrowcolor='black', # Couleur de la flèche du menu déroulant
                        font=('Verdana', 10)
                       )
        # Changement de couleur au survol pour le menu déroulant
        style.map('TMenubutton',
                  background=[('active', '#e0e0e0'), ('!disabled', '#d0d0d0')]
                 )


        self.main_frame = ttk.Frame(self.tk, padding="20 20 20 20")
        self.main_frame.pack(expand=True, fill='both')

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)

        # Nombre de joueurs
        ttk.Label(self.main_frame, text="Nombre de joueurs :").grid(row=0, column=0, sticky='w', pady=5)
        # Assurez-vous que le style est appliqué au menu déroulant
        self.player_count_var = tk.StringVar(self.tk)
        player_options = [str(i) for i in range(0, 7)]
        self.player_menu = ttk.OptionMenu(self.main_frame, self.player_count_var, *player_options, style='TMenubutton')
        self.player_count_var.set("6")
        self.player_menu.grid(row=0, column=1, sticky='ew', pady=5)

        # Dessiner les bords des hexagones
        self.draw_borders_var = tk.BooleanVar()
        self.draw_borders_var.set(True)
        self.border_checkbox = ttk.Checkbutton(self.main_frame, text="Dessiner les bords des hexagones", variable=self.draw_borders_var, style='TCheckbutton')
        self.border_checkbox.grid(row=1, column=0, columnspan=2, sticky='w', pady=5)

        # Nombre de colonnes
        ttk.Label(self.main_frame, text="Nombre de colonnes :").grid(row=2, column=0, sticky='w', pady=5)
        self.column_count_entry = ttk.Entry(self.main_frame)
        self.column_count_entry.insert(0, "50")
        self.column_count_entry.grid(row=2, column=1, sticky='ew', pady=5)

        # Bouton Démarrer
        self.start_button = ttk.Button(self.main_frame, text="Jouer", command=self.start_game, style='TButton')
        self.start_button.grid(row=4, column=0, columnspan=2, pady=15)

        self.tk.mainloop()

    # Fonction qui sera appelée lorsque le bouton "Démarrer" est cliqué
    def start_game(self):
        options = dict()
        options['nb_joueurs'] = int(self.player_count_var.get())
        options['bords'] = self.draw_borders_var.get()
        options['nb_colonnes'] = int(self.column_count_entry.get())

        self.tk.destroy()
        self.options = options


if __name__ == '__main__':
    menu = Menu()