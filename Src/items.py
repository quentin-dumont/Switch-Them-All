################################################################################
#IMPORTS ET INITIALISATION

import pygame
import random
import sys

listColor = ["🟥","🟧","🟩","🟦","🟪"]
listColorAvailable = ["blanc","🟥","🟧","🟩","🟦","🟪"]
################################################################################
#CLASSE ITEM

class Item():


    #Initialisation=============================================================
    def __init__(self):

        self.color = "blanc"
        self.coordX = 0
        self.coordY = 0

    #Utilitaires================================================================
    def __eq__(self, other):
        if isinstance(other, Item) :
            return self.color == other.color

    #Gestion de la couleur======================================================
    def setColor(self, color): #changer le parametre color de l'item
        if (color in listColor): #verifie que la couleur est comprise dans la liste autorisé
            self.color = color
        else :
            print("couleur non-comprise dans la liste autorisé")

    def getRandomColor(self):
        return random.choice(listColor)

    def setRandomColor(self):
        self.setColor(self.getRandomColor())


################################################################################
