from vue import *
import time
import threading


class Controleur:

    def __init__(self, mdl: ModeleTetris):
        """
        Controleur, ModeleTetris -> Controleur
        """
        self.__tetris = mdl
        self.__vue = VueTetris(mdl)
        self.__vue.get_bouton().configure(command=self.on_click)
        self.__fen = self.__vue.fenetre()
        self.__fen.bind("<Key-Left>", lambda event: self.forme_a_gauche())
        self.__fen.bind("<Key-Right>", lambda event: self.forme_a_droite())
        self.__fen.bind("<Key-Down>", lambda event: self.forme_tombe())
        self.__fen.bind("<Key-Up>", lambda event: self.forme_tourne())
        self.__fen.bind("r", lambda event: self.ajoute_reserve())
        self.__delai = 320
        self.__pause = True
        self.__m_score = 0  # Variable de meilleur score
        self.__vue.get_reset_bouton().configure(command=self.recommencer)
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
            self.__vue.get_quit_bouton().pack_forget()
            self.__vue.get_reset_bouton().pack_forget()
        else:
            self.__vue.get_bouton().configure(text="Reprendre")
            self.__vue.get_quit_bouton().pack_forget()
            self.__vue.get_reset_bouton().pack()
            self.__vue.get_quit_bouton().pack()
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
            self.__vue.get_reset_bouton().pack()
            if self.__tetris.get_score() > self.__m_score:
                self.__m_score = self.__tetris.get_score()
            self.__vue.fenetre_game_over(self.__tetris.get_score(), self.__m_score)
            return
        self.__fen.after(self.__delai, self.joue)
        return

    def recommencer(self):
        """
        Controleur -> None
        Recommence le jeu.
        """
        self.__vue.get_reset_bouton().pack_forget()
        self.__tetris.reinitialise()
        self.__vue.dessine_terrain()
        self.__pause = True
        self.__delai = 320
        self.__vue.get_bouton().configure(text="Commencer", command=self.on_click)
        self.__vue.nettoie_forme_suivante()
        self.__vue.nettoie_forme_reserve()
        self.joue()
        return

    def affichage(self):
        """
        Controleur -> None
        """
        if self.__tetris.forme_tombe():
            self.__delai = 320
        if self.__tetris.get_a_tetris():
            threading.Thread(target=self.event_tetris).start()
        self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivantes(),
                                          self.__tetris.get_couleur_suivante())
        self.__vue.dessine_terrain()
        self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
        self.__vue.met_a_jour_score(self.__tetris.get_score())
        return

    def forme_a_gauche(self):
        """
        Controleur, Event -> None
        Demande à la forme de se déplacer vers la gauche.
        """
        self.__tetris.forme_a_gauche()
        return

    def forme_a_droite(self):
        """
        Controleur, Event -> None
        Demande à la forme de se déplacer vers la droite.
        """
        self.__tetris.forme_a_droite()
        return

    def forme_tombe(self):
        """
        Controleur, Event -> None
        Augmente la vitesse de tombée des formes.
        """
        self.__delai = 50
        return

    def forme_tourne(self):
        """
        Controleur, Event -> None
        Demande au terrain de faire tourner la forme, si possible.
        """
        self.__tetris.forme_tourne()
        return

    def event_tetris(self):
        """
        Controleur -> None
        Contrôle les actions du composant de texte __lbl_tetris
        """
        self.__vue.affiche_txt_tetris()
        for i in range(12):
            self.__vue.colorie_tetris(i)
            time.sleep(0.1)
        self.__vue.cache_txt_tetris()
        return

    def ajoute_reserve(self):
        """
        Controleur -> None
        Ajoute la forme à la reserve.
        """
        self.__delai = 320
        self.__tetris.ajoute_reserve()
        self.__vue.dessine_forme_reserve(self.__tetris.get_coords_reserve(),
                                         self.__tetris.get_couleur_reserve())


if __name__ == "__main__":
    tetris = ModeleTetris()
    ctrl = Controleur(tetris)
