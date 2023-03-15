import modele
from modele import *
from vue import *
import time


class Controleur:

    def __init__(self, mdl: ModeleTetris):
        """
        Controleur, ModeleTetris -> Controleur
        """
        self.__tetris = mdl
        self.__vue = VueTetris(mdl)
        self.__fen = self.__vue.fenetre()
        self.__fen.bind("<Key-Left>", self.forme_a_gauche)
        self.__fen.bind("<Key-Right>", self.forme_a_droite)
        self.__fen.bind("<Key-Down>", self.forme_tombe)
        self.__fen.bind("<Key-Up>", self.forme_tourne)
        self.__delai = 320
        self.joue()
        self.__fen.mainloop()
        return

    def joue(self):
        """
        Controleur -> None
        Boucle principale du jeu. Fait tomber une forme d'une ligne.
        """
        if not self.__tetris.fini():
            self.affichage()
            self.__fen.after(self.__delai, self.joue)

    def affichage(self):
        """
        Controleur -> None
        """
        if self.__tetris.forme_tombe():
            self.__delai = 320
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())

        return

    def forme_a_gauche(self, event):
        """
        Controleur, Event -> None
        Demande à la forme de se déplacer vers la gauche.
        """
        self.__tetris.forme_a_gauche()
        return

    def forme_a_droite(self, event):
        """
        Controleur, Event -> None
        Demande à la forme de se déplacer vers la droite.
        """
        self.__tetris.forme_a_droite()
        return

    def forme_tombe(self, event):
        """
        Controleur, Event -> None
        Augmente la vitesse de tombée des formes.
        """
        self.__delai = 50
        return

    def forme_tourne(self, event):
        """
        Controleur, Event -> None
        Demande au terrain de faire tourner la forme, si possible.
        """
        self.__tetris.forme_tourne()
        return


if __name__ == "__main__":
    tetris = modele.ModeleTetris()
    ctrl = Controleur(tetris)
