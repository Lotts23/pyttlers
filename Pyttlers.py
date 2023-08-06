import importlib
import json
import os
import shutil
import sys
import time
from typing import Dict

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QRect, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QLabel,
                             QMessageBox, QPushButton, QStackedWidget,
                             QVBoxLayout, qApp)

import image_utils
from expl import ExplWindow
from geo import GeoWindow
from running import ProgressDialog

def move_json_files_to_app_data():
    global app_data_path
    exe_path = sys.argv[0]

    if sys.platform == 'win32':
        # För Windows, använda APPDATA-mappen
        app_data_dir = os.getenv('APPDATA')
    elif sys.platform == 'darwin':
        # För Mac, använda hemmappen
        app_data_dir = os.path.expanduser("~/Library/Application Support")
    else:
        # För Linux, använda hemmappen
        app_data_dir = os.path.expanduser(os.path.join(os.getenv('HOME'), ".config"))

    app_data_path = os.path.join(app_data_dir, 'Pyttlers')
    os.makedirs(app_data_path, exist_ok=True)

    exe_dir = os.path.dirname(os.path.abspath(exe_path))
    data_json_files = ["expl_nummer.json", "geo_nummer.json", "scale_data.json"]

    for json_file in data_json_files:
        data_path = os.path.join(exe_dir, "data", json_file)
        dest_path = os.path.join(app_data_path, json_file)
        shutil.copy(data_path, dest_path)

    return app_data_path

class StartDialog(QtWidgets.QDialog):
    returnToDialog = QtCore.pyqtSignal()

    def __init__(self, app_data_path):
        super(StartDialog, self).__init__()
        self.app_data_path = app_data_path
        self.setWindowTitle("Välj läge")
        self.setFixedSize(300, 200)

        # Skapa en layout för dialogrutan
        layout = QtWidgets.QHBoxLayout(self)

        with open("./data/stil.css", "r", encoding="utf-8") as file:
            self.setStyleSheet(file.read())

        # Kontrollera om json-filen med varning finns, dvs om användaren fått en varning tidigare
        if not os.path.exists(f"{app_data_path}/popup.json"):
            # Visa popup-rutan för första gången
            QMessageBox.information(None, "Viktig information", "När du har valt specialister och klickar ''check'' så tar programmet kontroll över din mus. Den är lärd att hantera vanligare felklick som om den råkar klicka på en specialist som redan är ute, men skulle problem uppstå så för du muspekaren längst ut i ett av skärmens hörn och håller den där. Det är en generell nödbroms som stoppar programmet.\nSläpp musen när programmet börjar jobba.\n\nDet här programmet är en demonstration av GUI-styrkod med Pyautogui och inte avsett att användas för att bryta mot TSO-regler.")

            # Skapa json-filen och markera användaren som informerad
            with open(f"{app_data_path}/popup.json", "w", encoding="utf-8") as json_file:
                json.dump({"informed": True}, json_file)

        # Skapa knappen för geolog-läget
        geo_button = QtWidgets.QPushButton()
        geo_button.setFixedSize(57, 68)
        geo_button.setIcon(QtGui.QIcon("./data/img/knapp/geo_knapp.png"))
        geo_button.setIconSize(geo_button.rect().size())
        geo_button.clicked.connect(self.open_geo_window)
        layout.addWidget(geo_button)

        # Skapa knappen för explorer-läget
        expl_button = QtWidgets.QPushButton()
        expl_button.setFixedSize(57, 68)
        expl_button.setIcon(QtGui.QIcon("./data/img/knapp/expl_knapp.png"))
        expl_button.setIconSize(expl_button.rect().size())
        expl_button.clicked.connect(self.open_expl_window)
        layout.addWidget(expl_button)


    def hitta_skalfaktor(self, skalbild_sokvag):# Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.
        tillatna_varden = [1, 0.75, 0.625, 0.55, 0.5, 0.45, 0.375, 0.25]
        global faktor
        for faktor in tillatna_varden:
            hittad_skalfaktor = image_utils.find_image(skalbild_sokvag, confidence=0.63, scale_factor=faktor)
            if hittad_skalfaktor is not None:
                data = {"faktor": faktor}
                with open(f"{app_data_path}/scale_data.json", "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file)
                return faktor
            time.sleep(0.01)
            app.exit(0)
        ### Skriv en felhantering för när skalan inte hittas
        return

    def testa_skalfaktor(self, skalbild_sokvag, faktor):
        hittad_testbild = image_utils.find_image(skalbild_sokvag, confidence=0.8, scale_faktor=faktor)

        if hittad_testbild is not None:
            return faktor
        else:
            self.hitta_skalfaktor("./data/img/01_image.bmp")
            return faktor


    def scale_handling(self):
        json_fil = f"{app_data_path}/scale_data.json"
        if os.path.isfile(json_fil):  # Om det finns en fil
            with open(json_fil, "r", encoding="utf-8") as json_file:  # öppna den
                json_data = json.load(json_file)  # och läs datan
                faktor = json_data.get("faktor")  # Hämta tidigare faktor
                test_factor = faktor
            if test_factor is not None: # Om faktor-värdet inte är tomt, testa det
                testad_faktor = start_dialog.testa_skalfaktor("./data/img/01_image.bmp", faktor) # Testar om gamla faktorn funkar
                if testad_faktor is None:
                    test_factor = self.hitta_skalfaktor("./data/img/01_image.bmp")
                    return test_factor
                else:
                    data = {"faktor": faktor}
                    with open(f"{app_data_path}/scale_data.json", "w", encoding="utf-8") as json_file:
                        json.dump(data, json_file)
                    return test_factor, faktor
        else:
            test_factor = self.hitta_skalfaktor("./data/img/01_image.bmp")
            return test_factor

    def open_geo_window(self):
        # Stäng dialogrutan och öppna geo-fönstret
        self.accept()
        self.geo_window = GeoWindow()
        self.geo_window = GeoWindow()
        self.hide()
        self.geo_window.returnToDialog.connect(self.show)  # Lägg till signalhantering för att visa dialogrutan igen
        self.geo_window.show()
        self.miniprogram = ProgressDialog(app_data_path)
        self.miniprogram.returnToDialog.connect(self.on_returnToDialog)
        self.geo_window.returnToDialog.connect(self.showProgressDialog)
        self.miniprogram.returnToDialog.connect(self.showProgressDialog)

    def open_expl_window(self):
        # Stäng dialogrutan och öppna expl-fönstret
        self.accept()
        self.expl_window = ExplWindow()
        self.expl_window = ExplWindow()
        self.hide()
        self.expl_window.returnToDialog.connect(self.show)  # Lägg till signalhantering för att visa dialogrutan igen
        self.expl_window.show()
        self.miniprogram = ProgressDialog(app_data_path)
        self.miniprogram.returnToDialog.connect(self.show)
        self.expl_window.returnToDialog.connect(self.showProgressDialog)
        self.miniprogram.returnToDialog.connect(self.showProgressDialog)

    def showProgressDialog(self):
        self.show()
        self.miniprogram.hide()

    def on_returnToDialog(self):
        self.show()



if __name__ == "__main__":
    app_data_path = move_json_files_to_app_data()
    from expl import ExplWindow
    from geo import GeoWindow
    from running import ProgressDialog
    global faktor
    faktor = None
    #from running2 import ProgressDialog
    app = QtWidgets.QApplication(sys.argv)
    start_dialog = StartDialog(app_data_path)

    miniprogram = ProgressDialog(app_data_path)
    start_dialog.show()
    faktor = StartDialog.scale_handling(app_data_path)
    miniprogram.hide()

    sys.exit(app.exec_())