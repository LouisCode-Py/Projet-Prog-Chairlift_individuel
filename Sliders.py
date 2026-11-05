import customtkinter as ctk
from tkinter import IntVar, filedialog

# Constante des paddings pour les widgets de chaque paramètre
PADDING_EN_Y = 30
PADDING_EN_X = 10

"""LEGENDE radio var et ordre des sliders"""
"------------------------------------------"
"Longueur cable :     1"
"Nombre chaise :      2"
"Vitesse :            3"
"Temps embarquement : 4"
"Temps debarquement : 5"
"Capacite chaise :    6"

class Sliders(ctk.CTkFrame) :

    def __init__(self, parent, chairlift, sur_mise_a_jour) :
        # Passage du Ctk parent pendant le constructeur, donc pour qu'il soit dans la MainApp
        super().__init__(parent)

        # Initialiser le Chairlift courant et appeler la création des widgets
        self.chairlift = chairlift
        self.creer_widgets()
        self.mise_a_jour = sur_mise_a_jour
        

    def creer_widgets(self) :

        # Créer les boutons d'importation et d'exportation, leur passer la commande _quand_importer qui est appelé si les boutons sont cliqués
        self.bouton_importer = ctk.CTkButton(self, text="Importer un CSV", command=self._quand_importer)
        self.bouton_importer.grid(row=6, column=0, padx=PADDING_EN_X, pady=20)
        self.bouton_exporter = ctk.CTkButton(self, text="Exporter un CSV", command=self._quand_exporter)
        self.bouton_exporter.grid(row=6, column=1, padx=PADDING_EN_X, pady=20)

        # initialiser la variable pour les "radiobutton", empêche que plusieurs soient cochés
        self.radio_var = IntVar(value=0)

        # Appeler les fonctions de création de chacun des paramètres du chairlift
        self.creer_widgets_cable()
        
        self.creer_widgets_chaise()

        self.creer_widgets_vitesse()

        self.creer_widgets_embarque()

        self.creer_widgets_debarque()
        
        self.creer_widgets_capacite()

        # Configurer les colonnes pour qu'ils prennent le frame, lorsqu'elle est étirée
        for i in range(7) :
            self.grid_rowconfigure(i, weight=1)
        
        
    # Les suivantes sont appelées pour créer sliders, texte et boutons, etc. de chacun des paramètres.
    # Le fonctionnement de celles-ci est identique dépendant des paramètres, l'explication est donc seulement fait une fois.
    def creer_widgets_cable(self) :
        # Création du texte lié au paramètre spécifique
        ctk.CTkLabel(self, text="Longueur du câble").grid(row=0, column=0, sticky="w", padx=PADDING_EN_X, pady=PADDING_EN_Y)

        # Création du slider, sa commande est relié à _quand_slider_<paramètre>
        self.slider_cable = ctk.CTkSlider(self, from_=0, to=3000, number_of_steps=3000)
        self.slider_cable.set(0)
        self.slider_cable.configure(command=self._quand_slider_cable)
        self.slider_cable.grid(row=0, column=1, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)

        # Première création du texte affichant la valeur du slider
        self.text_cable = ctk.CTkLabel(self, text="0" + " m")
        self.text_cable.grid(row=0, column=2, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)

        # Création du radio button permettant de choisir le paramètre observé et d'en sélectionner un seul, on leur passe tous la variable radio_var qui permet de suivre lequel est choisi. 
        self.case_cable = ctk.CTkRadioButton(self, text="", command=self._actualiser_slider, variable=self.radio_var, value=1)
        self.case_cable.grid(row=0, column=3, sticky="e")

    def creer_widgets_chaise(self) :
        ctk.CTkLabel(self, text="Nombre de chaises").grid(row=1, column=0, sticky="w", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.slider_chaise = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100)
        self.slider_chaise.set(0)
        self.slider_chaise.configure(command=self._quand_slider_chaise)
        self.slider_chaise.grid(row=1, column=1, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.text_chaise = ctk.CTkLabel(self, text="0")
        self.text_chaise.grid(row=1, column=2, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.case_chaise = ctk.CTkRadioButton(self, text="", command=self._actualiser_slider, variable=self.radio_var, value=2)
        self.case_chaise.grid(row=1, column=3, sticky="e")

    def creer_widgets_vitesse(self) :
        ctk.CTkLabel(self, text="Vitesse").grid(row=2, column=0, sticky="w", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.slider_vitesse = ctk.CTkSlider(self, from_=0.0, to=8, number_of_steps=(8*10))
        self.slider_vitesse.set(0.0)
        self.slider_vitesse.configure(command=self._quand_slider_vitesse)
        self.slider_vitesse.grid(row=2, column=1, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.text_vitesse = ctk.CTkLabel(self, text="0" + " m/s")
        self.text_vitesse.grid(row=2, column=2, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.case_vitesse = ctk.CTkRadioButton(self, text="", command=self._actualiser_slider, variable=self.radio_var, value=3)
        self.case_vitesse.grid(row=2, column=3, sticky="e")

    def creer_widgets_embarque(self) :
        ctk.CTkLabel(self, text="Temps d'embarquement").grid(row=3, column=0, sticky="w", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.slider_embarque = ctk.CTkSlider(self, from_=0, to=30, number_of_steps=30)
        self.slider_embarque.set(0)
        self.slider_embarque.configure(command=self._quand_slider_embarque)
        self.slider_embarque.grid(row=3, column=1, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.text_embarque = ctk.CTkLabel(self, text="0" + " s")
        self.text_embarque.grid(row=3, column=2, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.case_embarque = ctk.CTkRadioButton(self, text="", command=self._actualiser_slider, variable=self.radio_var, value=4)
        self.case_embarque.grid(row=3, column=3, sticky="e")

    def creer_widgets_debarque(self) :
        ctk.CTkLabel(self, text="Temps de débarquement").grid(row=4, column=0, sticky="w", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.slider_debarque = ctk.CTkSlider(self, from_=0, to=30, number_of_steps=30)
        self.slider_debarque.set(0)
        self.slider_debarque.configure(command=self._quand_slider_debarque)
        self.slider_debarque.grid(row=4, column=1, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.text_debarque = ctk.CTkLabel(self, text="0" + " s")
        self.text_debarque.grid(row=4, column=2, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.case_debarque = ctk.CTkRadioButton(self, text="", command=self._actualiser_slider, variable=self.radio_var, value=5)
        self.case_debarque.grid(row=4, column=3, sticky="e")

    def creer_widgets_capacite(self) :
        ctk.CTkLabel(self, text="Capacité des chaises").grid(row=5, column=0, sticky="w",  padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.slider_capacite = ctk.CTkSlider(self, from_=0, to=8, number_of_steps=8)
        self.slider_capacite.set(0)
        self.slider_capacite.configure(command=self._quand_slider_capacite)
        self.slider_capacite.grid(row=5, column=1, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.text_capacite = ctk.CTkLabel(self, text="0")
        self.text_capacite.grid(row=5, column=2, sticky="ew", padx=PADDING_EN_X, pady=PADDING_EN_Y)
        
        self.case_capacite = ctk.CTkRadioButton(self, text="", command=self._actualiser_slider, variable=self.radio_var, value=6)
        self.case_capacite.grid(row=5, column=3, sticky="e")


    # Les suivantes sont appelés lorsque leurs sliders respectifs changent de valeurs
    # Le fonctionnement de celles-ci est identique dépendant des paramètres, l'explication est donc seulement fait une fois.
    def _quand_slider_cable(self, valeur) :
        if not self.chairlift.definirLongueurDuTrajet(valeur) :
            print("erreur de limite")
        self.text_cable.configure(
            text=str(self.chairlift.obtenirLongueurDuTrajet()) + " m"
        )
        self.mise_a_jour()
    
    def _quand_slider_chaise(self, valeur) :
        if not self.chairlift.definirNombreDeChaise(valeur) :
            print("erreur de limite??")
        self.text_chaise.configure(
            text=str(self.chairlift.obtenirNombreDeChaise())
        )
        self.mise_a_jour()
    
    def _quand_slider_vitesse(self, valeur) :
        if not self.chairlift.definirVitesse(valeur) :
            print("erreur de limite??")
        self.text_vitesse.configure(
            text=str(self.chairlift.obtenirVitesse()) + " m/s"
        )
        self.mise_a_jour()
    
    def _quand_slider_embarque(self, valeur) :
        if not self.chairlift.definirTempsEmbarquement(valeur) :
            print("erreur de limite??")
        self.text_embarque.configure(
            text=str(self.chairlift.obtenirTempsEmbarquement()) + " s"
        )
        self.mise_a_jour()
    
    def _quand_slider_debarque(self, valeur) :
        if not self.chairlift.definirTempsDebarquement(valeur) :
            print("erreur de limite??")
        self.text_debarque.configure(
            text=str(self.chairlift.obtenirTempsDebarquement()) + " s"
        )
        self.mise_a_jour()
    
    def _quand_slider_capacite(self, valeur) :
        if not self.chairlift.definirNombreDePersonnesParChaise(valeur) :
            print("erreur de limite??")
        self.text_capacite.configure(
            text=str(self.chairlift.obtenirNombreDePersonnesParChaise())
        )
        self.mise_a_jour()
    
    
    def _actualiser_slider(self):
        # Aller chercher la valeur de radio_var pour déterminer ce qui est sélectionné
        selection = self.radio_var.get()
    
        if selection == 0 :
            print("Aucun paramètre observé")
    
        """LONGUEUR CABLE"""
        # Encore une fois c'est pareil pour chacun des paramètres
        # On rend le slider inutilisable si la case est sélectionnée
        self.slider_cable.configure(state="disabled" if selection == 1 else "normal")

        # appeler le setter du paramètre observé quand la case est choisie
        resultat1 =  self.chairlift.definirParametreObserver("longueurDuTrajet") if selection == 1 else True

        # Vérifier la sélection et mettre à jour le graph
        if selection == 1  and resultat1 :
            print("Graph longeur cable dans la bonne place")
            self.mise_a_jour()
        if not resultat1 : 
            print("Erreur dans le setter 1")
    
        """NOMBRE DE CHAISES"""
        self.slider_chaise.configure(state="disabled" if selection == 2 else "normal")
    
        resultat2 = self.chairlift.definirParametreObserver("nombreDeChaise") if selection == 2 else True
        if selection == 2 and resultat2 :
            print("Graph nombre chaise dans la bonne place")
            self.mise_a_jour()
        if not resultat2 :
            print("Erreur dans le setter 2")
    
        """VITESSE"""
        self.slider_vitesse.configure(state="disabled" if selection == 3 else "normal")
    
        resultat3 = self.chairlift.definirParametreObserver("vitesse") if selection == 3 else True
        if selection == 3 and resultat3:
            print("Graph vitesse dans la bonne place")
            self.mise_a_jour()
        if not resultat3 :
            print("Erreur dans le setter 3")
    
        """TEMPS EMBARQUEMENT"""
        self.slider_embarque.configure(state="disabled" if selection == 4 else "normal")
        resultat4 = self.chairlift.definirParametreObserver("tempsEmbarquement") if selection == 4 else True
        if selection == 4 and  resultat4:
            print("Graph temps embarquement dans la bonne place")
            self.mise_a_jour()
        if not resultat4 :
            print("Erreur dans le setter 4")
    
        """TEMPS DEBARQUEMENT"""
        self.slider_debarque.configure(state="disabled" if selection == 5 else "normal")
        resultat5 = self.chairlift.definirParametreObserver("tempsDebarquement") if selection == 5 else True
        if selection == 5 and resultat5 :
            print("Graph temps debarquement dans la bonne place")
            self.mise_a_jour()
        if not resultat5 :
            print("Erreur dans le setter 5")
    
        """CAPACITÉ CHAISE"""
        self.slider_capacite.configure(state="disabled" if selection == 6 else "normal")
        resultat6 = self.chairlift.definirParametreObserver("nombreDePersonnesParChaise") if selection == 6 else True
        if selection == 6 and resultat6 :
            print("Graph capacité dans la bonne place")
            self.mise_a_jour()
        if not resultat6 :
            print("Erreur dans le setter 6")
    
    
    # Fonctions appelées lors de l'appui des boutons d'import et d'export
    def _quand_importer(self) :
        chemin = filedialog.askopenfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if chemin:
            self.chairlift.importerDepuisCSV(chemin)
        self.appliquer_val_sliders()
        print("Bouton importer")

    def _quand_exporter(self) :
        chemin = filedialog.asksaveasfilename(defaultextension=".csv",
        filetypes=[("Fichiers CSV", "*.csv")])
        if chemin:
            self.chairlift.exporterVersCSV(chemin)
        print("Bouton exporter")
    
    def reset_radio_var(self) :
        self.radio_var.set(0)
        self._actualiser_slider()
        self.chairlift.definirParametreObserver("none")
        self.mise_a_jour()

    # Modifier les valeurs de des sliders pour qu'ils correspondent bien à celles importées
    def appliquer_val_sliders(self) :
        self.slider_cable.set(self.chairlift.obtenirLongueurDuTrajet())
        self.text_cable.configure(text=str(self.chairlift.obtenirLongueurDuTrajet()) + " m")

        self.slider_capacite.set(self.chairlift.obtenirNombreDePersonnesParChaise())
        self.text_capacite.configure(text=str(self.chairlift.obtenirNombreDePersonnesParChaise()))

        self.slider_chaise.set(self.chairlift.obtenirNombreDeChaise())
        self.text_chaise.configure(text=str(self.chairlift.obtenirNombreDeChaise()))

        self.slider_debarque.set(self.chairlift.obtenirTempsDebarquement())
        self.text_debarque.configure(text=str(self.chairlift.obtenirTempsDebarquement()) + " s")

        self.slider_embarque.set(self.chairlift.obtenirTempsEmbarquement())
        self.text_embarque.configure(text=str(self.chairlift.obtenirTempsEmbarquement()) + " s")
        
        self.slider_vitesse.set(self.chairlift.obtenirVitesse())
        self.text_vitesse.configure(text=str(self.chairlift.obtenirVitesse()) + " m/s")
        
