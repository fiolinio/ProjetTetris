from tkinter import *
from modele import *

DIM = 30
COULEURS = ["cyan", "yellow", "green", "red", "orange", "blue", "purple", "dark grey", "black"]
SUIVANT = 6
FONT = "8514oem"
DEF_BG_COLOR = "#4b326d"
RAINBOW = ["red", "orange", "yellow", "green", "blue", "indigo", "violet"]
AIDE = """Le but du jeu est de Tetris est de placer correctement
les formes qui tombent afin de compléter des lignes.
Chaque ligne complétée compte comme un point dans le score,
un bonus de 2 points vous est conféré si vous complétez 4 lignes en même temps.

Commandes:
Flèche Haut: tourner la forme de 90 degrés
Flèche Gauche / Droite: déplacer la forme
Flèche Bas: Accélérer la chute de la forme
R: Placer la forme courante en réserve"""


class VueTetris:

    def __init__(self, modele: ModeleTetris):
        """
        VueTetris, ModeleTetris -> VueTetris
        """
        self.__modele = modele
        self.__les_cases = []
        self.__fenetre = Tk()
        self.__fenetre.resizable(False, False)
        self.fenetre().tk_setPalette(background=DEF_BG_COLOR)
        self.__fenetre.title("Tetris")
        self.__frame = Frame(self.__fenetre)
        self.__fenetre.grid_rowconfigure(1, weight=1)
        self.__can_terrain = Canvas(self.__fenetre, height=DIM * self.__modele.get_hauteur(),
                                    width=DIM * self.__modele.get_largeur())

        Label(self.__frame, text="Forme suivante:", font=(FONT, 15)).pack()
        self.__can_fsuivante = Canvas(self.__frame, height=DIM * SUIVANT, width=DIM * SUIVANT)
        self.__can_fsuivante.pack()

        Label(self.__frame, text="Reserve:", font=(FONT, 15)).pack()
        self.__can_reserve = Canvas(self.__frame, height=DIM * SUIVANT, width=DIM * SUIVANT)
        self.__can_reserve.pack()

        self.__lbl_score = Label(self.__frame, text="Score : 0", font=(FONT, 20), pady=10)
        self.__lbl_score.pack()
        self.__quit_bouton = Button(self.__frame, text="Quitter", command=self.__fenetre.destroy)
        self.__can_terrain.grid(row=0, column=0, rowspan=2)
        self.__bouton = Button(self.__frame, text="Commencer", pady=5)
        self.__bouton.pack()
        self.__quit_bouton.pack()
        self.__reset_bouton = Button(self.__frame, text="Recommencer", pady=5)
        self.__frame.grid(row=0, column=1)
        Button(self.__fenetre, text='?', command=self.fenetre_aide).grid(row=0, column=2, sticky=N)

        self.__txt_tetris = Text(self.__fenetre, font=(FONT, 30), width=7, height=1)
        self.__txt_tetris.insert(END, "Tetris!")
        self.__txt_tetris.configure(state="disabled")
        self.__txt_tetris.grid_propagate(False)
        for i, char in enumerate("Tetris!"):
            self.__txt_tetris.insert("end", char)
            self.__txt_tetris.tag_add(f"tag{i}", f"1.0 + {i} chars", f"1.0 + {i + 1} chars")
        self.colorie_tetris(0)

        for i in range(self.__modele.get_hauteur()):
            temp_l = []
            for j in range(self.__modele.get_largeur()):
                temp_l.append(self.__can_terrain.create_rectangle(j * DIM, i * DIM, (j + 1) * DIM, (i + 1) * DIM,
                                                                  outline="grey", fill=""))
            self.__les_cases.append(temp_l)

        self.__les_suivants = []
        self.__reserve = []
        for i in range(SUIVANT):
            temp_l = []
            for j in range(SUIVANT):
                temp_l.append(self.__can_fsuivante.create_rectangle(j * DIM, i * DIM, (j + 1) * DIM, (i + 1) * DIM,
                                                                    outline="grey", fill=COULEURS[-1]))
            self.__les_suivants.append(temp_l)

            temp_l = []
            for j in range(SUIVANT):
                temp_l.append(self.__can_reserve.create_rectangle(j * DIM, i * DIM, (j + 1) * DIM, (i + 1) * DIM,
                                                                  outline="grey", fill=COULEURS[-1]))
            self.__reserve.append(temp_l)
        del temp_l
        return

    def fenetre(self):
        """
        VueTetris -> Tk
        Retourne l'instance de la fenêtre.
        """
        return self.__fenetre

    def get_bouton(self):
        """
        VueTetris -> Button
        Retourne le bouton principal.
        """
        return self.__bouton

    def get_reset_bouton(self):
        """
        VueTetris -> Button
        Retourne le bouton principal.
        """
        return self.__reset_bouton

    def get_quit_bouton(self):
        """
        VueTetris -> Button
        Retourne le bouton principal.
        """
        return self.__quit_bouton

    def dessine_case(self, i, j, coul):
        """
        VueTetris, int, int, int -> None
        Change la couleur d'une case.
        """
        self.__can_terrain.itemconfigure(self.__les_cases[i][j], fill=COULEURS[coul])
        return

    def dessine_terrain(self):
        """
        VueTetris -> None
        Mets à jour les couleurs des cases.
        """
        for i in range(self.__modele.get_hauteur()):
            for j in range(self.__modele.get_largeur()):
                self.dessine_case(i, j, self.__modele.get_valeur(i, j))
        return

    def dessine_forme(self, coords, couleur):
        """
        VueTetris, list(tuple(int,int)), int -> None
        Dessine une forme sur le terrain.
        """
        for c in coords:
            self.dessine_case(c[1], c[0], couleur)
        return

    def met_a_jour_score(self, val):
        """
        VueTetris, int -> None
        Met à jour le texte contenant le score.
        """
        self.__lbl_score.configure(text=f"Score : {val}")
        return

    def dessine_case_suivante(self, x, y, coul):
        """
        VueTerrain, int, int, int -> None
        Dessine la case sur le terrain
        """
        self.__can_fsuivante.itemconfigure(self.__les_suivants[x][y], fill=COULEURS[coul])
        return

    def dessine_case_reserve(self, x, y, coul):
        """
        VueTerrain, int, int, int -> None
        Dessine la case sur le terrain
        """
        self.__can_reserve.itemconfigure(self.__les_suivants[x][y], fill=COULEURS[coul])
        return

    def nettoie_forme_suivante(self):
        """
        VueTetris -> None
        Nettoie toutes les cases de l'affiche de la forme suivante
        """
        for x in range(SUIVANT):
            for y in range(SUIVANT):
                self.dessine_case_suivante(x, y, -1)
        return

    def nettoie_forme_reserve(self):
        """
        VueTetris -> None
        Nettoie toutes les cases de l'affiche de la forme suivante
        """
        for x in range(SUIVANT):
            for y in range(SUIVANT):
                self.dessine_case_reserve(x, y, -1)
        return

    def dessine_forme_suivante(self, coords, coul):
        """
        VueTetris, list(tuple(int, int)), int -> None
        Dessine la forme qui suit sur l'affichage
        """
        self.nettoie_forme_suivante()
        for c in coords:
            self.dessine_case_suivante(-c[1] + 3, c[0] + 3, coul)
        return

    def dessine_forme_reserve(self, coords, coul):
        """
        VueTetris, list(tuple(int, int)), int -> None
        Dessine la forme qui suit sur l'affichage
        """
        self.nettoie_forme_reserve()
        for c in coords:
            self.dessine_case_reserve(-c[1] + 3, c[0] + 3, coul)
        return

    def fenetre_game_over(self, score, m_score):
        """
        VueTetris -> None
        Affiche la fenêtre de Game Over
        """
        fen_go = Toplevel(self.__fenetre)
        fen_go.resizable(False, False)
        txt_frame = LabelFrame(fen_go)
        Label(txt_frame, text="Game Over!", font=(FONT, 20), fg="red").pack()
        Label(txt_frame, text=f"Votre score: {score}", font=(FONT, 10)).pack()
        Label(txt_frame, text=f"Meilleur score: {m_score}", font=(FONT, 10)).pack()
        txt_frame.grid(row=0, column=0, pady=5)
        Button(fen_go, text="Ok", command=fen_go.destroy).grid(row=1, column=0)
        fen_go.mainloop()
        return

    def fenetre_aide(self):
        """
        VueTetris -> None
        Affiche la fenêtre d'aide.
        """
        fen_aide = Toplevel(self.__fenetre)
        fen_aide.resizable(False, False)
        lbl_texte = Label(fen_aide, text=AIDE, justify='left')
        lbl_texte.grid(row=0, column=0, pady=5)
        Button(fen_aide, text="Ok", command=fen_aide.destroy).grid(row=1, column=0)
        fen_aide.mainloop()

    def affiche_txt_tetris(self):
        """
        VueTetris -> None
        Affiche le texte __txt_tetris.
        """
        self.__txt_tetris.grid(column=1, row=1)

    def cache_txt_tetris(self):
        """
        VueTetris -> None
        Cache le texte __txt_tetris.
        """
        self.__txt_tetris.grid_remove()

    def colorie_tetris(self, decalage):
        """
        VueTetris, int -> None
        Colorie le texte __txt_tetris.
        """
        for i in range(7):
            self.__txt_tetris.tag_config(f"tag{i}", foreground=RAINBOW[(i + decalage) % len(RAINBOW)])
