from random import randint

LES_FORMES = [[(0, -1), (0, 0), (0, 1), (0, 2)],
              [(0, 0), (1, 0), (0, 1), (1, 1)],
              [(-1, -1), (0, -1), (0, 0), (1, 0)],
              [(-1, 0), (0, -1), (0, 0), (1, -1)],
              [(-1, -1), (-1, 0), (0, 0), (1, 0)],
              [(1, -1), (-1, 0), (0, 0), (1, 0)],
              [(-1, 0), (0, 0), (0, 1), (1, 0)]]


class ModeleTetris:

    def __init__(self, haut=20, larg=14):
        """
        ModeleTetris -> ModeleTetris
        """
        self.__reserve_utilisee = False
        self.__a_tetris = False
        self.__haut = haut
        self.__larg = larg
        self.__base = 4
        ligne = []
        for i in range(haut):
            if i >= self.__base:
                ligne.append([-1 for j in range(larg)])
            else:
                ligne.append([-2 for j in range(larg)])
        self.__terrain = ligne
        self.__forme = Forme(self)
        self.__suivante = Forme(self)
        self.__score = 0
        self.__reserve = None
        return

    def reinitialise(self):
        """
        ModeleTetris -> None
        Réinitialise le modèle.
        """
        self.__init__()

    def get_largeur(self):
        """
        ModeleTetris -> int
        Retourne la largeur du terrain.
        """
        return self.__larg

    def get_hauteur(self):
        """
        ModeleTetris -> int
        Retourne la hauteur du terrain.
        """
        return self.__haut

    def get_valeur(self, lig, col):
        """
        ModeleTetris, int, int -> int
        Retourne la valeur d'une case.
        """
        return self.__terrain[lig][col]

    def get_score(self):
        """
        ModeleTetris -> int
        Retourne le score.
        """
        return self.__score

    def est_occupe(self, lig, col):
        """
        ModeleTetris, int, int -> bool
        Vérifie si une case est occupée.
        """
        return self.__terrain[lig][col] >= 0

    def fini(self):
        """
        ModeleTetris -> bool
        Vérifie si la partie est finie.
        """
        for i in range(self.__larg - 1):
            if self.est_occupe(self.__base, i) and self.est_occupe(self.__base - 1, i):
                return True
        return False

    def ajoute_forme(self):
        """
        ModeleTetris -> None
        Ajoute la forme sur le terrain.
        """
        for c in self.__forme.get_coords():
            self.__terrain[c[1]][c[0]] = self.__forme.get_couleur()
        return

    def forme_tombe(self):
        """
        ModeleTetris -> bool
        Fait tomber la forme sur le terrain.
        """
        self.supprime_lignes_complete()
        if self.__forme.tombe():
            self.ajoute_forme()
            self.__reserve_utilisee = False
            self.__forme = self.__suivante
            self.__suivante = Forme(self)
            return True
        return False

    def get_couleur_forme(self):
        """
        ModeleTetris -> int
        Retourne la couleur de la forme.
        """
        return self.__forme.get_couleur()

    def get_coords_forme(self):
        """
        ModeleTetris -> list(tuple(int, int))
        Retourne les coordonnées absolues de la forme.
        """
        return self.__forme.get_coords()

    def get_coords_suivantes(self):
        """
        ModeleTetris -> list(tuple(int, int))
        Retourne les coordonnées relatives de la forme suivante.
        """
        return self.__suivante.get_coords_relatives()

    def get_couleur_suivante(self):
        """
        ModeleTetris -> int
        Retourne la couleur de la forme suivante.
        """
        return self.__suivante.get_couleur()

    def get_coords_reserve(self):
        """
        ModeleTetris -> list(tuple(int, int))
        Retourne les coordonnées relatives de la forme en reserve.
        """
        return self.__reserve.get_coords_relatives()

    def get_couleur_reserve(self):
        """
        ModeleTetris -> int
        Retourne la couleur de la forme en reserve.
        """
        return self.__reserve.get_couleur()

    def forme_a_gauche(self):
        """
        ModeleTetris -> None
        Déplace la forme sur le terrain à gauche, si possible
        """
        self.__forme.a_gauche()
        return

    def forme_a_droite(self):
        """
        ModeleTetris -> None
        Déplace la forme sur le terrain à droite, si possible
        """

        self.__forme.a_droite()
        return

    def forme_tourne(self):
        """
        ModeleTetris -> None
        Fait tourner la forme sur le terrain de 90 degrés.
        """
        self.__forme.tourne()
        return

    def est_ligne_complete(self, lig):
        """
        ModeleTetris, int -> bool
        Vérifie si la ligne indicée est complète.
        """
        for i in range(self.__larg):
            if not self.est_occupe(lig, i):
                return False
        return True

    def supprime_ligne(self, lig):
        """
        ModeleTetris, int -> None
        Supprime la ligne indicée sur le terrain.
        """
        temp = [[-1 for i in range(self.__larg)]]
        for i in range(self.__base, lig):
            temp.append(self.__terrain[i])
        for i in range(len(temp)):
            self.__terrain[self.__base + i] = temp[i]
        del temp
        return

    def supprime_lignes_complete(self):
        """
        ModeleTetris -> bool
        Supprime les lignes complètes sur le terrain.
        Retourne si 4 lignes ont été supprimées.
        """
        lignes_comp = 0
        for i in range(self.__base, self.__haut):
            if self.est_ligne_complete(i):
                lignes_comp += 1
                self.supprime_ligne(i)
                self.__score += 1
            if lignes_comp == 4:
                self.__a_tetris = True
                self.__score += 2
                return True
        return False

    def get_a_tetris(self):
        """
        ModeleTetris -> bool
        Retourne la valeur de __a_tetris.
        Réinitialise sa valeur à False.
        """
        if self.__a_tetris:
            self.__a_tetris = False
            return True
        return False

    def ajoute_reserve(self):
        """
        ModeleTetris -> None
        Ajoute la forme courante à la réserve.
        """
        if not self.__reserve_utilisee:
            self.__reserve_utilisee = True
            temp1, temp2, temp3 = self.__reserve, self.__forme, self.__suivante
            if self.__reserve is None:
                self.__reserve = self.__forme
                self.__forme = self.__suivante
                self.__suivante = Forme(self)
            else:
                self.__reserve, self.__forme = self.__forme, self.__reserve
            if not self.__forme.position_valide():
                self.__reserve, self.__forme, self.__suivante = temp1, temp2, temp3
                return
            self.__reserve.reset_position()
        return


class Forme:

    def __init__(self, modele):
        """
        Forme, ModeleTetris -> Forme
        """
        self.__modele = modele
        n = randint(0, len(LES_FORMES) - 1)
        self.__couleur = n
        self.__forme = LES_FORMES[n].copy()
        self.__x0 = randint(3, self.__modele.get_largeur() - 3)
        self.__y0 = self.taille_forme()

    def get_couleur(self):
        """
        Forme -> int
        Retourne la couleur de la forme.
        """
        return self.__couleur

    def get_coords(self):
        """
        Forme -> list(tuple(int, int))
        Retourne les coordonnées absolues d'une forme.
        """
        coords = []
        for i in self.__forme:
            coords.append((i[0] + self.__x0, -i[1] + self.__y0))
        return coords

    def get_coords_relatives(self):
        """
        Forme -> list(tuple(int, int))
        Retourne les coordonnées relatives de la forme.
        """
        return self.__forme

    def collision(self):
        """
        Forme -> bool
        Vérifie si la forme doit se poser.
        """
        # il faut trouver le bloc le plus en bas
        blocs_bas = [self.get_coords()[0]]
        for coord in self.get_coords()[1:]:
            if coord[1] > blocs_bas[0][1]:
                blocs_bas = [coord]
            elif coord[1] == blocs_bas[0][1]:
                blocs_bas.append(coord)
        if blocs_bas[0][1] + 1 >= self.__modele.get_hauteur():
            return True
        for c in self.get_coords():
            if self.__modele.est_occupe(c[1] + 1, c[0]):
                return True
        return False

    def tombe(self):
        """
        Forme -> bool
        Fait tomber d'une ligne la forme s'il n'y a pas de collisions.
        Retourne si il y a eu collision.
        """
        if not self.collision():
            self.__y0 += 1
            return False
        return True

    def position_valide(self):
        """
        Forme -> bool
        Retourne si la position de la forme est valide.
        """
        for c in self.get_coords():
            if c[0] >= self.__modele.get_largeur() or c[0] < 0:
                return False
            if c[1] >= self.__modele.get_hauteur() or c[1] < 0:
                return False
            if self.__modele.est_occupe(c[1], c[0]):
                return False
        return True

    def a_gauche(self):
        """
        Forme -> None
        Déplace la forme à gauche, si possible.
        """
        self.__x0 -= 1
        if not self.position_valide():
            self.__x0 += 1
        return

    def a_droite(self):
        """
        Forme -> None
        Déplace la forme à droite, si possible.
        """
        self.__x0 += 1
        if not self.position_valide():
            self.__x0 -= 1
        return

    def tourne(self):
        """
        Forme -> None
        Fait tourner la forme de 90 degrés.
        """
        forme_prec = self.__forme.copy()
        for i in range(len(self.__forme)):
            self.__forme[i] = (self.__forme[i][1], -self.__forme[i][0])
        if not self.position_valide():
            self.__forme = forme_prec
        return

    def taille_forme(self):
        """
        Forme -> int
        Retourne la taille de la forme, c'est-à-dire l'écart entre le milieu et le bloc le plus haut.
        """
        return max([i[1] for i in self.__forme])

    def reset_position(self):
        """
        Forme -> None
        Réinitialise la position de la forme.
        """
        self.__y0 = self.taille_forme()
        return
