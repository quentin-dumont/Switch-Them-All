'''Ce fichier contient des fonctions d'initialisation de la grille de jeu,
ainsi que des fonctions et détecteurs de base qui la concerne directement.'''
################################################################################
#IMPORTS ET INITIALISATIONS

from os import TMP_MAX
import entity
from items import *
from random import randint
import itemPygame
import pygame
import time
################################################################################
#CLASSE GRID

class Grid(pygame.sprite.Sprite):

    #Initialisation=============================================================
    def __init__(self, x, y, image, dim) :
        '''INITIALISATION DE LA CLASSE'''
        pygame.sprite.Sprite.__init__(self)

        self.largeur = 7
        self.longueur = 7
        self.type = 0
        self.grid = []
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (dim, dim))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.cree_ligne()
        self.cree_grille()

    #Création de la grille======================================================
    def cree_ligne(self) :
        '''CREATION DE GRILLE'''
        ligne = []
        for i in range(self.largeur) :
            ligne.append(self.type)
        return ligne

    def cree_grille(self) :
        '''CREATION DE GRILLE'''
        for i in range(self.longueur) :
            self.grid.append(self.cree_ligne())
        self.type = "🔲"
        self.grid.append(self.cree_ligne())
        self.type = 0
        return self.grid

    #Fonctions principales======================================================
    def remplir_grille(self,item_size) :
        while not self.is_pleine() :
            self.feed(item_size)
            #print("feed")
            self.affiche_grille_console()

            self.decalage_item()
            #print("decalage")
            self.affiche_grille_console()

            self.destroy()
            #print("destruction")
            self.affiche_grille_console()


    def switch_en_console(self) :
        '''Fonction d'échange de deux items'''
        i = int(input("ligne du premier objet à déplacer : "))
        j = int(input("colonne du premier objet à déplacer : "))
        i2 = int(input("ligne du deuxième objet à déplacer : "))
        j2 = int(input("colonne du deuxième objet à déplacer : "))

        tmp = self.grid[i][j]
        self.grid[i][j] = self.grid[i2][j2]
        self.grid[i2][j2] = tmp

        if (not self.combo_ligne()) and (not self.combo_colonne()) :

             tmp = self.grid[i][j]
             self.grid[i][j] = self.grid[i2][j2]
             self.grid[i2][j2] = tmp
             return self.switch_en_console()

    def lister_switch(self) :
        '''Gère le choix de l'ia // detection tous les switchs possibles et ajout dans une liste'''
        listeSwitch = []

        for i in range(len(self.grid)) :
            for j in range(len(self.grid[i])) :

                #switch horizontal
                if j+1 < self.largeur and i+1 < self.longueur and self.grid[i+1][j] != "🔲":
                    itemDown = self.grid[i][j]
                    itemUp = self.grid[i][j+1]

                    switch(itemDown, itemUp, (18,18))

                    if (self.combo_ligne()) or (self.combo_colonne()) :
                        listeSwitch.append( [(i,j),(i,j+1)] )
                    #annulation switch
                    switch(itemDown, itemUp, (18,18))

                #switch vertical
                if i+1 < self.longueur and self.grid[i+1][j] != "🔲"  :
                    itemDown = self.grid[i][j]
                    itemUp = self.grid[i+1][j]

                    switch(itemDown, itemUp, (18,18))

                    if (self.combo_ligne()) or (self.combo_colonne()) :
                        listeSwitch.append( [(i,j),(i+1,j)] )
                    #annulation switch
                    switch(itemDown, itemUp, (18,18))

        return listeSwitch

    def calcul_combo(self) :
        combo = 0
        comboC = 0
        comboL = 0
        if self.combo_ligne() != False :
            comboL = len(self.combo_ligne())
        if self.combo_colonne() != False :
            comboC = len(self.combo_colonne())
        if self.is_L() != False :
            combo = comboL + comboC - 1
        else : 
            combo = comboC + comboL
        return combo

    def dico_switch(self) :
        '''Trie les coups possibles par nombre d'items détruits, renvoie un dictionnaire
        contenant des listes des couops qui détruisent respectivement 3, 4, et 5 items.'''

        liste3 = []
        liste4 = []
        liste5 = []

        for i in range(len(self.grid)) :
                for j in range(len(self.grid[i])) :

                    #switch horizontal
                    if j+1 < self.largeur and i+1 < self.longueur and self.grid[i+1][j] != "🔲":
                        itemDown = self.grid[i][j]
                        itemUp = self.grid[i][j+1]

                        switch(itemDown, itemUp, (18,18))

                        if self.combo_ligne() or self.combo_colonne() :

                            combo = self.calcul_combo()
                            if combo >= 5 :
                                liste5.append([ (i,j),(i,j+1)] )
                            elif combo == 4 :
                                liste4.append([ (i,j),(i,j+1)] )
                            elif combo == 3 :
                                liste3.append([ (i,j),(i,j+1)] )

                        #annulation switch
                        switch(itemDown, itemUp, (18,18))

                    #switch vertical
                    if i+1 < self.longueur and self.grid[i+1][j] != "🔲"  :
                        itemDown = self.grid[i][j]
                        itemUp = self.grid[i+1][j]

                        switch(itemDown, itemUp, (18,18))

                        if self.combo_ligne() or self.combo_colonne() :

                            combo = self.calcul_combo()
                            if combo >= 5 :
                                liste5.append( [(i,j),(i+1,j)] )
                            elif combo == 4 :
                                liste4.append( [(i,j),(i+1,j)] )
                            elif combo == 3 :
                                liste3.append( [(i,j),(i+1,j)] )

                        #annulation switch
                        switch(itemDown, itemUp, (18,18))

        dico = {'combo3' : liste3, 'combo4' : liste4, 'combo5' : liste5}
        return dico

    def switch_random(self, listeRandom) :
        print("----------")
        switch_choisi = randint(0, len(listeRandom)-1)

        i,j = listeRandom[switch_choisi][0]
        i2, j2 = listeRandom[switch_choisi][1]

        itemDown = self.grid[i][j]
        itemUp = self.grid[i2][j2]

        print("coup choisi : ", [i,j], [i2,j2])
        switch(itemDown, itemUp, (18,18))

    def switch_ia_easy(self) :
        '''IA Mode facile : choix aléatoire dans une liste de switchs possibles.'''

        listeSwitch = self.lister_switch()
        self.switch_random(listeSwitch)

    def switch_ia_normal(self) :
        '''IA Mode normal : priorité aux combinaisons de 4 puis de 5 puis de 3'''
        dico = self.dico_switch()
        print("coups en 3 : ",dico['combo3'])
        print("coups en 4 : ",dico['combo4'])
        print("coups en 5 : ",dico['combo5'])

        if len(dico['combo4']) >= 1 :
            self.switch_random(dico['combo4'])
        elif len(dico['combo5']) >= 1 :
            self.switch_random(dico['combo5'])
        else :
            self.switch_random(dico['combo3'])

    def switch_ia_hard(self) :
        '''IA Mode difficile : priorité aux combinaisons de 5 puis de 4 puis de 3'''
        dico = self.dico_switch()
        print("coups en 3 : ",dico['combo3'])
        print("coups en 4 : ",dico['combo4'])
        print("coups en 5 : ",dico['combo5'])
        if len(dico['combo5']) >= 1 :
            self.switch_random(dico['combo5'])
        elif len(dico['combo4']) >= 1 :
            self.switch_random(dico['combo4'])
        else :
            self.switch_random(dico['combo3'])

    #Affichage==================================================================
    def affiche_grille_joueur(self, fenetre) :
            '''Affichage de la grille du joueur sur Pygame'''
            decalage = 0
            for ligne in self.grid :
                for item in ligne :
                    if type(item) == itemPygame.Item_Pygame :
                        coordX = item.coordX * 71 + 405
                        coordY = item.coordY + 124 + decalage
                        item.rect.left = coordX
                        item.rect.top = coordY
                        fenetre.blit(item.image, (coordX, coordY))
                decalage += 70

    def affiche_grille_console(self) :
        '''Affichage de la grille en terminal'''
        for ligne in self.grid :
            for item in ligne :
                if type(item) == itemPygame.Item_Pygame :
                    print(" " + str(item.color) +  " ", end="")
                else :
                    print(" " + str(item) + " ", end="")
            print("\n",end="")

    def affiche_grille_ia(self, fenetre) :
        '''Affichage de la grille de l'ordinateur sur Pygame'''
        decalage = 0
        for ligne in self.grid :
            for item in ligne :
                if type(item) == itemPygame.Item_Pygame :
                    coordX = item.coordX * 21 + 924
                    coordY = item.coordY + 183 + decalage
                    fenetre.blit(item.image, (coordX, coordY))
            decalage += 19.5

    #Remplissage================================================================
    def construct_item(self, item_size) :
        '''Fonction <Générer un item aléatoire>'''
        item = itemPygame.Item_Pygame()
        item.setRandomColor()
        color = item.color
        item.setSprite(color, item_size)
        return item

    def feed(self, item_size) :
        '''Fonction qui alimente constamment la première ligne de la grille'''
        for i in range(len(self.grid[0])) :
            if self.grid[0][i] == 0 :
                self.grid[0][i] = self.construct_item(item_size)
                self.grid[0][i].coordX = i
                self.grid[0][i].coordY = 0


    def decalage_item(self) :
        '''Fonction qui fait tomber les items sur la grille'''
        for ligne in self.grid :
            for item in ligne :
                if type(item) == itemPygame.Item_Pygame :
                    if self.grid[item.coordY+1][item.coordX] == 0 :
                        tmp = self.grid[item.coordY][item.coordX]
                        self.grid[item.coordY][item.coordX] = 0
                        self.grid[item.coordY+1][item.coordX] = tmp
                        item.coordY = item.coordY + 1

    #Destruction Combos=========================================================
    def put_zero(self, liste) :
        value = 0
        key = self.grid[liste[0][0]][liste[0][1]].color
        for i in range(len(liste)) :
            self.grid[liste[i][0]][liste[i][1]] = 0
            value += 1
        return key, value

    def destroy(self) :
        '''Fonction qui détruit les items alignés, et
        retourne à terme le nombre d'items détruits par couleur'''
        dict = {"🟥" : 0,"🟧" : 0,"🟩" : 0,"🟦" : 0,"🟪" : 0}

        while self.is_L() != False :
            liste_a_detruire = self.is_L()
            key, value = self.put_zero(liste_a_detruire)
            dict[key] = value

        while self.combo_ligne() != False :
            liste_a_detruire = self.combo_ligne()
            key, value = self.put_zero(liste_a_detruire)
            dict[key] = value

        while self.combo_colonne() != False :
            liste_a_detruire = self.combo_colonne()
            key, value = self.put_zero(liste_a_detruire)
            dict[key] = value

        return dict

    #Détection==================================================================
    '''Son fonctionnement est simple : elle teste tous les items de la grille
    jusqu'à en trouver un (ou pas) qui marque le début d'alignement d'au moins
    3 items. Si elle n'en trouve pas, elle retourne 0.'''

    def combo_ligne(self) :
        '''combo_ligne et combo_colonne identifient des alignements allant de 3 à 5,
        et retourne les coordonnées des items formant le plus grand alignement. FONCTIONNENT MAIS A OPTIMISER'''
        for i in range(len(self.grid)) :
            for j in range(len(self.grid[i])) :
                if (self.grid[i][j] != 0 and self.grid[i][j] != "🔲") :
                    if (j+4 < self.largeur) and (self.grid[i][j]) == (self.grid[i][j+1]) and (self.grid[i][j]) == (self.grid[i][j+2]) and (self.grid[i][j]) == (self.grid[i][j+3]) and (self.grid[i][j]) == (self.grid[i][j+4]) :
                        return [[i, j], [i,j+1], [i,j+2], [i,j+3], [i,j+4]]
                    elif (j+3 < self.largeur) and (self.grid[i][j]) == (self.grid[i][j+1]) and (self.grid[i][j]) == (self.grid[i][j+2]) and (self.grid[i][j]) == (self.grid[i][j+3]) :
                        return [[i, j], [i,j+1], [i,j+2], [i,j+3]]
                    elif (j+2 < self.largeur) and (self.grid[i][j]) == (self.grid[i][j+1]) and (self.grid[i][j]) == (self.grid[i][j+2]) :
                        return [[i, j], [i,j+1], [i,j+2]]
        return False

    def combo_colonne(self) :
        '''combo_ligne et combo_colonne identifient des alignements allant de 3 à 5,
        et retourne les coordonnées des items formant le plus grand alignement. FONCTIONNENT MAIS A OPTIMISER'''
        for i in range(len(self.grid)) :
            for j in range(len(self.grid[i])) :
                if (self.grid[i][j] != 0 and self.grid[i][j] != "🔲") :
                    if (i+4 < self.longueur) and (self.grid[i][j]) == (self.grid[i+1][j]) and (self.grid[i][j]) == (self.grid[i+2][j]) and (self.grid[i][j]) == (self.grid[i+3][j]) and (self.grid[i][j]) == (self.grid[i+4][j]) :
                        return [[i, j], [i+1,j], [i+2,j], [i+3,j], [i+4,j]]
                    elif (i+3 < self.longueur) and (self.grid[i][j]) == (self.grid[i+1][j]) and (self.grid[i][j]) == (self.grid[i+2][j]) and (self.grid[i][j]) == (self.grid[i+3][j]) :
                        return [[i, j], [i+1,j], [i+2,j], [i+3,j]]
                    elif (i+2 < self.longueur) and (self.grid[i][j]) == (self.grid[i+1][j]) and (self.grid[i][j]) == (self.grid[i+2][j]) :
                        return [[i, j], [i+1,j], [i+2,j]]
        return False

    def is_L(self) :
        '''La fonction is_L détecte tous les T et les angles droits. (A améliorer pour qu'elle
        détecte également les L --> quatre alignés et un sur le côté)'''
        if self.combo_colonne() != 0 and self.combo_ligne() != 0 :
            liste = self.combo_ligne()
            liste2 = self.combo_colonne()
            if len(liste) >= 3 and len(liste2) >= 3 :
                for i in liste :
                    if i in liste2 :
                        for coord in liste2 :
                            if not(coord in liste) :
                                liste.append(coord)
                        return liste
        return False

    def is_pleine(self) :
        for i in range(len(self.grid)) :
            for j in range(len(self.grid[i])) :
                if self.grid[i][j] == 0 :
                    return False
        return True

################################################################################
#FONCTIONS HORS-CLASSE

#Modifications visuelles========================================================
def switch(itemDown, itemUp, size) :
    itemDown.color, itemUp.color = itemUp.color, itemDown.color
    itemDown.updateSprite(size)
    itemUp.updateSprite(size)

def blits(fenetre, fond, background, joueur, ordi, grilleJ, grilleIA, compteur, ennemyCoords, isWorld2) :
    fenetre.blit(background, (140,0))
    fenetre.blit(fond, (0,0))
    fenetre.blit(grilleJ.image, (grilleJ.rect.x, grilleJ.rect.y))
    grilleJ.affiche_grille_joueur(fenetre)
    joueur.affiche_jauges(fenetre, (230, 110), (130,12))
    ordi.affiche_jauges(fenetre, (930, 110), (130,12))
    fenetre.blit(grilleIA.image, (920,180))
    grilleIA.affiche_grille_ia(fenetre)
    joueur.animate(fenetre, (230,400), compteur, isWorld2)
    ordi.animate(fenetre, ennemyCoords, compteur, isWorld2)

def update_grilles(fenetre, fond, background, joueur, ordi, grilleJ, grilleIA, item_sizeJ, item_sizeIA, speed, compteur, ennemyCoords, isWorld2) :

        while not grilleJ.is_pleine() :

            grilleJ.feed(item_sizeJ)
            blits(fenetre, fond, background, joueur, ordi, grilleJ, grilleIA, compteur, ennemyCoords, isWorld2)
            pygame.display.flip()
            pygame.time.delay(speed)

            grilleJ.decalage_item()
            blits(fenetre, fond, background, joueur, ordi, grilleJ, grilleIA, compteur, ennemyCoords, isWorld2)
            pygame.display.flip()
            pygame.time.delay(speed)

            damageIA, poisonIA = joueur.update_defense(grilleJ)
            ordi.update_attack(damageIA, poisonIA)
            joueur.affiche_jauges(fenetre, (230, 110), (130,12))
            ordi.affiche_jauges(fenetre, (930, 110), (130,12))

            pygame.display.flip()
            blits(fenetre, fond, background, joueur, ordi, grilleJ, grilleIA, compteur, ennemyCoords, isWorld2)
            pygame.time.delay(speed)

        while not grilleIA.is_pleine() :

            grilleIA.feed(item_sizeIA)
            fenetre.blit(grilleIA.image, (920,180))
            grilleIA.affiche_grille_ia(fenetre)

            fenetre.blit(grilleJ.image, (grilleJ.rect.x, grilleJ.rect.y))
            grilleJ.affiche_grille_joueur(fenetre)
            pygame.display.flip()
            pygame.time.delay(speed)

            grilleIA.decalage_item()
            fenetre.blit(grilleIA.image, (920,180))
            grilleIA.affiche_grille_ia(fenetre)

            fenetre.blit(grilleJ.image, (grilleJ.rect.x, grilleJ.rect.y))
            grilleJ.affiche_grille_joueur(fenetre)
            pygame.display.flip()
            pygame.time.delay(speed)

            damageJ, poisonJ = ordi.update_defense(grilleIA)
            joueur.update_attack(damageJ, poisonJ)
            joueur.affiche_jauges(fenetre, (230, 110), (130,12))
            ordi.affiche_jauges(fenetre, (930, 110), (130,12))

            pygame.display.flip()
            fenetre.blit(grilleIA.image, (920,180))
            pygame.time.delay(speed)

        joueur.affiche_stats_console("*** JOUEUR ***")
        print('\n')
        ordi.affiche_stats_console("*** ORDINATEUR ***")



def calcul_i_j(frame, channel, sound, status):
    position = pygame.mouse.get_pos()
    for ligne in range(len(frame.spritePosition(0).grid)) :
        for colonne in range(len(frame.spritePosition(0).grid[ligne])) :
            objet = frame.spritePosition(0).grid[ligne][colonne]
            if type(objet) == itemPygame.Item_Pygame :
                if (objet.rect.collidepoint(position)) :
                    if status == 'down' : channel.play(sound)
                    return ligne, colonne
    return -1, -1

################################################################################
#DEBUG

def add_item(self) :
    '''Fonction <Ajouter un item> UTILE POUR DEBUG'''
    item = self.construct_item()  #cet input est à  remplacer par un item généré
    item.color = "🟥"
    ligne = int(input("ligne : "))
    colonne = int(input("colonne : "))
    if item != "" :
        for i in range(len(self.grid)) :
            for j in range(len(self.grid[0])) :
                if (i == ligne) and (j == colonne) :
                    self.grid[i][j] = item

################################################################################
