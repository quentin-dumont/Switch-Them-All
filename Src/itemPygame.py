################################################################################
#IMPORTS ET INITIALISATION

import items
import pygame

IMAGE_FOLDER = "./Images/"

DICO_IMAGE = {
    "rouge" : pygame.image.load(IMAGE_FOLDER+"items-proto/damageSmall.png").convert_alpha(),
    "orange" : pygame.image.load(IMAGE_FOLDER+"items-proto/chargedSmall.png").convert_alpha(),
    "vert" : pygame.image.load(IMAGE_FOLDER+"items-proto/healSmall.png").convert_alpha(),
    "bleu" : pygame.image.load(IMAGE_FOLDER+"items-proto/armorSmall.png").convert_alpha(),
    "violet" : pygame.image.load(IMAGE_FOLDER+"items-proto/poisonSmall.png").convert_alpha(),
}

################################################################################
#CLASSE ITEM_PYGAME

class Item_Pygame(items.Item) :

    #Initialisation=============================================================
    def __init__(self) :

        items.Item.__init__(self)
        self.image = DICO_IMAGE["rouge"]
        self.rect = self.image.get_rect()

    #Affectation des items aux sprites==========================================
    def setSprite(self, color, item_size):
        if color == "🟥" :
            load_img = DICO_IMAGE["rouge"]
            load_img = pygame.transform.scale(load_img, item_size)
            self.image = load_img
            self.rect = self.image.get_rect()
            return self.image
        if color == "🟧" :
            load_img = DICO_IMAGE["orange"]
            load_img = pygame.transform.scale(load_img, item_size)
            self.image = load_img
            self.rect = self.image.get_rect()
            return self.image
        if color == "🟩" :
            load_img = DICO_IMAGE["vert"]
            load_img = pygame.transform.scale(load_img, item_size)
            self.image = load_img
            self.rect = self.image.get_rect()
            return self.image
        if color == "🟦" :
            load_img = DICO_IMAGE["bleu"]
            load_img = pygame.transform.scale(load_img, item_size)
            self.image = load_img
            self.rect = self.image.get_rect()
        if color == "🟪" :
            load_img = DICO_IMAGE["violet"]
            load_img = pygame.transform.scale(load_img, item_size)
            self.image = load_img
            self.rect = self.image.get_rect()
            return self.image

    #Actualisation==============================================================
    def updateSprite(self, size):
        self.setSprite(self.color, size)
        #else : raise Exception(f"La couleur est inconnue : {color}")

################################################################################
