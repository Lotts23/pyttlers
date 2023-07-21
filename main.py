import json
import os
import importlib
import sys

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from src.expl import ExplWindow
from src.geo import GeoWindow


class StartDialog(QtWidgets.QDialog):
    def __init__(self):
        super(StartDialog, self).__init__()
        self.setWindowTitle("Välj läge")
        self.setFixedSize(300, 200)

        # Skapa en layout för dialogrutan
        layout = QtWidgets.QHBoxLayout(self)

        with open("./src/stil.css", "r") as file:
            self.setStyleSheet(file.read())
            
        # Kontrollera om json-filen med varning finns, dvs om användaren fått en varning tidigare
        if not os.path.exists("./src/popup.json"):
            # Visa popup-rutan för första gången
            QMessageBox.information(None, "Viktig information", "När du har valt specialister och klickar ''check'' så tar programmet kontroll över din mus. Den är lärd att hantera vanligare felklick som om den råkar klicka på en specialist som redan är ute, men skulle problem uppstå så för du muspekaren längst ut i ett av skärmens hörn och håller den där. Det är en generell nödbroms som stoppar programmet.\nSläpp musen när programmet börjar jobba.\n\nDet här programmet är en demonstration av GUI-styrkod med Pyautogui och inte avsett att användas för att bryta mot TSO-regler.")
            

            # Skapajson-filen och markera användaren som informerad
            with open("./src/popup.json", "w") as json_file:
                json.dump({"informed": True}, json_file)     
                
        # Skapa knappen för geolog-läget
        geo_button = QtWidgets.QPushButton()
        geo_button.setFixedSize(57, 68)
        geo_button.setIcon(QtGui.QIcon("./src/img/knapp/geo_knapp.png"))
        geo_button.setIconSize(geo_button.rect().size())
        geo_button.clicked.connect(self.open_geo_window)
        layout.addWidget(geo_button)

        # Skapa knappen för explorer-läget
        expl_button = QtWidgets.QPushButton()
        expl_button.setFixedSize(57, 68)
        expl_button.setIcon(QtGui.QIcon("./src/img/knapp/expl_knapp.png"))
        expl_button.setIconSize(expl_button.rect().size())
        expl_button.clicked.connect(self.open_expl_window)
        layout.addWidget(expl_button)

    def open_geo_window(self):
        # Stäng dialogrutan och öppna geo-fönstret
        self.accept()
        self.geo_window = GeoWindow()
        self.hide()
        self.geo_window.returnToDialog.connect(self.show)  # Lägg till signalhantering för att visa dialogrutan igen
        self.geo_window.show()

    def open_expl_window(self):
        # Stäng dialogrutan och öppna expl-fönstret
        self.accept()
        expl_window = ExplWindow()
        self.hide()
        expl_window.returnToDialog.connect(self.show)  # Lägg till signalhantering för att visa dialogrutan igen
        expl_window.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    img_folder = os.path.join(os.path.dirname(__file__), "src", "img")
    image_files = [f for f in os.listdir(img_folder) if f.lower().endswith((".bmp", ".png", ".jpg"))]
    css_folder = os.path.join(os.path.dirname(__file__), "src")
    css_files = [f for f in os.listdir(css_folder) if f.lower().endswith(".css")]
    json_folder = os.path.join(os.path.dirname(__file__), "src")
    json_files = [f for f in os.listdir(json_folder) if f.lower().endswith(".json")]
    
    start_dialog = StartDialog()
    if start_dialog.exec_() == QtWidgets.QDialog.Accepted:
        sys.exit(app.exec_())
