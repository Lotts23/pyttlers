import json
import sys
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
                             QVBoxLayout)


class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pågår...")
        self.setFixedSize(300, 150)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Fönstret alltid överst

        self.setStyleSheet(open("stil.css").read())  # Länk till stil.css

        layout = QVBoxLayout(self)

        self.label = QLabel("Process pågår...\nSöker {geologer} som ska leta {resurs}\nnödstopp genom att flytta musen till skärmens hörn.", self)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)    

        self.button = QPushButton("Starta om processen", self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.start_process)  # Anslut knappen till start_process-metoden
        
        self.button = QPushButton("Avbryt", self)
        layout.addWidget(self.button)
        
        self.button.clicked.connect(self.stop_process)
        
    def stop_process(self):
        self.close()  # Stäng minifönstret och avbryt processen

    def start_process(self):
        #self.hide()  # Göm minifönstret
        leta_sten()  # Starta leta_sten-funktionen    


def prepare(): # Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.

    def hitta_skalfaktor(skalbild_sokvag): # Som det låter, vi kollar skalan
        faktor = 1 # Vi kan börja med faktor 2 också och först skala upp bilden, med sämre resultat och längre tid
        skalbild = Image.open(skalbild_sokvag)

        while faktor >= 0.2: # Den behöver aldrig pröva mindre än så här. Om faktor 1 är 200% i spelet så är 0.2 20% och spelet går bara ner till 50%
            skalad_bild = skalbild.resize((int(skalbild.width * faktor), int(skalbild.height * faktor)))
            skalbild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
            hittad_skalfaktor = pyautogui.locateOnScreen(skalbild_array, confidence=0.7, grayscale=True)

            if hittad_skalfaktor is not None: #skriv till json
                pyautogui.moveTo(hittad_skalfaktor)
                faktor = round(faktor, 1)
                data = {"faktor": faktor}
                with open("scale_data.json", "w") as json_file: # Skriv i json
                    json.dump(data, json_file)
                return faktor

            print(".", end="", flush=True)
            time.sleep(0.1) # Vid många fel kan denna ökas.

            faktor -= 0.02 # Lägre tal ger större nogrannhet i sökningen.

        return None

    hitta_skalfaktor("img/01_image.BMP")

    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    def oppna_stjarna(bild_sokvag, faktor):
        hittad = None
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        time.sleep(1)
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None: #klicka
            hittad = pyautogui.center(hittad_position)
            time.sleep(1)  # minskar fel
            pyautogui.moveTo(hittad)
            pyautogui.click(duration=1)
            time.sleep(1)  # minskar fel
        else:
            print(f"{bild_sokvag} inte hittad")

    # Testar om stjärnann är öppen annars kör den funktionen öppna stjärna. Definitionen av 
    # öppna stjärna ligger över just för att vara redo att köras om hitta_bild_stjärna inte 
    # hittar stjärnfönstret. Alternativt skulle hela definitionen ligga i if-else.
    def hitta_bild_stjarna(bild_sokvag, faktor):
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            time.sleep(1)  # minskar antalet fel
            print("\nstjärnan öppen")
        else:
            print(f"{bild_sokvag} inte hittad")
            oppna_stjarna("img/03_image.BMP", faktor) # Här öppnas stjärnan om stjärnmenyn inte hittats.

    hitta_bild_stjarna("img/02_image.BMP", faktor) # Detta är den öppna stjärnmenyn, om den hittas går vi vidare, annars öppnas stjärnan

    with open("scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor
        data = json.load(json_file)
        faktor = data["faktor"]

    def tab_stjarna(bild_sokvag, faktor):
        hittad = None
        time.sleep(1)  # minskar fel
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array

        try:
            hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)
            if hittad_position is not None:
                hittad = pyautogui.center(hittad_position)
                time.sleep(1)  # minskar fel
                pyautogui.moveTo(hittad)
                pyautogui.click(duration=1)
                time.sleep(1)  # minskar fel
        except:
            pass

    tab_stjarna("img/04_image.BMP", faktor)
    
prepare() # Kör hela ovanstående förberedelser inför att ta tag i uppdraget

    
time.sleep(2)  # minskar fel

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]

with open("scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor
    data = json.load(json_file)
    faktor = data["faktor"]

def leta_sten():
    global flagga  # Använd global för att referera till den globala variabeln
    flagga = True
    for geolog in geologer:
        flagga = True  # Återställ flagga till True vid varje iteration

        while flagga:
            def hitta_geolog(bild_sokvag, faktor):
                global flagga  # Använd nonlocal för att ändra flagga i den yttre funktionen
                time.sleep(1)
                hittad = None
                bild = Image.open(bild_sokvag)
                skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                if hittad_position is not None:
                    hittad = pyautogui.center(hittad_position)
                    time.sleep(1)  # minskar fel
                    pyautogui.moveTo(hittad)
                    pyautogui.click(duration=1)
                    pyautogui.moveTo(200, 200)
                    time.sleep(3) 
                else:
                    flagga = False
                    print(f"{bild_sokvag} inte hittad")
                    

                return hittad

            hittad_geolog = hitta_geolog(f"img/{geolog}_geo.BMP", faktor)
            if not hittad_geolog:
                flagga = False

            hitta_geolog(f"img/{geolog}_geo.BMP", faktor)

            def hitta_resurs(bild_sokvag, faktor):
                hittad = None
                time.sleep(1)
                bild = Image.open(bild_sokvag)
                skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                if hittad_position is not None:
                    x, y, width, height = hittad_position
                    knappens_plats = x + width - (width // 5), y + (height // 2)
                    time.sleep(1)  # minskar fel
                    pyautogui.moveTo(knappens_plats)
                    pyautogui.click(duration=1)
                    pyautogui.moveTo(200, 200)
                    time.sleep(1)  # minskar fel
                else:
                    hittad = None
                    print("resurs inte hittad")

                return 

            hitta_resurs(f"img/{resurs}_resurs.BMP", faktor)

            def hitta_check(bild_sokvag, faktor):
                hittad = None
                time.sleep(1)
                bild = Image.open(bild_sokvag)
                skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=False)

                if hittad_position is not None:
                    hittad = pyautogui.center(hittad_position)
                    time.sleep(1)  # minskar fel
                    pyautogui.moveTo(hittad)
                    pyautogui.click(duration=1)
                    time.sleep(3)  # minskar fel
                else:
                    print("check inte hittad")
                

            hitta_check("img/check.BMP", faktor)

            

    leta_sten()
    print("Alla möjliga klick är genomförda.")  

if __name__ == "__main__":
    app = QApplication([])
    miniprogram = ProgressDialog()
    miniprogram.show()
    prepare()
    leta_sten()
    app.exec_()
    sys.exit()
