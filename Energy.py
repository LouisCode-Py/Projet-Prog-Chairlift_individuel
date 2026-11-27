import numpy as np
import random
from Chairlift import Chairlift

class Energy:


    # initialisation d'une instance d'Energy
    def __init__(self,parent, chairlift):
        self.__chairlift = chairlift
        self.__gravity = 9.81 # m/s^2
        self.__singleChairWeight = 0 # kg
        self.__poidsChaiseTot = 0 # kg
        self.__poidsPersonneTot = 0 # kg
        self.__poidsCabletot = 0 # kg/m
        self.__energieLift = 0 # J
        self.__powerLift = 0 # watts
        self.__powerFriction = 0 # watt
        self.__energieTot = 0 # Wh

    # Transformer degrees en radians
    def obtenirRad(self):
        self._angle_radians = np.deg2rad(self.__chairlift.obtenirAngleInclinaison())
        return self._angle_radians

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
        nbPersonne = self.__chairlift.calculerNombreDePersonnesParHeure()
        
        poidsTotal = 0
        for i in range(nbPersonne):
            poidsTotal += (43 + random.randint(0,107))
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

    # Méthode pour calculer l'énergie que le remonte pente utilise
    def energy_lift(self):

        hauteur = (self.__chairlift.obtenirLongueurDuTrajet() * np.sin(self._angle_radians))
        
        self.__energieLift =  self.__poidsPersonneTot * self.__gravity * hauteur # implementer obtenir angle inclinaison
        
        return self.__energieLift

    # Méthode pour calculer puissance utilisée par le lift
    def power_lift(self):
        self.__powerLift = self.__energieLift / 3600
        return self.__powerLift


    # Calcule la puissance perdue en friction
    def power_friction(self):
        # frottement constant a 0.25
        vitesse = self.__chairlift.obtenirVitesse()
        if vitesse == 0:
            self.__powerFriction = 0
            return self.__powerFriction
        
        masseSurCable = self.__poidsCabletot + self.__poidsChaiseTot + self.__poidsPersonneTot * self.__chairlift.obtenirLongueurDuTrajet() / (3600 * vitesse)

        self.__powerFriction = 0.25 * masseSurCable * self.__gravity * np.cos(self._angle_radians) * vitesse
        
        return self.__powerFriction


    # Calcule la puissance électrique
    def power_electric(self):
        self.__powerElectric = (self.__powerLift + self.__powerFriction) / 0.8
        return self.__powerElectric


    # Calcule énergie totale
    def total_energy(self):
        self.__energieTot = self.__powerElectric * 12
        return self.__energieTot

    # Crée liste des données en x
    def listeX(self):
        donneesX = []
        for i in range(61):
            donneesX.append(i)
        return donneesX


    # Crée liste des données en y
    def calculerY(self):
        # Initialiser paramètres de base
        angles = self.listeX()
        donneesY = []
        angle_initial = self.__chairlift.obtenirAngleInclinaison()

        # Calculer poids de chaque objet qui change la demande de travail
        self.poidsC()
        self.poidsChaiseT()
        self.poidsP()
        self.poidsCableTotal()

        try:
            for angle in angles:
                self.__chairlift.definirAngle(angle)

                self.obtenirRad()
                self.energy_lift()
                self.power_lift()
                self.power_friction()
                self.power_electric()

                # Ajout de l'énergie a la liste de valeur des y
                donneesY.append(self.total_energy())

        # Fait en sorte que peu importe si le try fonctionne ou non, finally est exécuté (remet l'angle initial en tant qu'angle défini)
        finally:
            self.__chairlift.definirAngle(angle_initial)

        return donneesY


    # Clacule tout
    def calculerTout(self):
        print(self.obtenirRad(),
        self.poidsC(),
        self.poidsChaiseT(),
        self.poidsP(),
        self.poidsCableTotal(),

        self.energy_lift(),
        self.power_lift(),
        self.power_friction(),
        self.power_electric())

        return {
        "puissance_lift": self.__powerLift,
        "puissance_friction": self.__powerFriction,
        "puissance_electrique": self.__powerElectric,
        "energie_totale": self.total_energy(),
    }

    # Calcule le cout avec une moyenne de prix de Wh aux États-Unis
    def coutTotal(self):
        resultats = self.calculerTout()

        dollarPerWattHour = 0.0001427

        return resultats["energie_totale"] * dollarPerWattHour