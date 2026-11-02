
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from Chairlift import Chairlift
#TODO COMMENTER AVANT D'ENVOYER

## commencer par prendre donnees ncecessaire a la creation du graphique dans __init__



class GraphControl(tk.Frame):

    def __init__(self,parent,modele):
        super().__init__(parent)
        self.modele = modele
        self.creation_image()

#fonction pour creer une image
    def creation_image(self):
        self.figure = Figure(figsize=(6, 3.5))
        ##ligne inutile, veux dire ligne 1, colonne 1, graphique selectionner 1, changer en fonction de ou l'image doit s'afficher
        self.axis = self.figure.add_subplot(111)
        ##transforme matplotlib image en image utilisable par tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        ##extrait image avec get_tk_widget et place l'image avec .pack
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


#fonction pour que l'image puisse changer lors de la modification des parametres
    def mise_a_jour_image(self,titrey="Personnes par heure"):
        ## DOIT PRENDRE EN PARAMETRE FONCTION QUI VERIFIER SI DONNÉES ONT CHARGER CORRECTEMENT??
        ## Attribu titre doit etre modifiable -- quel sont les titres possible???, faire comme avec titrex
        
        donnee = self.modele.obtenirDonneesGraphique(11,0,10)

        ##Creation dictionnaire des noms d'axe des x possible et accesseur de parametre ajouter
        parametre_obs = self.modele.obtenirParametreObserver()

        #Creation attribut du titre de l'axe des x
        titrex_dic ={"vitesse":["Vitesse"], "nombreDeChaise":["Nombre de chaise"], "longueurDuTrajet":["Longueur du trajet"],
                  "tempsEmbarquement":["Temps embarquement"], "tempsDebarquement":["Temps debarquement"], "nombreDePersonnesParChaise":["Personnes par chaise"], "none":["Vide"]}
        #Creation attribut du titre de graphique
        titre_dic ={"vitesse":["Débit selon la vitesse"], "nombreDeChaise":["Débit selon les chaises"], "longueurDuTrajet":["Débit selon la longueur"],
                    "tempsEmbarquement":["Débit selon l'embarquement"],"tempsDebarquement":["Débit selon débarquement"],"nombreDePersonnesParChaise":["Débit selon la capacité par chaise"],
                    "none":["Aucun paramètre sélectionné"]}      

        titrex = titrex_dic[parametre_obs][0]
        titre = titre_dic[parametre_obs][0]

        self.axis.clear()
        self.axis.set(title=titre,
                xlabel=titrex, 
                ylabel=titrey)

        if donnee is None or donnee.size == 0:
            self.axis.text(0.5,0.5,"Aucune données", transform=self.axis.transAxes,
                ha="center", va="center")
        else:
            x,y = donnee.T
            self.axis.plot(x, y, label=titre)
            self.axis.legend()

        self.axis.grid(alpha=0.3)
        self.canvas.draw_idle()

#import pandas as pd
#
#root = tk.Tk()
#mon_Chairlift = Chairlift()
#mon_Chairlift.tester()
#mon_Chairlift.definirParametreObserver("vitesse")
#
#g = GraphControl(root, modele=mon_Chairlift)
#
#g.pack(fill="both", expand=True)
#g.mise_a_jour_image("Temps")
#root.mainloop()