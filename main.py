from Sliders import Sliders
from Chairlift import Chairlift
from GraphControl import GraphControl
from GraphScatter import GraphScatter
from Energy import Energy
from Fiche import Fiche
from BarGraph import BarGraph
from CTkMenuBar import *
from CTkMessagebox import CTkMessagebox

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

        # Initialiser le frame du Graphique bar
        self.barGraph = BarGraph(self, self.__chairlift,self.energy)
        self.barGraph.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)

        # Initialiser le frame du Graphique scatter
        self.scatterGraph = GraphScatter(self,self.__chairlift,self.energy)
        self.scatterGraph.grid(row=0,column=1,sticky="nsew",padx=12,pady=12)

        # Initialiser le frame du Graphique ligne
        self.graph = GraphControl(self, self.__chairlift,self.energy)
        self.graph.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)




        # Affichage du label du nombre de personnes par heure avec les paramètres courants.
        self.label_nb_personne = ctk.CTkLabel(self, bg_color="white", text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()), text_color="black")
        #self.label_nb_personne.grid(row=1, column=1, sticky="nsew", padx=10, pady=(0,12))\



        
        # Création de barre de sélection en haut de l'application principale
        menu = CTkMenuBar(master=parent)
        # Ajout de cascade et bouton principale
        selectionGraphique = menu.add_cascade("Type de graphique")
        selectionG = CustomDropdownMenu(widget=selectionGraphique)
        menuSecondaireG = selectionG.add_submenu("Graphique") 
        menuSecondaireG.add_option(option="Ligne",command=self._quand_selectionner_ligne)
        menuSecondaireG.add_option(option="Barres",command=self._quand_selectionner_bar)
        menuSecondaireG.add_option(option="Points",command=self._quand_selectionner_points)

        # Création sélection de boutons chargement et sauvegarde csv 
        exportImport = menu.add_cascade("Sauvegarde/Charge")
        selectionEI = CustomDropdownMenu(widget=exportImport)
        menuSelectionEI = selectionEI.add_submenu("Option désirée : ")
        menuSelectionEI.add_option(option="Sauvegarder",command=self.sliders._quand_exporter)
        menuSelectionEI.add_option(option="Charger",command=self.sliders._quand_importer)



        # Création de bouton dans la barre de menu pour quitter
        option = menu.add_cascade("Option")
        selectionO = CustomDropdownMenu(widget=option)
        # Ajout d'une option pour calculer énergie
        menuOption = selectionO.add_option("Énergie",command=self._energie_calcul)
        menuOption = selectionO.add_option("Coût",command=self.coutEnDollar)


        # Change le poids de la colonne 4 pour qu'elle prends toute la place restante sur la barre de menu
        menu.grid_columnconfigure(4, weight=1)
        # Ferme la fenêtre
        quitter = menu.add_cascade("Quitter",command=self.winfo_toplevel().destroy)
        # Place la colonne de l'option quitter totalement à droite avec un espace de 15 pixel entre la bordure et le bouton
        quitter.grid(row=0,column=4,sticky="e",padx=(0,15))




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
    
    # Permet de placer le graphique de ligne par dessus le graphique de barres
    def _quand_selectionner_ligne(self):
        self.graph.tkraise()

    # Permet de placer le graphique de barres par dessus le graphique de lignes
    def _quand_selectionner_bar(self):
        self.barGraph.tkraise()

    # Permet de placer le graphique de points par dessus le graphique de lignes
    def _quand_selectionner_points(self):
        self.scatterGraph.tkraise()

    # Mettre à jour le graphique 
    def mettre_a_jour(self):
        self.graph.mise_a_jour_image()
        self.barGraph.mise_a_jour_image()
        self.scatterGraph.mise_a_jour_image()
        
        self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))

        #.label_calcul_energie.configure(text="energie : " + str(self.energy.calculerTout))

    # Commande du bouton de rafraichissement qui recalcule et déselectionne
    def _rafraichissement(self) :
        self.sliders.reset_radio_var()
        
        #self.label_nb_personne.configure(text="Nombre de personnes par heure : " + str(self.__chairlift.calculerNombreDePersonnesParHeure()))


    # Fonction pour afficher un MessageBox avec l'énergie et puissance
    def _energie_calcul(self):
        resultats = self.energy.calculerTout()
        CTkMessagebox(
            #Accède au dictionnaire de calculerTout pour sortir energie totale et puissance total
            #:.2f fait afficher au plus 2 decimales
            title="Énergie",
            message=(f"Énergie totale : {resultats['energie_totale']:.2f} Wh \n"
            f"Puissance totale : {resultats['puissance_electrique']:.2f} W"
            )
        )

    # Fonction pour afficher le cout total par heure
    def coutEnDollar(self):
        cout = self.energy.coutTotal()
        CTkMessagebox(
            #Prend ce que la fonction de Energy, coutTotal retourne et le met dans un message box
            title="Coût a faire fonctionner par heure",
            message=(
                f"{cout:.2f} $"
                )
        )


# Définition de classe Application
class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestionnaire de remonte-pente mécanique")
        self.geometry("1200x700")
        self.show_fiche()

    # Méthode pour afficher la fenêtre d'accueil
    def show_fiche(self):
        self.fenetre = Fiche(self, self.show_main)
        self.fenetre.pack(fill="both", expand=True)     

    # Méthode pour afficher la fenêtre principale d'accueil
    def show_main(self):
        self.fenetre.destroy()
        self.fenetre = MainApp(self)
        self.fenetre.pack(fill="both",expand=True)

    #Loop du MainApp et choix de l'apparence du ctk
if __name__ == "__main__" :
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("green")
    application = Application()
    application.mainloop()
