import numpy as np
import random
from Chairlift import Chairlift

class Energy:

    def __init__(self, chairlift):
        self.__chairlift = chairlift
        self.__energie = 0 #J
        self.__gravity = 9.81 #m/s^2
        self.__singleChairWeight = 0 #kg
        self.__weightDic = {0:0,1:45.35924,2:68.03886,3:79.37866,4:226.7962,5:260,6:589.6701,7:700,8:1000}


    def poidsC(self):
        size = self.__chairlift.obtenirNombreDePersonnesParChaise()
        self.__singleChairWeight = self.__weightDic[size]
        return self.__singleChairWeight

    def poidsP(self):
        poidsPossible = [43,44,45,46,47,48,49,50]
        nbPersonne = self.__chairlift.calculerNombreDePersonnesParHeure()
        if nbPersonne == 0:
            return 0
        else: 
            poidsTotal = 0
            for i in range(nbPersonne):
                poidsTotal += (poidsPossible + random.randint(0,107))
            return poidsTotal
