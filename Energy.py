import numpy as np
import random
from Chairlift import Chairlift

class Energy:

    #PAR HEURE, POIDS CHAISE OK, POIDS PERSONNES OK, POIDS CABLE (M/KG) OK

    def __init__(self, chairlift):
        self.__chairlift = chairlift
        self.__energie = 0 #J
        self.__gravity = 9.81 #m/s^2
        self.__singleChairWeight = 0 #kg
        self.__poidsCabletot = 0 #kg/m

    # Calcule poids des chaises individuelles
    def poidsC(self):
        weightChairDic = {0:0,1:45.35924,2:68.03886,3:79.37866,4:226.7962,5:260,6:589.6701,7:700,8:1000}
        size = self.__chairlift.obtenirNombreDePersonnesParChaise()
        self.__singleChairWeight = weightChairDic[size]
        return self.__singleChairWeight

    # Calcule poids total des chaises
    def poidsChaiseT(self):
        return (self.__singleChairWeight*self.__chairlift.obtenirNombreDeChaise())

    # Calcule poids total des personnes par heure
    def poidsP(self):
        poidsPossible = 43
        nbPersonne = self.__chairlift.calculerNombreDePersonnesParHeure()
        if nbPersonne == 0:
            return 0
        else: 
            poidsTotal = 0
            for i in range(nbPersonne):
                poidsTotal += (poidsPossible + random.randint(0,107))
            return poidsTotal

    def poidsCable(self):
        #kg/m
        weightCableDic = {0:0,1:6.1,2:7.3,3:7.8,4:8.4,5:9,6:10.7,7:11.6,8:12.4}
        size = self.__chairlift.obtenirNombreDePersonnesParChaise()
        cableWeight = weightCableDic[size]
        return cableWeight

    def poidsCableTotal(self):
        self.__poidsCabletot = (self.poidsCable() * (2*self.__chairlift.obtenirLongueurDuTrajet()))
        return self.__poidsCabletot

    # Calculer energie/h en fonction du poids