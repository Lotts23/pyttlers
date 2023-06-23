import json
from p1 import hitta_skalfaktor
from p2 import hitta_bild
import pyautogui

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Progress")
        self.setFixedSize(300, 150)
        
        self.setStyleSheet(open("stil.css").read())  # Länka till stil.css

        layout = QVBoxLayout(self)

        self.label = QLabel("Process pågår...", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton("Avbryt", self)
        layout.addWidget(self.button)
        
        self.button.clicked.connect(self.stop_process)
        
    def stop_process(self):
        self.close()  # Stäng minifönstret och avbryt processen

def main():
    with open("scale_data.json", "w") as f:
        json.dump({}, f)  # Skriv över filen med en tom dictionary

    progress_dialog = ProgressDialog()  # Skapa instans av ProgressDialog

    # Skapa ett huvudfönster och lägg till minifönstret
    main_window = QWidget()
    layout = QVBoxLayout(main_window)
    layout.addWidget(progress_dialog)

    # Visa huvudfönstret
    main_window.show()

    faktor = hitta_skalfaktor("img/01_image.JPG") #Denna är alltid samma
    print(f"Skalfaktor hittad: {faktor}") 

    with open('nummer.json', 'r') as f:
        data = json.load(f)

    geologer = data['geologer']
    resurs = ""

    if resurs_nummer:
        resurslet = f"img/{resurs}_image.JPG"
        hittad_bild = hitta_bild(resurslet, faktor)

        if hittad_bild:
            print("Specialisten hittad")
            pyautogui.moveTo(hittad_bild)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
        else:
            print("Ingen bild hittad för det resursen")

    for num in data['geologer']:
        bild_adress = f"img/{num}_image.JPG"
        hittad_bild = hitta_bild(bild_adress, faktor)

        if hittad_bild:
            print("Resurs hittad")
            pyautogui.moveTo(hittad_bild)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

            if resurs:
                resurs_bild_adress = f"img/{resurs}"
                hittad_resurs = hitta_bild(resurs_bild_adress, faktor)

                if hittad_resurs:
                    print(f"Resurs {resurs} hittad")
                    pyautogui.moveTo(hittad_resurs)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                else:
                    print(f"Ingen bild hittad för {resurs}")
        else:
            print(f"Ingen bild hittad för {bild_adress}")

    print("Klar")

if __name__ == "__main__":
    app = QApplication([])
    main()
    app.exec_()
