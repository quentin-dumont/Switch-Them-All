################################################################################
#IMPORTS

import pygame
import time
import level
from grille import Grid
################################################################################

font = pygame.font.Font("./font/blowbrush.ttf", 18)
imagesFolder = "./Images/"

fondEnnemyW1 = pygame.image.load(imagesFolder+"fondEnnemyW1.jpg")
fondEnnemyW2 = pygame.image.load(imagesFolder+"fondEnnemyW2.jpg")
fondJoueurW1 = pygame.image.load(imagesFolder+"fondJoueurW1.jpg")
fondJoueurW2 = pygame.image.load(imagesFolder+"fondJoueurW2.jpg")


doriTaille = (288/2,288/2)
doritos1 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Doritos/Doritos-0.png"), doriTaille)
doritos2 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Doritos/Doritos-1.png"), doriTaille)
doritos3 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Doritos/Doritos-4.png"), doriTaille)
doritos4 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Doritos/Doritos-5.png"), doriTaille)
spritesDoritos = [doritos1, doritos2, doritos2, doritos2, doritos3, doritos4, doritos4, doritos4]

requinTaille = (288/2,576/2)
requin1 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Requin/frame1.png"), requinTaille)
requin2 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Requin/frame2.png"), requinTaille)
requin3 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Requin/frame3.png"), requinTaille)
requin4 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/Requin/frame4.png"), requinTaille)
spritesRequin = [requin1, requin1, requin2, requin2, requin3, requin3, requin4, requin4]

chienTaille = (640/4,640/4)
chienB1 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienB/chienavionbleu1.png"), chienTaille)
chienB2 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienB/chienavionbleu2.png"), chienTaille)
chienB3 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienB/chienavionbleu3.png"), chienTaille)
chienB4 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienB/chienavionbleu4.png"), chienTaille)
chienB5 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienB/chienavionbleu5.png"), chienTaille)
spritesChienB = [chienB1, chienB2, chienB3, chienB4, chienB5]

chienR1 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienR/chienavionrouge1.png"), chienTaille)
chienR2 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienR/chienavionrouge2.png"), chienTaille)
chienR3 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienR/chienavionrouge3.png"), chienTaille)
chienR4 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienR/chienavionrouge4.png"), chienTaille)
chienR5 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienR/chienavionrouge5.png"), chienTaille)
spritesChienR = [chienR1, chienR2, chienR3, chienR4, chienR5]

chienA1 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienA/chienavionarcenciel1.png"), chienTaille)
chienA2 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienA/chienavionarcenciel2.png"), chienTaille)
chienA3 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienA/chienavionarcenciel3.png"), chienTaille)
chienA4 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienA/chienavionarcenciel4.png"), chienTaille)
chienA5 = pygame.transform.scale(pygame.image.load(imagesFolder+"Personnages/ChienA/chienavionarcenciel5.png"), chienTaille)
spritesChienA = [chienA1, chienA2, chienA3, chienA4, chienA5]

#CLASSE ENTITY

class Entity():

    #Initialisation=============================================================
    def __init__(self, skin, side, playerBool, basePV, maxPV, armorMax, difficulty = ""):
        self.skin = skin
        self.side = side
        self.player = playerBool
        self.difficulty = difficulty

        #stats
        self.lifeMax = maxPV
        self.life = basePV
        self.damage = 0
        self.chargedMax = 15
        self.charged = 0
        self.armorMax = armorMax
        self.armor = 0
        self.poisonRows = 0
        self.isPoisoned = False

        self.poisonIndic = pygame.transform.scale(pygame.image.load(imagesFolder+"items-proto/poisonSmall.png").convert_alpha(), (28,28))

        #couleurs de jauge
        self.fondBarColor = (30,30,30) #gris très foncé
        self.lifeColor = (0, 230, 0) # vert vif
        self.armorColor = (49, 140, 231) #bleu roi
        self.chargeNullColor = (158, 158, 158) #gris souris
        self.chargeMiddleColor = (223, 109, 20) #orange citrouille
        self.chargeFullColor = (115, 8, 0) #rouge sang



        #pygame.draw.rect(fenetre, (255,0,0), pygame.Rect(500, 0, 200, 30)) BARRE DE VIE

    def calcul_percent(self, stat, statMax) :
        return stat / statMax

    def affiche_jauges(self, surface, coord, dimJauges) :
        longueur, hauteur = dimJauges
        x, y = coord
        chargeColor = (0,0,0)

        lifePercent = self.calcul_percent(self.life, self.lifeMax)
        armorPercent = self.calcul_percent(self.armor, self.armorMax)
        chargePercent = self.calcul_percent(self.charged, self.chargedMax)

        if chargePercent == 1 :
            chargeColor = self.chargeFullColor
        elif chargePercent >= 0.5 :
            chargeColor = self.chargeMiddleColor
        else :
            chargeColor = self.chargeNullColor

        #life
        pygame.draw.rect(surface, self.fondBarColor, pygame.Rect((x-2, y-2), (longueur+4, hauteur+4)))
        pygame.draw.rect(surface, self.lifeColor, pygame.Rect(coord, (lifePercent * longueur, hauteur)))
        if self.life < 0 :
            life = font.render('0', 1, (255,255,255))
        else :
            life = font.render(str(self.life), 1, (255,255,255)) 
        lifeMax = font.render("/   " + str(self.lifeMax), 1, (255,255,255)) 
        surface.blit(life, (x+30,y-1))
        surface.blit(lifeMax, (x+60, y-1))

        #armor
        pygame.draw.rect(surface, self.fondBarColor, pygame.Rect((x-2, y-1+20), (longueur+4, hauteur+4)))
        pygame.draw.rect(surface, self.armorColor, pygame.Rect((x, y+20), (armorPercent * longueur, hauteur)))
        armor = font.render(str(self.armor), 1, (255,255,255)) 
        armorMax = font.render("/   " + str(self.armorMax), 1, (255,255,255)) 
        surface.blit(armor, (x+30,y+19))
        surface.blit(armorMax, (x+60, y+19))

        #charge
        pygame.draw.rect(surface, self.fondBarColor, pygame.Rect((x-2, y-2+42), (longueur+4, hauteur+4)))
        pygame.draw.rect(surface, chargeColor, pygame.Rect((x, y+42), (chargePercent * longueur, hauteur)))
        charge = font.render(str(self.charged), 1, (255,255,255)) 
        chargeMax = font.render("/   " + str(self.chargedMax), 1, (255,255,255)) 
        surface.blit(charge, (x+30,y+40))
        surface.blit(chargeMax, (x+60, y+40))

        if self.isPoisoned :
            surface.blit(self.poisonIndic, (x+122, y-23) )


    def animate(self, fenetre, coords, compteur, isWorld2) :

        if self.skin == "doritos" :
            if isWorld2 :
                fenetre.blit(fondJoueurW2, (188, 292))
                fenetre.blit(fondEnnemyW2, (917, 340))
            else :
                fenetre.blit(fondJoueurW1, (188, 296))
                fenetre.blit(fondEnnemyW1, (920, 345))

            compteur = compteur % len(spritesDoritos)
            fenetre.blit(spritesDoritos[compteur], coords)

        if self.skin == "requin" :
            compteur = compteur % len(spritesRequin)
            fenetre.blit(spritesRequin[compteur], coords)

        if self.skin == "chienB" :
            compteur = compteur % len(spritesChienB)
            fenetre.blit(spritesChienB[compteur], coords)

        if self.skin == "chienR" :
            compteur = compteur % len(spritesChienR)
            fenetre.blit(spritesChienR[compteur], coords)

        if self.skin == "chienA" :
            compteur = compteur % len(spritesChienA)
            fenetre.blit(spritesChienA[compteur], coords)



    #Fin de Partie==============================================================
    def end_game(self, surface, level) :
        if (self.life <= 0) :

            if (self.player == False) :
                if (level.unlockedLevel < level.totalLevel and level.niveau == level.unlockedLevel) :
                    level.unlockedLevel += 1
                return True

            else : return True

        else : return False

    #Application des altérations================================================

    def update_defense(self, grille) :
        if type(grille) == Grid :
            dico = grille.destroy()

            damage = dico["🟥"]
            poison = dico["🟪"]

            if damage > 0 :
                if self.charged == self.chargedMax :
                    damage = dico["🟥"] * 3
                    self.charged = 0
                elif self.charged >= self.chargedMax/2 :
                    damage = dico["🟥"] * 2
                    self.charged = 0

            
            charge = dico["🟧"]
            heal = dico["🟩"]
            armor = dico["🟦"]

            if heal > 0 :
                self.apply_heal(heal)
            if charge > 0 :
                self.apply_charge(charge)
            if armor > 0 :
                self.apply_armor(armor)

            return damage, poison

        else : raise Exception("l'objet passé en paramètre n'est pas une grille")

    def update_attack(self, damage, poison) :
        self.apply_damage(damage)
        self.apply_poison(poison)

    def update_poison(self) :
        self.update_poison_rows()


    def affiche_stats_console(self, entityName) :

        print("Récapitulatif après un tour : "+entityName)
        print("\nPOINTS DE VIE (MAX :"+str(self.lifeMax)+") : "+str(self.life))
        print("\nPOINTS D'ARMURE (MAX :"+str(self.armorMax)+") : "+str(self.armor))
        print("\nEMPOISONNE ? "+str(self.isPoisoned)+" RESTE "+str(self.poisonRows)+" TOURS DE POISON")
        print("\nJAUGE DE CHARGE (MAX :"+str(self.chargedMax)+") : "+str(self.charged))


    #Soins======================================================================
    def apply_heal(self, val) :
        if val > 0 :
            #print("vie actuelle : " + str(self.life))
            if (self.life + val) < (self.lifeMax) :
                self.life += val
            else :
                self.life = self.lifeMax
            #print("vie + soin : " + str(self.life))
        #else : print("aucune vie ajoutée")

    #Coup spécial===============================================================
    def apply_charge(self, val) :
        if val > 0 :
            #print("jauge d'attaque chargée actuelle : " + str(self.charged))
            if (self.charged + val) < self.chargedMax :
                self.charged += val
            else :
                self.charged = self.chargedMax
            #print("jauge d'attaque chargée + charge : " + str(self.charged))

        #else : print("aucune charge ajoutée")


    #Bouclier===================================================================
    def apply_armor(self, val) :
        if val > 0 :
            #print("shield actuel : " + str(self.armor))
            if (self.armor + val) < self.armorMax :
                self.armor += val
            else :
                self.armor = self.armorMax
            #print("shield new : " + str(self.armor))
        #else : print("aucune armure ajoutée")

    #Poison=====================================================================
    def apply_poison(self, val) :
        if val > 0 :
            if self.poisonRows == 0 :
                self.poisonRows = val
                self.isPoisoned = True
            else :
                self.poisonRows += 1
        #else : print("aucun poison ajouté")

    def update_poison_rows(self) :
        if self.poisonRows > 0 :
            #print("1 tour de poison écoulé, 2PV * le nombre de tour d'empoisonnement restant retiré")
            print("life = " + str(self.life) + " -> " + str(self.life - 2 * self.poisonRows))
            self.life -= (1.5 * self.poisonRows)
            self.poisonRows -= 1
        else :
            #print("Plus/Pas empoisonné")
            self.isPoisoned = False

    #Dégâts=====================================================================
    def apply_damage(self, val) :
        if val > 0 :
            #print("vie actuelle : " + str(self.life))
            if self.armor == 0 :
                if (self.life - val) > 0 :
                    self.life -= val
                else :
                    self.life = 0
            else :
                if self.armor > val :
                    self.armor -= val
                else :
                    val -= self.armor
                    self.armor = 0
                    self.life -= val
            #print("vie - dégâts : " + str(self.life))
        #else : print("aucun dégât subit")

################################################################################
