import numpy as np
import random
from Chairlift import Chairlift

class Energy:

    #PAR HEURE, POIDS CHAISE OK, POIDS PERSONNES OK, POIDS CABLE (M/KG) OK

    def __init__(self, chairlift):
        self.__chairlift = chairlift
        self.__gravity = 9.81 # m/s^2
        self.__singleChairWeight = 0 # kg
        self.__poidsChaiseTot = 0 # kg
        self.__poidsPersonneTot = 0 # kg
        self.__poidsCabletot = 0 # kg/m

        self.__energieLift = 0 # J
        self.__powerLift = 0 # watts
        self.__powerFriction = 0 # watt
        self.__energieTot = 0 # W/h

    # Calcule poids des chaises individuelles
    def poidsC(self):
        weightChairDic = {0:0,1:45.35924,2:68.03886,3:79.37866,4:226.7962,5:260,6:589.6701,7:700,8:1000}
        size = self.__chairlift.obtenirNombreDePersonnesParChaise()
        self.__singleChairWeight = weightChairDic[size]
        return self.__singleChairWeight

    # Calcule poids total des chaises
    def poidsChaiseT(self):
        self.__poidsChaiseTot = (self.__singleChairWeight*self.__chairlift.obtenirNombreDeChaise())
        return self.__poidsChaiseTot

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
            self.__poidsPersonneTot = poidsTotal
            return self.__poidsPersonneTot

    def poidsCable(self):
        #kg/m
        weightCableDic = {0:0,1:6.1,2:7.3,3:7.8,4:8.4,5:9,6:10.7,7:11.6,8:12.4}
        size = self.__chairlift.obtenirNombreDePersonnesParChaise()
        cableWeight = weightCableDic[size]
        return cableWeight

    def poidsCableTotal(self):
        self.__poidsCabletot = (self.poidsCable() * (2*self.__chairlift.obtenirLongueurDuTrajet()))
        return self.__poidsCabletot

    # Calculer energie/h en fonction du poids, ajouter angle inclinaison dans parametres de Chairlift.py
    # E_lift = mgh => e = mt * g * (cableLength * angle inclinaison theta)
    # P_lift = E_lift /3600 (watts)
    # P_friction = μ × m_on_line × g × cos θ × v
    ## Efficiency
    # P_electric = (P_lift + P_friction) / η η ≈ 0.8 to 0.9
    # Total energy = P_electric × operating time
    # K non necessaire au long terme, juste utiliser au depart du chairlift

    def energy_lift(self):
        masseTot = self.__poidsCabletot + self.__poidsPersonneTot + self.__poidsChaiseTot
        self.__energieLift = masseTot * self.__gravity * ((2*self.__chairlift.obtenirLongueurDuTrajet())*np.sin(self.__chairlift.obtenirAngleInclinaison())) # implementer obtenir angle inclinaison
        return self.__energieLift

    def power_lift(self):
        self.__powerLift = self.__energieLift / 3600
        return self.__powerLift


    def power_friction(self):
        # frottement constant a 0.25
        masseSurCable = self.__poidsChaiseTot + self.__poidsPersonneTot
        self.__powerFriction = 0.25 * masseSurCable * self.__gravity * np.cos(self.__chairlift.obtenirAngleInclinaison()) * self.__chairlift.obtenirVitesse()
        return self.__powerFriction


    def power_electric(self):
        self.__powerElectric = (self.__powerLift + self.__powerFriction) / 0.8
        return self.__powerElectric


    def total_energy(self):
        self.__energieTot = self.__powerElectric * 12
        return self.__energieTot