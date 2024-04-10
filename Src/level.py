################################################################################
#CLASSE LEVEL

class Level():

    #Initialisation=============================================================
    def __init__(self, progression): #initialiser le manager de niveau
        self.niveau = 1
        self.totalLevel = 6
        self.unlockedLevel = progression
        self.name = ""

    #Tests=====================================================================
    def assertNiveau(self, val) :
        return val <= self.unlockedLevel and self.unlockedLevel <= self.totalLevel
