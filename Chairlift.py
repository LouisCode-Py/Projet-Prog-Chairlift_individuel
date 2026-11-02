

import numpy as np
import csv

class Chairlift:
    def __init__(self):
        self.__vitesse = 0
        self.__nombreDeChaise = 0
        self.__nombreDePersonnesParChaise = 0
        self.__longeurDuTrajet = 0
        self.__tempsEmbarquement = 0
        self.__tempsDebarquement = 0

        self.__parametreObserver = "none"


    def setVitesse(self, vitesse):
        if vitesse >= 0:
            self.__vitesse = vitesse
            return True
        else:
            return False

    def setNombreDeChaise(self,nombreDeChaise):
        if nombreDeChaise >= 0:
            self.__nombreDeChaise = nombreDeChaise
            return True
        else:
            return False

    def setLongeurDuTrajet(self,longeurDuTrajet):
        if longeurDuTrajet > 0:
            self.__longeurDuTrajet = longeurDuTrajet
            return True
        else:
            return False

    def setTempsEmbarquement(self, tempsEmbarquement):
        if tempsEmbarquement >= 0:
            self.__tempsEmbarquement = tempsEmbarquement
            return True
        else:
            return False

    def setTempsDebarquement(self,tempsDebarquement):
        if tempsDebarquement >= 0:
            self.__tempsDebarquement = tempsDebarquement
            return True
        else:
            return False

    def setNombreDePersonnesParChaise(self, nombreDePersonnesParChaise):
        if nombreDePersonnesParChaise >= 0:
            self.__nombreDePersonnesParChaise = nombreDePersonnesParChaise
            return True
        else:
            return False
        
    def setParametreObserver(self, parametreObserver):
        if parametreObserver in ["vitesse", "nombreDeChaise", "longeurDuTrajet", "tempsEmbarquement", "tempsDebarquement", "nombreDePersonnesParChaise", "none"]:
            self.__parametreObserver = parametreObserver
            return True
        else:
            return False

    def calculerTempsTrajet(self):
        if self.__vitesse == 0:
            return 0
        tempsTrajet = self.__longeurDuTrajet / self.__vitesse
        return tempsTrajet
    

    def calculerTempsDeCycle(self):
        tempsTrajet = self.calculerTempsTrajet()
        if tempsTrajet == 0:
            return 0
        tempsDeCycle = 2*tempsTrajet + self.__tempsEmbarquement + self.__tempsDebarquement
        return tempsDeCycle

    def calculerNombreDePersonnesParHeure(self):
        tempsDeCycle = self.calculerTempsDeCycle()
        if tempsDeCycle == 0:
            print("fuck")
            return 0
        nombreDePersonnesParHeure = (3600 / tempsDeCycle) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise
        print(nombreDePersonnesParHeure)
        return int(nombreDePersonnesParHeure)
    
    def calculerNombreDePersonnesParametreManquant(self, valeurParametre):
        try:
            if self.__parametreObserver == "vitesse":
                return int((3600 / (2*(self.__longeurDuTrajet/valeurParametre) + self.__tempsEmbarquement + self.__tempsDebarquement)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
            
            elif self.__parametreObserver == "nombreDeChaise":
                return int((3600 / (2*(self.__longeurDuTrajet/self.__vitesse) + self.__tempsEmbarquement + self.__tempsDebarquement)) * valeurParametre * self.__nombreDePersonnesParChaise)
            
            elif self.__parametreObserver == "longeurDuTrajet":
                return int((3600 / (2*(valeurParametre/self.__vitesse) + self.__tempsEmbarquement + self.__tempsDebarquement)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
            
            
            elif self.__parametreObserver == "nombreDePersonnesParChaise":
                return int((3600 / (2*(self.__longeurDuTrajet/self.__vitesse) + self.__tempsEmbarquement + self.__tempsDebarquement)) * self.__nombreDeChaise * valeurParametre)
            elif self.__parametreObserver == "tempsEmbarquement":
                return int((3600 / (2*(self.__longeurDuTrajet/self.__vitesse) + valeurParametre + self.__tempsDebarquement)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
                                
            elif self.__parametreObserver == "tempsDebarquement":
                return int((3600 / (2*(self.__longeurDuTrajet/self.__vitesse) + self.__tempsEmbarquement + valeurParametre)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
                        
            else:
                return 0
        except (ZeroDivisionError, TypeError, ValueError, OverflowError):
            return 0

    def getGraphData(self, resolution, min, max):
        x = np.linspace(min, max, num=resolution)
        y = np.array([
            self.calculerNombreDePersonnesParametreManquant(value)
            for value in x
        ])
    
        return np.column_stack((x, y))

    def getParametreObserver(self):
        return self.__parametreObserver
    
    def exportToCSV(self, path):
        ligne = [
            ("vitesse", self.__vitesse),
            ("nombreDeChaise", self.__nombreDeChaise),
            ("nombreDePersonnesParChaise", self.__nombreDePersonnesParChaise),
            ("longeurDuTrajet", self.__longeurDuTrajet),
            ("tempsEmbarquement", self.__tempsEmbarquement),
            ("tempsDebarquement", self.__tempsDebarquement),
            ("parametreObserver", self.__parametreObserver),
        ]

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Parametre", "Valeur"])   # en-tête
            writer.writerows(ligne)


    def importFromCSV(self, path):
        try:
            setters = {
                "vitesse": (self.setVitesse, float),
                "nombreDeChaise": (self.setNombreDeChaise, int),
                "nombreDePersonnesParChaise": (self.setNombreDePersonnesParChaise, int),
                "longeurDuTrajet": (self.setLongeurDuTrajet, float),
                "tempsEmbarquement": (self.setTempsEmbarquement, float),
                "tempsDebarquement": (self.setTempsDebarquement, float),
                "parametreObserver": (self.setParametreObserver, str),
            }

            with open(path, newline="", encoding="utf-8") as f:
                for ligne in csv.DictReader(f):
                    nom = ligne["Parametre"]
                    if nom not in setters:
                        continue                      # ligne inconnue : on l'ignore
                    setter, convert = setters[nom]
                    if not setter(convert(ligne["Valeur"])):
                        raise ValueError(f"Valeur invalide pour {nom} : {ligne['Valeur']}")
        except (OSError, ValueError, KeyError) as error:
            print("Chargement impossible :", error)

    def test(self):
        print("input vitesse: ")
        vitesse = float(input())
        self.setVitesse(vitesse)

        print("input nombre de chaises: ")
        nombreDeChaise = int(input())
        self.setNombreDeChaise(nombreDeChaise)

        print("input longueur du trajet: ")
        longeurDuTrajet = float(input())
        self.setLongeurDuTrajet(longeurDuTrajet)

        print("input temps d'embarquement: ")
        tempsEmbarquement = float(input())
        self.setTempsEmbarquement(tempsEmbarquement)

        print("input temps de débarquement: ")
        tempsDebarquement = float(input())
        self.setTempsDebarquement(tempsDebarquement)

        print("input nombre de personnes par chaise: ")
        nombreDePersonnesParChaise = int(input())
        self.setNombreDePersonnesParChaise(nombreDePersonnesParChaise)

        print(self)
        print(f"Nombre de personnes par heure: {self.calculerNombreDePersonnesParHeure()}")


    def __str__(self):
        return f"Vitesse: {self.__vitesse}, Nombre de chaises: {self.__nombreDeChaise}, Longueur du trajet: {self.__longeurDuTrajet}, Temps d'embarquement: {self.__tempsEmbarquement}, Temps de débarquement: {self.__tempsDebarquement}, Nombre de personnes par chaise: {self.__nombreDePersonnesParChaise}, Temps de trajet: {self.calculerTempsTrajet()}, Temps de monter: {self.calculerTempsDeMonter()}, Temps de cycle: {self.calculerTempsDeCycle()}"

#mon_chairlift = Chairlift()
#mon_chairlift.test()
#mon_chairlift.setParametreObserver("vitesse")
#mon_chairlift.getGraphData(11,0,10)
#path = filedialog.asksaveasfilename(defaultextension=".csv",
                                    #filetypes=[("Fichiers CSV", "*.csv")])
#if path:
    #self.chairlift.exportToCSV(path)
#mon_chairlift.exportToCSV("parametres.csv")
#mon_chairlift.importFromCSV("parametres.csv")
