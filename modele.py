from random import randint


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
        if self.__forme.collision():
            for coord in self.get_coords_forme():
                if coord[1] >= self.__base:
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
        ModeleTetris -> None
        Fait tomber la forme sur le terrain.
        """
        if self.__forme.tombe():
            return
        for c in self.__forme.get_coords():
            self.__terrain[c[1] - 1][c[0]] = -1 if c[1] - 1 >= self.__base else -2
        self.ajoute_forme()
        return

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
        for c in self.__forme.get_coords():
            self.__terrain[c[1]][c[0]] = -1 if c[1] >= self.__base else -2
        self.__forme.a_gauche()
        return

    def forme_a_droite(self):
        """
        ModeleTetris -> None
        Déplace la forme sur le terrain à droite, si possible
        """
        for c in self.__forme.get_coords():
            self.__terrain[c[1]][c[0]] = -1 if c[1] >= self.__base else -2
        self.__forme.a_droite()
        return


class Forme:

    def __init__(self, modele):
        """
        Forme, ModeleTetris -> Forme
        """
        self.__modele = modele
        self.__couleur = 0
        self.__forme = [(-1, 1), (-1, 0), (0, 0), (1, 0)]
        self.__x0 = randint(2, self.__modele.get_largeur() - 2)
        self.__y0 = 0

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
            l.append((i[0] + self.__x0, i[1] + self.__y0))
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
        for coord in blocs_bas:
            if self.__modele.est_occupe(coord[1] + 1, coord[0]):
                return True
        return False

    def tombe(self):
        """
        Forme -> bool
        Fait tomber d'une ligne la forme s'il n'y a pas de collisions.
        Retourne si il y a eu collision.
        """
        if self.collision():
            return True
        self.__y0 += 1
        return False

    def position_valide(self):
        """
        Forme -> bool
        Retourne si la position de la forme est valide.
        """
        for c in self.get_coords():
            if c not in self.get_coords() and self.__modele.est_occupe(c[1], c[0]):
                return False
            if c[0] >= self.__modele.get_largeur() or c[0] < 0:
                return False
            if c[1] >= self.__modele.get_hauteur() or c[1] < 0:
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
