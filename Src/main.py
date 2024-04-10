################################################################################
#IMPORTS ET FENETRE

import sys
import time
import pygame

from pygame.locals import *


#TEST SYSTEME DE PROGRESSION
PROGRESSION = 6
############################

IMAGE_FOLDER = "./Images/"
SOUNDS_FOLDER = "./Sounds/"

if __name__ == '__main__' :

    #Initialisation de la fenêtre===============================================
    pygame.init()
    fenetre = pygame.display.set_mode((1280, 720), vsync=1)
    pygame.display.set_caption('Switch Them ALL!')
    icone = pygame.image.load(IMAGE_FOLDER+"items-proto/damageSmall.png").convert_alpha()
    pygame.display.set_icon(icone)
    
    import items
    import itemPygame
    import entity
    import level
    from  grille import Grid, switch, update_grilles, calcul_i_j

    #Initialisation du son
    pygame.mixer.init()

    musiqueSTA = pygame.mixer.Sound(SOUNDS_FOLDER+"musiqueSTA.mp3")
    buttonPressed = pygame.mixer.Sound(SOUNDS_FOLDER+"buttonSound.mp3")
    switchGood = pygame.mixer.Sound(SOUNDS_FOLDER+"switchSound.mp3")
    switchWrong = pygame.mixer.Sound(SOUNDS_FOLDER+"noswitchSound.mp3")
    victory = pygame.mixer.Sound(SOUNDS_FOLDER+"victory.mp3")

    channelMusic = pygame.mixer.Channel(1)
    channelMouse = pygame.mixer.Channel(0)

    channelMusic.set_volume(0.5)
    channelMouse.set_volume(0.8)

    channelMusic.play(musiqueSTA, 999)


pygame.mouse.set_cursor(pygame.cursors.arrow)
################################################################################
#INITIALISATIONS

#Evenemements===================================================================
NEW_GAME = pygame.USEREVENT + 1
RESET_GAME = pygame.USEREVENT + 2
MENU_PRINCIPAL = pygame.USEREVENT + 3
OPTIONS = pygame.USEREVENT + 4
CHOIX_DIFF1 = pygame.USEREVENT + 5
CHOIX_DIFF2 = pygame.USEREVENT + 6
WIN = pygame.USEREVENT + 7
LOSE = pygame.USEREVENT + 8
HELP = pygame.USEREVENT + 9

#Variables======================================================================
levelManager = level.Level(PROGRESSION)
isWorld2 = False
isMuted = False
isGameEnded = False


################################################################################
#CLASSES SPRITES

class Button(pygame.sprite.Sprite) :
    def __init__(self, x, y, img, evenement, largeur, hauteur) :
        pygame.sprite.Sprite.__init__(self)

        self.evenement = evenement
        self.largeur = largeur
        self.hauteur = hauteur
        self.image = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (self.largeur, self.hauteur))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.triggered = False

    def set_triggered(self, pos):
        if not self.triggered:
            self.triggered = self.rect.collidepoint(pos)
            if self.triggered :
                channelMouse.play(buttonPressed)

    def update(self):
        global isWorld2
        global isMuted

        if self.triggered:

            if self.evenement == 'to_menu' :
                pygame.event.post(pygame.event.Event(MENU_PRINCIPAL))

            if self.evenement == 'to_diff1' :
                isWorld2 = False
                pygame.event.post(pygame.event.Event(CHOIX_DIFF1))

            if self.evenement == 'to_diff2' :
                isWorld2 = True
                pygame.event.post(pygame.event.Event(CHOIX_DIFF2))

            elif self.evenement == 'to_options' :
                pygame.event.post(pygame.event.Event(OPTIONS))

            elif self.evenement == 'to_help' :
                pygame.event.post(pygame.event.Event(HELP))

            elif self.evenement == 'to_level1' :
                levelManager.niveau = 1
                pygame.event.post(pygame.event.Event(NEW_GAME))

            elif self.evenement == 'to_level2' :
                levelManager.niveau = 2
                pygame.event.post(pygame.event.Event(NEW_GAME))

            elif self.evenement == 'to_level3' :
                levelManager.niveau = 3
                pygame.event.post(pygame.event.Event(NEW_GAME))

            elif self.evenement == 'to_level4' :
                levelManager.niveau = 4
                pygame.event.post(pygame.event.Event(NEW_GAME))

            elif self.evenement == 'to_level5' :
                levelManager.niveau = 5
                pygame.event.post(pygame.event.Event(NEW_GAME))

            elif self.evenement == 'to_level6' :
                levelManager.niveau = 6
                pygame.event.post(pygame.event.Event(NEW_GAME))

            elif self.evenement == 'sound_on' :
                channelMusic.play(musiqueSTA, 999)
                isMuted = False
                self.image = pygame.transform.scale(pygame.image.load(IMAGE_FOLDER+"volume_on.png").convert_alpha(), (self.largeur, self.hauteur))
                self.evenement = 'sound_off'

            elif self.evenement == 'sound_off' :
                channelMusic.stop()
                isMuted = True
                self.image = pygame.transform.scale(pygame.image.load(IMAGE_FOLDER+"volume_off.png").convert_alpha(), (self.largeur, self.hauteur))
                self.evenement = 'sound_on'

            elif self.evenement == 'sound_plus' :
                channelMusic.set_volume(channelMusic.get_volume() + 0.1)
                channelMouse.set_volume(channelMouse.get_volume() + 0.1)

            elif self.evenement == 'sound_moins' :
                channelMusic.set_volume(channelMusic.get_volume() - 0.1)
                channelMouse.set_volume(channelMouse.get_volume() - 0.1)

            elif self.evenement == 'leave' :
                sys.exit()

            self.triggered = False

class Decoration(pygame.sprite.Sprite) :
    def __init__(self, x, y, img, largeur, hauteur) :
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.transform.scale(pygame.image.load(img).convert_alpha(), (largeur, hauteur))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

################################################################################
#CLASSES D'AFFICHAGE

class Start() :
    def __init__(self) :
        self.groupSprites = pygame.sprite.Group()
        self.groupSprites.add(Decoration(305, 500, IMAGE_FOLDER+"boutonstart.png", 700, 200))
        self.groupSprites.add(Decoration(345, 65, IMAGE_FOLDER+"logo.png", 600, 600))

    def react(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN :
            channelMouse.play(buttonPressed)
            pygame.event.post(pygame.event.Event(MENU_PRINCIPAL))

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

class Menu() :
    def __init__(self) :
        self.groupSprites = pygame.sprite.Group()
        self.groupSprites.add(Button(475, 100, IMAGE_FOLDER+"panneauPlay.png", 'to_diff1', 375, 231))
        self.groupSprites.add(Button(310, 500, IMAGE_FOLDER+"largeHelp.png", 'to_help', 188, 116))
        self.groupSprites.add(Button(560, 500, IMAGE_FOLDER+"panneauSettings.png", 'to_options', 188, 116))
        self.groupSprites.add(Button(810, 500, IMAGE_FOLDER+"panneauLeave.png", 'leave', 188, 116))

    def react(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            for sprite in self.groupSprites :
                sprite.set_triggered(event.pos)

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

class EndGame() :
    def __init__(self) :
        self.groupSprites = pygame.sprite.Group()
        if levelManager.niveau <= 3 :
            self.groupSprites.add(Button(400, 470, IMAGE_FOLDER+"panneauLevels.png", 'to_diff1', 188, 116))
        else :
            self.groupSprites.add(Button(400, 470, IMAGE_FOLDER+"panneauLevels.png", 'to_diff2', 188, 116))
        self.groupSprites.add(Button(700, 470, IMAGE_FOLDER+"panneauMP.png", 'to_menu', 188, 116))


    def react(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            for sprite in self.groupSprites :
                sprite.set_triggered(event.pos)

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

class Options() :
    def __init__(self) :
        self.groupSprites = pygame.sprite.Group()
        if isMuted :
            self.groupSprites.add(Button(570, 50, IMAGE_FOLDER+"volume_off.png", 'sound_on', 160, 160))
        else :
            self.groupSprites.add(Button(570, 50, IMAGE_FOLDER+"volume_on.png", 'sound_off', 160, 160))
        self.groupSprites.add(Button(770, 50, IMAGE_FOLDER+"plus.png", 'sound_plus', 160, 160))
        self.groupSprites.add(Button(370, 50, IMAGE_FOLDER+"moins.png", 'sound_moins', 160, 160))
        self.groupSprites.add(Button(555, 550, IMAGE_FOLDER+"panneauMP.png", 'to_menu', 188, 116))

    def react(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            for sprite in self.groupSprites :
                sprite.set_triggered(event.pos)

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

class Help() :
    def __init__(self, tutorial, fond) :
        self.groupSprites = pygame.sprite.Group()
        self.tutorial = tutorial
        self.groupSprites.add(Decoration(150,5, IMAGE_FOLDER+"pageHelp0.png", 1000, 720))
        self.groupSprites.add(Button(1040,40, IMAGE_FOLDER+"close.png", "to_menu", 50, 50))
        self.diapo = 0
        self.fond = fond

    def react(self, event) :

        if event.type == pygame.MOUSEBUTTONDOWN :

            for sprite in self.groupSprites :
                if isinstance(sprite, Button) :
                    sprite.set_triggered(event.pos)

            self.diapo += 1
            if self.diapo > 3 :
                self.diapo = 0
            self.groupSprites.sprites()[0].image = tutorial[self.diapo]

            pygame.display.flip()
            pygame.time.delay(10)

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)
        fenetre.blit(self.fond, (0,0))

class Diff() :
    def __init__(self) :
        self.groupSprites = pygame.sprite.Group()
        self.groupSprites.add(Button(560, 550, IMAGE_FOLDER+"panneauMP.png", 'to_menu', 188, 116))
        if levelManager.assertNiveau(4) :
            self.groupSprites.add(Button(920, 350, IMAGE_FOLDER+"pageSuivante.png", 'to_diff2', 100, 100))

        self.groupSprites.add(Button(250, 100, IMAGE_FOLDER+"chiffre1.png", 'to_level1', 250, 176))
        if levelManager.assertNiveau(2) :
            self.groupSprites.add(Button(530, 200, IMAGE_FOLDER+"chiffre2.png", 'to_level2', 250, 176))
        else :
            self.groupSprites.add(Decoration(530, 200, IMAGE_FOLDER+"chiffre2_gris.png", 250, 176))

        if levelManager.assertNiveau(3) :
            self.groupSprites.add(Button(800, 100, IMAGE_FOLDER+"chiffre3.png", 'to_level3', 250, 176))
        else :
            self.groupSprites.add(Decoration(800, 100, IMAGE_FOLDER+"chiffre3_gris.png", 250, 176))

    def react(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            for sprite in self.groupSprites :
                if isinstance(sprite, Button) :
                    sprite.set_triggered(event.pos)

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

class Diff2() :
    def __init__(self) :
        self.groupSprites = pygame.sprite.Group()
        self.groupSprites.add(Button(560, 550, IMAGE_FOLDER+"panneauMP.png", 'to_menu', 188, 116))
        self.groupSprites.add(Button(270, 350, IMAGE_FOLDER+"pagePrecedente.png", 'to_diff1', 100, 100))

        if levelManager.assertNiveau(4) :
            self.groupSprites.add(Button(250, 100, IMAGE_FOLDER+"chiffre4.png", 'to_level4', 250, 176))
        else :
            self.groupSprites.add(Button(250, 100, IMAGE_FOLDER+"chiffre4_gris.png", 'to_level4', 250, 176))
        if levelManager.assertNiveau(5) :
            self.groupSprites.add(Button(530, 200, IMAGE_FOLDER+"chiffre5.png", 'to_level5', 250, 176))
        else :
            self.groupSprites.add(Decoration(530, 200, IMAGE_FOLDER+"chiffre5_gris.png", 250, 176))

        if levelManager.assertNiveau(6) :
            self.groupSprites.add(Button(800, 100, IMAGE_FOLDER+"chiffre6.png", 'to_level6', 250, 176))
        else :
            self.groupSprites.add(Decoration(800, 100, IMAGE_FOLDER+"chiffre6_gris.png", 250, 176))

    def react(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN :
            for sprite in self.groupSprites :
                if isinstance(sprite, Button) :
                    sprite.set_triggered(event.pos)

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

class Game() :
    def __init__(self, background) :
        self.background = background
        self.groupSprites = pygame.sprite.Group()
        self.groupSprites.add(Grid(370, 90, IMAGE_FOLDER+"grilleJ.png", 550)) #grille Joueur
        self.groupSprites.add(Grid(920, 180, IMAGE_FOLDER+"grille.png", 150)) #grille IA
        self.groupSprites.add(Button(1040,40, IMAGE_FOLDER+"close.png", "to_menu", 50, 50)) #bouton fermer
        self.I_down = -1
        self.J_down = -1
        self.I_up = -1
        self.J_up = -1
        self.compteur = 0

    def blits(self, gridJ, gridIA) :
        fenetre.blit(self.background, (140,0))
        fenetre.blit(fond, (0,0))
        fenetre.blit(gridJ.image, (gridJ.rect.x, gridJ.rect.y))
        gridJ.affiche_grille_joueur(fenetre)
        joueur.affiche_jauges(fenetre, (230, 110), (130,12))
        ordi.affiche_jauges(fenetre, (930, 110), (130,12))
        fenetre.blit(gridIA.image, (920, 180))
        gridIA.affiche_grille_ia(fenetre)

    def react(self, event) :
        global isGameEnded
        global isWorld2
        global levelManager
        gridJ = self.groupSprites.sprites()[0]
        gridIA = self.groupSprites.sprites()[1]

        if levelManager.niveau == 3 :
            ennemyCoords = (930,320)
        else :
            ennemyCoords = (930, 380)

        self.blits(gridJ, gridIA)
        joueur.animate(fenetre, (230,400), self.compteur, isWorld2)
        ordi.animate(fenetre, ennemyCoords, self.compteur, isWorld2)

        self.compteur += 1
        #print("compteur ++", self.compteur)


        if event.type == pygame.MOUSEBUTTONDOWN :
            self.I_down, self.J_down  = calcul_i_j(self, channelMouse, buttonPressed, 'down')

            for sprite in self.groupSprites :
                if isinstance(sprite, Button) :
                    sprite.set_triggered(event.pos)

            for sprite in self.groupSprites :
                if isinstance(sprite, Button) :
                    sprite.set_triggered(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            self.I_up, self.J_up  = calcul_i_j(self, channelMouse, buttonPressed, 'up')

            if (self.I_up, self.J_up) in [(self.I_down+1, self.J_down), (self.I_down-1, self.J_down), (self.I_down, self.J_down+1), (self.I_down, self.J_down-1)]:

                itemDown = gridJ.grid[self.I_down][self.J_down]
                itemUp = gridJ.grid[self.I_up][self.J_up]

                switch(itemDown, itemUp, (57,57))
                self.blits(gridJ, gridIA)


                joueur.animate(fenetre, (230,400), self.compteur, isWorld2)
                ordi.animate(fenetre, ennemyCoords, self.compteur, isWorld2)

                pygame.display.flip()
                pygame.time.delay(100)

                if not(gridJ.combo_ligne()) and not(gridJ.combo_colonne()) :
                    channelMouse.play(switchWrong)
                    switch(itemDown, itemUp, (57,57))

                    self.blits(gridJ, gridIA)

                    joueur.animate(fenetre, (230,400), self.compteur, isWorld2)
                    ordi.animate(fenetre, ennemyCoords, self.compteur, isWorld2)

                    pygame.display.flip()
                    pygame.time.delay(100)

                else :
                    channelMouse.play(switchGood)
                    damageIA, poisonIA = joueur.update_defense(gridJ)
                    ordi.update_attack(damageIA, poisonIA)

                    joueur.affiche_jauges(fenetre, (230, 110), (130,12))
                    ordi.affiche_jauges(fenetre, (930, 110), (130,12))
                    pygame.display.flip()

                    if ordi.end_game(fenetre, levelManager) :
                        pygame.time.delay(1000)
                        isGameEnded = True
                        pygame.event.post(pygame.event.Event(WIN))
                        return 0
                    else : update_grilles(fenetre, fond, self.background, joueur, ordi, gridJ, gridIA, (57,57), (18,18), 150, self.compteur, ennemyCoords, isWorld2)

                    if ordi.end_game(fenetre, levelManager) :
                        pygame.time.delay(1000)
                        isGameEnded = True
                        pygame.event.post(pygame.event.Event(WIN))
                        return 0

                    print("difficulté : ",ordi.difficulty)
                    if ordi.difficulty == "hard" :
                        gridIA.switch_ia_hard()
                    elif ordi.difficulty == "normal" :
                        gridIA.switch_ia_normal()
                    else :
                        gridIA.switch_ia_easy()

                    fenetre.blit(gridJ.image, (370,90))
                    gridJ.affiche_grille_joueur(fenetre)
                    fenetre.blit(gridIA.image, (920, 180))
                    gridIA.affiche_grille_ia(fenetre)

                    pygame.display.flip()
                    pygame.time.delay(500)

                    damageJ, poisonJ = ordi.update_defense(gridIA)
                    joueur.update_attack(damageJ, poisonJ)

                    if joueur.end_game(fenetre, levelManager) :
                        pygame.time.delay(1000)
                        isGameEnded = True
                        pygame.event.post(pygame.event.Event(LOSE))
                        return 0
                    else : update_grilles(fenetre, fond, self.background, joueur, ordi, gridJ, gridIA, (57,57), (18,18), 150, self.compteur, ennemyCoords, isWorld2)

                    if joueur.end_game(fenetre, levelManager) :
                        pygame.time.delay(1000)
                        isGameEnded = True
                        pygame.event.post(pygame.event.Event(LOSE))
                        return 0

                    ordi.update_poison()
                    joueur.update_poison()
                    joueur.affiche_jauges(fenetre, (230, 110), (130,12))
                    ordi.affiche_jauges(fenetre, (930, 110), (130,12))
                    gridIA.affiche_grille_ia(fenetre)
                    pygame.display.flip()

                    if joueur.end_game(fenetre, levelManager) :
                        pygame.time.delay(1000)
                        isGameEnded = True
                        pygame.event.post(pygame.event.Event(LOSE))
                        return 0
                    if ordi.end_game(fenetre, levelManager) :
                        pygame.time.delay(1000)
                        isGameEnded = True
                        pygame.event.post(pygame.event.Event(WIN))
                        return 0


                    pygame.display.flip()

            print(">>>>>>>>>>>>>>>")

    def spritePosition(self, index) :
        return self.groupSprites.sprites()[index]

    def draw(self, fenetre) :
        self.groupSprites.update()
        self.groupSprites.draw(fenetre)

################################################################################
#PROGRAMME PRINCIPAL

if __name__ == '__main__' :
    #images du didacticiel
    doritos = pygame.transform.scale(pygame.image.load(IMAGE_FOLDER+"Personnages/Doritos/Doritos-0.png").convert_alpha(), (288/2, 288/2))
    help0 = pygame.image.load(IMAGE_FOLDER+"pageHelp0.png").convert()
    help1 = pygame.image.load(IMAGE_FOLDER+"pageHelp1.png").convert()
    help2 = pygame.image.load(IMAGE_FOLDER+"pageHelp2.png").convert()
    help3 = pygame.image.load(IMAGE_FOLDER+"pageHelp3.png").convert()
    tutorial = [help0, help1, help2, help3]


    #Chargement des fonds=========================================================
    backgroundM1 = pygame.image.load(IMAGE_FOLDER+"backgroundM1.jpg").convert_alpha()
    backgroundInterfaceM1 = pygame.image.load(IMAGE_FOLDER+"backgroundInterfaceM1.jpg").convert()

    backgroundM2 = pygame.image.load(IMAGE_FOLDER+"backgroundM2.jpg").convert_alpha()
    backgroundInterfaceM2 = pygame.image.load(IMAGE_FOLDER+"backgroundInterfaceM2.jpg").convert()

    fond = pygame.image.load(IMAGE_FOLDER+"borne-arcade.png").convert_alpha()
    win = pygame.image.load(IMAGE_FOLDER+"win.png").convert_alpha()
    lose = pygame.image.load(IMAGE_FOLDER+"lose.png").convert_alpha()
    fenetre.blit(backgroundM1, (140, 0))
    fenetre.blit(fond, (0, 0))

    #Initialisation de l'affichage==============================================
    frame = Start()
    background = backgroundM1
    backgroundInterface = backgroundInterfaceM1

    #Boucle infinie=============================================================
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == MENU_PRINCIPAL :
                if isWorld2 :
                    background = backgroundM2
                else :
                    background = backgroundM1

                if isGameEnded and not isMuted :
                    channelMusic.play(musiqueSTA,999)

                isGameEnded = False
                frame = Menu()
                fenetre.blit(background, (140, 0))
                fenetre.blit(fond, (0, 0))


            elif event.type == OPTIONS :
                if isWorld2 :
                    backgroundInterface = backgroundInterfaceM2
                else :
                    backgroundInterface = backgroundInterfaceM1
                frame = Options()
                fenetre.blit(backgroundInterface, (140, 0))
                fenetre.blit(fond, (0, 0))


            elif event.type == CHOIX_DIFF1 :
                if isGameEnded and not isMuted :
                    channelMusic.play(musiqueSTA,999)

                isGameEnded = False
                backgroundInterface = backgroundInterfaceM1
                frame = Diff()
                fenetre.blit(backgroundInterface, (140, 0))
                fenetre.blit(fond, (0, 0))

            elif event.type == CHOIX_DIFF2 :
                if isGameEnded and not isMuted :
                    channelMusic.play(musiqueSTA,999)

                isGameEnded = False
                backgroundInterface = backgroundInterfaceM2
                frame = Diff2()
                fenetre.blit(backgroundInterface, (140, 0))
                fenetre.blit(fond, (0, 0))


            elif event.type == NEW_GAME:

                """PARTIE A EQUILIBRER"""
                if levelManager.niveau == 1 :
                    joueur = entity.Entity("doritos", "left", True, 30, 30, 5)
                    ordi = entity.Entity("chienB", "right", False, 15, 15, 3)
                if levelManager.niveau == 2 :
                    joueur = entity.Entity("doritos",  "left", True, 20, 25, 5)
                    ordi = entity.Entity("chienR", "right", False, 20, 20, 3, "normal")
                if levelManager.niveau == 3 :
                    joueur = entity.Entity("doritos", "left",  True, 20, 20, 5)
                    ordi = entity.Entity("requin", "right", False, 20, 20, 5, "normal")
                if levelManager.niveau == 4 :
                    joueur = entity.Entity("doritos", "left", True, 20, 20, 5)
                    ordi = entity.Entity("chienB", "right", False, 20, 20, 3, "hard")
                if levelManager.niveau == 5 :
                    joueur = entity.Entity("doritos", "left", True, 20, 20, 5)
                    ordi = entity.Entity("chienR", "right", False, 20, 20, 4, "hard")
                if levelManager.niveau == 6 :
                    joueur = entity.Entity("doritos", "left",  True, 20, 20, 5)
                    ordi = entity.Entity("chienA", "right", False, 30, 30, 5, "hard")

                if levelManager.niveau >= 4 :
                    background = backgroundM2
                else :
                    background = backgroundM1

                fenetre.blit(background, (140, 0))
                fenetre.blit(fond, (0, 0))
                frame = Game(background)

                frame.groupSprites.sprites()[0] = 0
                frame.groupSprites.sprites()[0] = Grid(390, 110, IMAGE_FOLDER+"grilleJ.png", 550)
                frame.groupSprites.sprites()[0].remplir_grille((57,57))
                frame.groupSprites.sprites()[0].affiche_grille_console()

                frame.groupSprites.sprites()[1] = 0
                frame.groupSprites.sprites()[1] = Grid(920, 180, IMAGE_FOLDER+"grille.png", 150)
                frame.groupSprites.sprites()[1].remplir_grille((18,18))

                joueur.affiche_jauges(fenetre, (230, 110), (130,12))
                ordi.affiche_jauges(fenetre, (930, 110), (130,12))
                frame.compteur += 1

            elif event.type == RESET_GAME:
                fenetre.blit(background, (140, 0))
                fenetre.blit(fond, (0, 0))
                frame = Menu()

            elif event.type == WIN :
                frame = EndGame()
                channelMusic.play(victory)
                fenetre.blit(win, (0, 0))
                fenetre.blit(fond, (0, 0))

            elif event.type == LOSE :
                frame = EndGame()
                channelMusic.play(switchWrong)
                fenetre.blit(lose, (0, 0))
                fenetre.blit(fond, (0, 0))

            elif event.type == HELP :
                fenetre.blit(fond, (0, 0))
                frame = Help(tutorial, fond)

            frame.react(event)

        frame.draw(fenetre)
        if isinstance(frame, Game) :
            pygame.event.post(pygame.event.Event(pygame.locals.KEYDOWN, unicode="a", key=pygame.locals.K_a, mod=pygame.locals.KMOD_NONE))
            pygame.time.delay(100)
            frame.groupSprites.sprites()[1].affiche_grille_ia(fenetre)

        pygame.display.flip()

################################################################################
