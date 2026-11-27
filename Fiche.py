import customtkinter as ctk
from PIL import Image
import sys
from pathlib import Path


class Fiche(ctk.CTkFrame):
    def __init__(self,parent,continuer):
        super().__init__(parent)
        # Crée le path pour avoir l'image de fond d'écran
        image_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / "96431.png"
        image = Image.open(image_path)
        self.fond_ecran = ctk.CTkImage(light_image=image,dark_image=image,size=(1200,700))

        self.bg_label = ctk.CTkLabel(self, text="", image=self.fond_ecran)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Création du bouton d'accueil
        self.button = ctk.CTkButton(self,text="Bienvenue, veuillez cliquer pour continuer",
                                    font=("Arial",23,"bold"),
                                    fg_color="black",hover_color="black",width=500,height=50, command=continuer)
        self.button.place(anchor=ctk.CENTER, relx=0.5,rely=0.5)
        self.bind("<Configure>", self._changer_fe)

    # Creation methode pour changer grosseur de l'image de fond ecran
    def _changer_fe(self,event):
        # Change la dimension de la fenetre
        if event.width > 1 and event.height > 1:
            self.fond_ecran.configure(size=(event.width,event.height))

    # Methode de test
    def button_click(self):
        print("button click")

