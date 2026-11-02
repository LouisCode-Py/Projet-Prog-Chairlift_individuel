from Sliders import Sliders
from Chairlift import Chairlift
from GraphControl import GraphControl

import customtkinter as ctk

class MainApp(ctk.CTk) :

    def __init__(self) :
        # Initialiser la fenêtre principale
        super().__init__()
        self.title("Gestionnaire de remonte-pente mécanique")
        self.geometry("1200x700")

        # Initialiser, en privé, le Chairlift courant
        self.__chairlift = Chairlift()

        # Initialiser la frame des sliders et autres boutons
        self.grid_rowconfigure(0, weight=1)
        self.sliders = Sliders(self, self.__chairlift, self.mettre_a_jour)
        self.sliders.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=12, pady=12)

        # Initialiser la frame du Graphique
        self.graph = GraphControl(self, self.__chairlift)
        self.graph.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)

        # Affichage du label du nombre de personne par heure avec les paramètres courants.
        self.label_nb_personne = ctk.CTkLabel(self, bg_color="white", text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()), text_color="black")
        self.label_nb_personne.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0,12))
        # Bouton de rafraichissement
        self.bouton_rafraichissement = ctk.CTkButton(self, text="Recalculer", command=self._rafraichissement)
        self.bouton_rafraichissement.grid(row=2, column=1, sticky="nsew", padx=12, pady=(3,12))

        # Modifier le poids des différentes colonnes
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Appeler mettre à jour qui met à jour l'image/le graph
        self.mettre_a_jour()

    # mettre à jour le graphique 
    def mettre_a_jour(self):
        self.graph.mise_a_jour_image()

    # Commande du bouton de rafraichissement qui recalcul et déselectionne
    def _rafraichissement(self) :
        self.sliders.reset_radio_var()
        self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))


#TODO il a un "print(fuck)" en qq part...???

if __name__ == "__main__" :
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    application = MainApp()
    application.mainloop()
