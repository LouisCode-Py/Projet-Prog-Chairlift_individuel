from Sliders import Sliders
from Chairlift import Chairlift
from GraphControl import GraphControl
from Energy import Energy
from Fiche import Fiche
import tkinter as tk

import customtkinter as ctk

class MainApp(ctk.CTkFrame) :

    def __init__(self,parent) :
        # Initialiser la fenêtre principale
        super().__init__(parent)
       

        # Initialiser, en privé, le Chairlift courant
        self.__chairlift = Chairlift()

        # Initialiser la frame des sliders et autres boutons
        self.grid_rowconfigure(0, weight=1)
        self.sliders = Sliders(self, self.__chairlift, self.mettre_a_jour)
        self.sliders.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=12, pady=12)


        # Initialisation d'une instance d'energie
        self.energy = Energy(self, self.__chairlift)


        # Initialiser la frame du Graphique
        self.graph = GraphControl(self, self.__chairlift,self.energy)
        self.graph.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)


        # Affichage du label du nombre de personnes par heure avec les paramètres courants.
        self.label_nb_personne = ctk.CTkLabel(self, bg_color="white", text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()), text_color="black")
        self.label_nb_personne.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0,12))\


        
        # Bouton de rafraichissement
        #self.bouton_rafraichissement = ctk.CTkButton(self, text="Déselectionner", command=self._rafraichissement)
        #self.bouton_rafraichissement.grid(row=2, column=1, sticky="nsew", padx=12, pady=(3,12))

        # Bouton de déselection
        self.bouton_deselection = ctk.CTkButton(self, text="Déselectionner", command=self._rafraichissement)
        self.bouton_deselection.grid(row=2,column=1,sticky="e",padx=12,pady=(3,12))

        #"""
        # Bouton de calcul d'energie (all)
        self.bouton_energie = ctk.CTkButton(self, text="Calcul Energie", command = self._energie_calcul)
        self.bouton_energie.grid(row=2,column=1,sticky="w",padx=12,pady=(3,12))
        #"""

        # Modifier le poids des différentes colonnes
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        #Configurer les rows du grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # Appeler mettre à jour qui met à jour l'image/le graph
        self.mettre_a_jour()

    # Creer barre de menu pour selectionner entre page d'acceuil et graphe a barres d'energie
    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        selection_menu = tk.Menu(menu_bar,tearoff=0)
        menu_bar.add_cascade(label="Selection", menu=selection_menu)
        ###selection_menu.add_command(label="Page acceuil", command=self.) ## Trouver comment mettre page acceuil comme premiere option

    # Mettre à jour le graphique 
    def mettre_a_jour(self):
        self.graph.mise_a_jour_image()
        
        self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))

        #.label_calcul_energie.configure(text="energie : " + str(self.energy.calculerTout))

    # Commande du bouton de rafraichissement qui recalcule et déselectionne
    def _rafraichissement(self) :
        self.sliders.reset_radio_var()
        
        #self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))

    def _energie_calcul(self):
        self.energy.calculerTout()
        self.energy.total_energy()
        #self.label_calcul_energie.configure(text="Tout energie : " + str(self))


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de remonte-pente mécanique")
        self.geometry("1200x700")
        self.show_fiche()


    def show_fiche(self):
        self.current_view = Fiche(self, self.show_main)
        self.current_view.pack(fill="both", expand=True)     

    def show_main(self):
        self.current_view.destroy()
        self.current_view = MainApp(self)
        self.current_view.pack(fill="both",expand=True)   

    #Loop du MainApp et choix de l'apparence du ctk
if __name__ == "__main__" :
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    application = Application()
    application.mainloop()
