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

        self.grid_rowconfigure(0, weight=1)
        self.sliders = Sliders(self, self.__chairlift, self.mettre_a_jour)
        self.sliders.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=12, pady=12)

        self.graph = GraphControl(self, self.__chairlift)
        self.graph.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)

        # Affichage du label du nombre de personne par heure avec les paramètres courants.
        ctk.CTkLabel(self, bg_color="green", text="Nombre de personnes par heure :" + str(self.__chairlift.calculerNombreDePersonnesParHeure())).grid(row=1, column=1, sticky="nsew", padx=12, pady=12)

        # Modifier le poids des différentes colonnes
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        # Appeler mettre à jour qui met à jour l'image/le graph
        self.mettre_a_jour()

    # mettre à jour le graphique 
    def mettre_a_jour(self):
        #TODO regler le edge case de aucun paramètre observé, c'est juste vide 
        self.graph.mise_a_jour_image()



if __name__ == "__main__" :
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("green")
    application = MainApp()
    application.mainloop()
