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
        self.__tetris.forme_tombe()
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
        return


if __name__ == "__main__":
    tetris = modele.ModeleTetris()
    ctrl = Controleur(tetris)
