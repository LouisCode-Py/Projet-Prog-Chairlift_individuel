
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from Chairlift import Chairlift


class GraphControl(tk.Frame):

    def __init__(self,parent,modele,energy):
        super().__init__(parent)
        self.energy = energy
        self.modele = modele
        self.creation_image()

#fonction pour créer une image
    def creation_image(self):
        self.figure = Figure(figsize=(6, 3.5))
        
        self.axis = self.figure.add_subplot(111)
        #transforme matplotlib image en image utilisable par tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        #extrait image avec get_tk_widget et place l'image avec .pack
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


#fonction pour que l'image puisse changer lors de la modification des parametres
    def mise_a_jour_image(self):
        

        #Création dictionnaire des noms d'axe des x possible et accesseur de paramètre ajouté
        parametre_obs = self.modele.obtenirParametreObserver()
        if parametre_obs != "angleInclinaison":
        
            #Création attribut du titre de l'axe des x
            titrex_dic ={"vitesse":["Vitesse"], "nombreDeChaise":["Nombre de chaise"], "longueurDuTrajet":["Longueur du trajet"],
                      "tempsEmbarquement":["Temps embarquement"], "tempsDebarquement":["Temps debarquement"], "nombreDePersonnesParChaise":["Personnes par chaise"], "none":["Vide"]}
            #Création attribut du titre de graphique
            titre_dic ={"vitesse":["Débit selon la vitesse"], "nombreDeChaise":["Débit selon les chaises"], "longueurDuTrajet":["Débit selon la longueur"],
                        "tempsEmbarquement":["Débit selon l'embarquement"],"tempsDebarquement":["Débit selon débarquement"],"nombreDePersonnesParChaise":["Débit selon la capacité par chaise"],
                        "none":["Aucun paramètre sélectionné"]}

            #Créer dictionnaire des plages de données
            plage_dic = {"vitesse":(80,0.1,8),
                         "nombreDeChaise":(101,0,100),
                         "longueurDuTrajet":(1000,0,3000),
                         "tempsEmbarquement":(31,0,30),
                         "tempsDebarquement":(31,0,30),
                         "nombreDePersonnesParChaise":(9,0,8),
                         "none":(11,0,10)}

            #Créer les titres concrets qui vont être mis dans le graphique
            titrex = titrex_dic[parametre_obs][0]
            titre = titre_dic[parametre_obs][0]

            #Ajouter les bons axes au graphique
            self.axis.clear()
            self.axis.set(title=titre,
                    xlabel=titrex, 
                    ylabel="Personnes par heure")
            resolution, minimum, maximum = plage_dic.get(parametre_obs)
            donnee = self.modele.obtenirDonneesGraphique(resolution,minimum,maximum)

            #Cas où aucun paramètre n'est selectionné
            if donnee is None or donnee.size == 0:
                self.axis.text(0.5,0.5,"Aucune données", transform=self.axis.transAxes,
                    ha="center", va="center")

            else:
                x,y = donnee.T
                self.axis.plot(x, y, label=titre)
                self.axis.legend()

                
        if parametre_obs == "angleInclinaison":
            # Angle plus haut "contre" friction, ce qui fait que moins d'énergie est requise à un plus haut angle
            x=self.energy.listeX()
            y = self.energy.calculerY()
            self.axis.clear()
            self.axis.set(title="Énergie en fonction de l'angle",
                          xlabel="Angle inclinaison (°)",
                          ylabel="Énergie (Wh)")
            self.axis.plot(x, y,label="Énergie (Wh)")
            self.axis.legend()

        self.axis.grid(alpha=0.3)
        self.canvas.draw_idle()