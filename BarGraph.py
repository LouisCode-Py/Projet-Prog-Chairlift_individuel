
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from Chairlift import Chairlift


class BarGraph(tk.Frame):

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

# Fonction de changement de données affichées
    def mise_a_jour(self):

        # Trouver le paramètre observé
        param_obs = self.modele.obtenirParametreObserver()
        