

import numpy as np
import csv

class Chairlift:
    def __init__(self):
        self.__vitesse = 0
        self.__nombreDeChaise = 0
        self.__nombreDePersonnesParChaise = 0
        self.__longueurDuTrajet = 0
        self.__tempsEmbarquement = 0
        self.__tempsDebarquement = 0

        self.__parametreObserver = "none"


    def definirVitesse(self, vitesse):
        if vitesse >= 0:
            self.__vitesse = vitesse
            return True
        else:
            return False

    def definirNombreDeChaise(self,nombreDeChaise):
        if nombreDeChaise >= 0:
            self.__nombreDeChaise = nombreDeChaise
            return True
        else:
            return False

    def definirLongueurDuTrajet(self, longueurDuTrajet):
        if longueurDuTrajet > 0:
            self.__longueurDuTrajet = longueurDuTrajet
            return True
        else:
            return False

    def definirTempsEmbarquement(self, tempsEmbarquement):
        if tempsEmbarquement >= 0:
            self.__tempsEmbarquement = tempsEmbarquement
            return True
        else:
            return False

    def definirTempsDebarquement(self,tempsDebarquement):
        if tempsDebarquement >= 0:
            self.__tempsDebarquement = tempsDebarquement
            return True
        else:
            return False

    def definirNombreDePersonnesParChaise(self, nombreDePersonnesParChaise):
        if nombreDePersonnesParChaise >= 0:
            self.__nombreDePersonnesParChaise = nombreDePersonnesParChaise
            return True
        else:
            return False
        
    def definirParametreObserver(self, parametreObserver):
        if parametreObserver in ["vitesse", "nombreDeChaise", "longueurDuTrajet", "tempsEmbarquement", "tempsDebarquement", "nombreDePersonnesParChaise", "none"]:
            self.__parametreObserver = parametreObserver
            return True
        else:
            return False

    def calculerTempsTrajet(self):
        if self.__vitesse == 0:
            return 0
        tempsTrajet = self.__longueurDuTrajet / self.__vitesse
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
                return int((3600 / (2*(self.__longueurDuTrajet/valeurParametre) + self.__tempsEmbarquement + self.__tempsDebarquement)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
            
            elif self.__parametreObserver == "nombreDeChaise":
                return int((3600 / (2*(self.__longueurDuTrajet/self.__vitesse) + self.__tempsEmbarquement + self.__tempsDebarquement)) * valeurParametre * self.__nombreDePersonnesParChaise)
            
            elif self.__parametreObserver == "longueurDuTrajet":
                return int((3600 / (2*(valeurParametre/self.__vitesse) + self.__tempsEmbarquement + self.__tempsDebarquement)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
            
            
            elif self.__parametreObserver == "nombreDePersonnesParChaise":
                return int((3600 / (2*(self.__longueurDuTrajet/self.__vitesse) + self.__tempsEmbarquement + self.__tempsDebarquement)) * self.__nombreDeChaise * valeurParametre)
            elif self.__parametreObserver == "tempsEmbarquement":
                return int((3600 / (2*(self.__longueurDuTrajet/self.__vitesse) + valeurParametre + self.__tempsDebarquement)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
                                
            elif self.__parametreObserver == "tempsDebarquement":
                return int((3600 / (2*(self.__longueurDuTrajet/self.__vitesse) + self.__tempsEmbarquement + valeurParametre)) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise)
                        
            else:
                return 0
        except (ZeroDivisionError, TypeError, ValueError, OverflowError):
            return 0

    def obtenirDonneesGraphique(self, resolution, minimum, maximum):
        abscisses = np.linspace(minimum, maximum, num=resolution)
        ordonnees = np.array([
            self.calculerNombreDePersonnesParametreManquant(valeur)
            for valeur in abscisses
        ])
    
        return np.column_stack((abscisses, ordonnees))

    def obtenirParametreObserver(self):
        return self.__parametreObserver
    
    def exporterVersCSV(self, chemin):
        ligne = [
            ("vitesse", self.__vitesse),
            ("nombreDeChaise", self.__nombreDeChaise),
            ("nombreDePersonnesParChaise", self.__nombreDePersonnesParChaise),
            ("longueurDuTrajet", self.__longueurDuTrajet),
            ("tempsEmbarquement", self.__tempsEmbarquement),
            ("tempsDebarquement", self.__tempsDebarquement),
            ("parametreObserver", self.__parametreObserver),
        ]

        with open(chemin, "w", newline="", encoding="utf-8") as fichier:
            redacteur = csv.writer(fichier)
            redacteur.writerow(["Parametre", "Valeur"])   # en-tête
            redacteur.writerows(ligne)


    def importerDepuisCSV(self, chemin):
        try:
            definisseurs = {
                "vitesse": (self.definirVitesse, float),
                "nombreDeChaise": (self.definirNombreDeChaise, int),
                "nombreDePersonnesParChaise": (self.definirNombreDePersonnesParChaise, int),
                "longueurDuTrajet": (self.definirLongueurDuTrajet, float),
                "tempsEmbarquement": (self.definirTempsEmbarquement, float),
                "tempsDebarquement": (self.definirTempsDebarquement, float),
                "parametreObserver": (self.definirParametreObserver, str),
            }

            with open(chemin, newline="", encoding="utf-8") as fichier:
                for ligne in csv.DictReader(fichier):
                    nom = ligne["Parametre"]
                    if nom not in definisseurs:
                        continue                      # ligne inconnue : on l'ignore
                    definisseur, convertir = definisseurs[nom]
                    if not definisseur(convertir(ligne["Valeur"])):
                        raise ValueError(f"Valeur invalide pour {nom} : {ligne['Valeur']}")
        except (OSError, ValueError, KeyError) as error:
            print("Chargement impossible :", error)

    def tester(self):
        print("input vitesse: ")
        vitesse = float(input())
        self.definirVitesse(vitesse)

        print("input nombre de chaises: ")
        nombreDeChaise = int(input())
        self.definirNombreDeChaise(nombreDeChaise)

        print("input longueur du trajet: ")
        longueurDuTrajet = float(input())
        self.definirLongueurDuTrajet(longueurDuTrajet)

        print("input temps d'embarquement: ")
        tempsEmbarquement = float(input())
        self.definirTempsEmbarquement(tempsEmbarquement)

        print("input temps de débarquement: ")
        tempsDebarquement = float(input())
        self.definirTempsDebarquement(tempsDebarquement)

        print("input nombre de personnes par chaise: ")
        nombreDePersonnesParChaise = int(input())
        self.definirNombreDePersonnesParChaise(nombreDePersonnesParChaise)

        print(self)
        print(f"Nombre de personnes par heure: {self.calculerNombreDePersonnesParHeure()}")


    def __str__(self):
        return f"Vitesse: {self.__vitesse}, Nombre de chaises: {self.__nombreDeChaise}, Longueur du trajet: {self.__longueurDuTrajet}, Temps d'embarquement: {self.__tempsEmbarquement}, Temps de débarquement: {self.__tempsDebarquement}, Nombre de personnes par chaise: {self.__nombreDePersonnesParChaise}, Temps de trajet: {self.calculerTempsTrajet()}, Temps de monter: {self.calculerTempsDeMonter()}, Temps de cycle: {self.calculerTempsDeCycle()}"

#mon_chairlift = Chairlift()
#mon_chairlift.tester()
#mon_chairlift.definirParametreObserver("vitesse")
#mon_chairlift.obtenirDonneesGraphique(11,0,10)
#chemin = filedialog.asksaveasfilename(defaultextension=".csv",
                                    #filetypes=[("Fichiers CSV", "*.csv")])
#if chemin:
    #self.chairlift.exporterVersCSV(chemin)
#mon_chairlift.exporterVersCSV("parametres.csv")
#mon_chairlift.importerDepuisCSV("parametres.csv")
