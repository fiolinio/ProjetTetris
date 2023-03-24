from tkinter import *
from modele import *

DIM = 30
COULEURS = ["cyan", "yellow", "green", "red", "orange", "blue", "purple", "dark grey", "black"]


class VueTetris:

    def __init__(self, modele: ModeleTetris):
        """
        VueTetris, ModeleTetris -> VueTetris
        """
        self.__modele = modele
        self.__les_cases = []
        self.__fenetre = Tk()
        self.__fenetre.title("Tetris")
        self.__frame = Frame(self.__fenetre)
        self.__can_terrain = Canvas(self.__fenetre, height=DIM*self.__modele.get_hauteur(),
                                    width=DIM*self.__modele.get_largeur())
        self.__lbl_score = Label(self.__frame, text="Score : 0")
        self.__lbl_score.pack()
        self.__bouton = Button(self.__frame, text="Quitter", command=self.__fenetre.destroy)
        self.__can_terrain.grid(row=0, column=0)
        self.__bouton.pack()
        self.__frame.grid(row=0, column=1)
        for i in range(self.__modele.get_hauteur()):
            temp_l = []
            for j in range(self.__modele.get_largeur()):
                temp_l.append(self.__can_terrain.create_rectangle(j * DIM, i * DIM, (j + 1) * DIM, (i + 1) * DIM,
                                                                  outline="grey", fill=""))
            self.__les_cases.append(temp_l)
        return

    def fenetre(self):
        """
        VueTetris -> Tk
        Retourne l'instance de la fenêtre.
        """
        return self.__fenetre

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
        self.__lbl_score.configure(text=f"Score: {val}")
        return
