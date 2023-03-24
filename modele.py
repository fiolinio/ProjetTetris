from random import randint


LES_FORMES = [[(0, -1), (0, 0), (0, 1), (0, 2)],
              [(0, 0), (1, 0), (0, 1), (1, 1)],
              [(-1, 0), (0, -1), (0, 0), (1, -1)],
              [(-1, -1), (0, -1), (0, 0), (1, 0)],
              [(-1, -1), (-1, 0), (0, 0), (1, 0)],
              [(-1, 0), (0, 0), (1, 0), (1, 1)],
              [(-1, 0), (0, 0), (0, 1), (1, 0)]]


class ModeleTetris:

    def __init__(self, haut=20, larg=14):
        """
        ModeleTetris -> ModeleTetris
        """
        self.__haut = haut
        self.__larg = larg
        self.__base = 4
        l = []
        for i in range(haut):
            if i >= self.__base:
                l.append([-1 for j in range(larg)])
            else:
                l.append([-2 for j in range(larg)])
        self.__terrain = l
        self.__forme = Forme(self)
        self.__score = 0
        return

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
        for i in range(self.__larg):
            if self.est_occupe(self.__base, i) and self.__forme.collision():
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
        self.suppmrime_lignes_complete()
        if self.__forme.tombe():
            self.ajoute_forme()
            self.__forme = Forme(self)
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
        Retourne les coordonées absolues de la forme.
        """
        return self.__forme.get_coords()

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
            self.__terrain[self.__base+i] = temp[i]
        return

    def suppmrime_lignes_complete(self):
        """
        ModeleTetris -> None
        Supprime les lignes complètes sur le terrain.
        """
        for i in range(self.__base, self.__haut):
            if self.est_ligne_complete(i):
                self.supprime_ligne(i)
                self.__score += 1
        return


class Forme:

    def __init__(self, modele):
        """
        Forme, ModeleTetris -> Forme
        """
        self.__modele = modele
        n = randint(0, len(LES_FORMES) - 1)
        self.__couleur = n
        self.__forme = LES_FORMES[n]
        self.__x0 = randint(2, self.__modele.get_largeur() - 2)
        self.__y0 = 3

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
        l = []
        for i in self.__forme:
            l.append((i[0] + self.__x0, -i[1] + self.__y0))
        return l

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
            self.__forme[i] = (-self.__forme[i][1], self.__forme[i][0])
        if not self.position_valide():
            self.__forme = forme_prec
        return
