
import numpy as np
import csv

class Chairlift:
    def __init__(self):
        self.__vitesse = 0 # m/s
        self.__nombreDeChaise = 0
        self.__nombreDePersonnesParChaise = 0
        self.__longueurDuTrajet = 0 # m
        self.__tempsEmbarquement = 0 # s
        self.__tempsDebarquement = 0 # s
        self.__angleInclinaison = 0 # rad

        self.__parametreObserver = "none"

    #setter pour la vitesse de deplacement du chairlift
    def definirVitesse(self, vitesse):
        if vitesse >= 0:
            self.__vitesse = vitesse
            return True
        else:
            return False

    #setter pour le nombre de chaises du chairlift
    def definirNombreDeChaise(self, nombreDeChaise):
        if nombreDeChaise >= 0:
            self.__nombreDeChaise = nombreDeChaise
            return True
        else:
            return False
    #setter pour la longueur du trajet du chairlift
    def definirLongueurDuTrajet(self, longueurDuTrajet):
        if longueurDuTrajet > 0:
            self.__longueurDuTrajet = longueurDuTrajet
            return True
        else:
            return False

    #setter pour le temps d'embarquement du chairlift
    def definirTempsEmbarquement(self, tempsEmbarquement):
        if tempsEmbarquement >= 0:
            self.__tempsEmbarquement = tempsEmbarquement
            return True
        else:
            return False
    #setter pour le temps de débarquement du chairlift
    def definirTempsDebarquement(self, tempsDebarquement):
        if tempsDebarquement >= 0:
            self.__tempsDebarquement = tempsDebarquement
            return True
        else:
            return False

    #setter pour le nombre de personnes par chaise du chairlift
    def definirNombreDePersonnesParChaise(self, nombreDePersonnesParChaise):
        if nombreDePersonnesParChaise >= 0:
            self.__nombreDePersonnesParChaise = nombreDePersonnesParChaise
            return True
        else:
            return False
    #setter pour le paramètre observé du chairlift    
    def definirParametreObserver(self, parametreObserver):
        if parametreObserver in ["vitesse", "nombreDeChaise", "longueurDuTrajet", "tempsEmbarquement", "tempsDebarquement", "nombreDePersonnesParChaise", "none"]:
            self.__parametreObserver = parametreObserver
            return True
        else:
            return False
    # Getters des différents paramètres, convertis dans le bon type
    def obtenirVitesse(self):
        return round(float(self.__vitesse), 1)

    def obtenirNombreDeChaise(self):
        return int(self.__nombreDeChaise)

    def obtenirNombreDePersonnesParChaise(self):
        return int(self.__nombreDePersonnesParChaise)

    def obtenirLongueurDuTrajet(self):
        return int(self.__longueurDuTrajet)

    def obtenirTempsEmbarquement(self):
        return int(self.__tempsEmbarquement)

    def obtenirTempsDebarquement(self):
        return int(self.__tempsDebarquement)

    #calculer le temps de trajet du chairlift
    def calculerTempsTrajet(self):
        if self.__vitesse == 0:
            return 0
        tempsTrajet = self.__longueurDuTrajet / self.__vitesse
        return tempsTrajet
    
    #calculer le temps de cycle pour une chaise du chairlift, qui est le temps de trajet aller-retour plus le temps d'embarquement et de débarquement
    def calculerTempsDeCycle(self):
        tempsTrajet = self.calculerTempsTrajet()
        if tempsTrajet == 0:
            return 0
        tempsDeCycle = 2*tempsTrajet + self.__tempsEmbarquement + self.__tempsDebarquement
        return tempsDeCycle

    #calculer le nombre de personnes par heure du chairlift, qui est le nombre de personnes transportées par heure en fonction du temps de cycle, du nombre de chaises et de personnes par chaise
    def calculerNombreDePersonnesParHeure(self):
        tempsDeCycle = self.calculerTempsDeCycle()
        if tempsDeCycle == 0:
            return 0
        nombreDePersonnesParHeure = (3600 / tempsDeCycle) * self.__nombreDeChaise * self.__nombreDePersonnesParChaise

        return int(nombreDePersonnesParHeure) #client/heure

    #calculer le nombre de personnes par heure en fonction du paramètre observé et de la valeur du paramètre manquant. Utile pour la génération de graphique. Le paramètre observé est celui qui est modifié dans le graphique.
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

    #retourne les données pour le graphique en fonction du paramètre observé et de la résolution, minimum et maximum du paramètre observé. Utile pour la génération de graphique.
    def obtenirDonneesGraphique(self, resolution, minimum, maximum):
        abscisses = np.linspace(minimum, maximum, num=resolution)
        ordonnees = np.array([
            self.calculerNombreDePersonnesParametreManquant(valeur)
            for valeur in abscisses
        ])
    
        return np.column_stack((abscisses, ordonnees))

    #getter pour le paramètre observé du chairlift
    def obtenirParametreObserver(self):
        return self.__parametreObserver

    #exporter les paramètres du chairlift vers un fichier CSV
    def exporterVersCSV(self, chemin):
        ligne = [
            ("vitesse", round(float(self.__vitesse), 1)),
            ("nombreDeChaise", int(self.__nombreDeChaise)),
            ("nombreDePersonnesParChaise", int(self.__nombreDePersonnesParChaise)),
            ("longueurDuTrajet", int(self.__longueurDuTrajet)),
            ("tempsEmbarquement", int(self.__tempsEmbarquement)),
            ("tempsDebarquement", int(self.__tempsDebarquement)),
        ]

        with open(chemin, "w", newline="", encoding="utf-8") as fichier:
            redacteur = csv.writer(fichier)
            redacteur.writerow(["Parametre", "Valeur"])   # en-tête
            redacteur.writerows(ligne)

    #importer les paramètres du chairlift depuis un fichier CSV
    def importerDepuisCSV(self, chemin):
        try:
            definisseurs = {
                "vitesse": (self.definirVitesse, float),
                "nombreDeChaise": (self.definirNombreDeChaise, int),
                "nombreDePersonnesParChaise": (self.definirNombreDePersonnesParChaise, int),
                "longueurDuTrajet": (self.definirLongueurDuTrajet, int),
                "tempsEmbarquement": (self.definirTempsEmbarquement, int),
                "tempsDebarquement": (self.definirTempsDebarquement, int),
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

    #fonction pour tester le fonctionnement de la classe
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

    #utile pour le debug, permet d'afficher les parametres du chairlift et les resultats des calculs
    def __str__(self):
        return f"Vitesse: {self.__vitesse}, Nombre de chaises: {self.__nombreDeChaise}, Longueur du trajet: {self.__longueurDuTrajet}, Temps d'embarquement: {self.__tempsEmbarquement}, Temps de débarquement: {self.__tempsDebarquement}, Nombre de personnes par chaise: {self.__nombreDePersonnesParChaise}, Temps de trajet: {self.calculerTempsTrajet()}, Temps de cycle: {self.calculerTempsDeCycle()}"

