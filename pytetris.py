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
        self.__vue.get_bouton().configure(command=self.on_click)
        self.__fen = self.__vue.fenetre()
        self.__fen.bind("<Key-Left>", self.forme_a_gauche)
        self.__fen.bind("<Key-Right>", self.forme_a_droite)
        self.__fen.bind("<Key-Down>", self.forme_tombe)
        self.__fen.bind("<Key-Up>", self.forme_tourne)
        self.__delai = 320
        self.__pause = True
        self.joue()
        self.__fen.mainloop()
        return

    def on_click(self):
        """
        Controleur -> None
        Fonction qui commande le bouton principal.
        """
        if self.__pause:
            self.__vue.get_bouton().configure(text="Pause")
        else:
            self.__vue.get_bouton().configure(text="Reprendre")
        self.__pause = not self.__pause
        return

    def joue(self):
        """
        Controleur -> None
        Boucle principale du jeu. Fait tomber une forme d'une ligne.
        """
        if not self.__tetris.fini() and not self.__pause:
            self.affichage()
        elif self.__tetris.fini():
            self.__vue.get_bouton().configure(text="Recommencer", command=self.recommencer)
            return
        self.__fen.after(self.__delai, self.joue)
        return

    def recommencer(self):
        """
        Controleur -> None
        Recommence le jeu.
        """
        self.__tetris.reinitialise()
        self.__vue.dessine_terrain()
        self.__pause = True
        self.__delai = 320
        self.__vue.get_bouton().configure(text="Commencer", command=self.on_click)
        self.__vue.nettoie_forme_suivante()
        self.joue()
        return

    def affichage(self):
        """
        Controleur -> None
        """
        if self.__tetris.forme_tombe():
            self.__delai = 320
            self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivantes(),
                                              self.__tetris.get_couleur_suivante())
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
        self.__vue.met_a_jour_score(self.__tetris.get_score())
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
    tetris = ModeleTetris()
    ctrl = Controleur(tetris)
