import json
import sys
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
                             QVBoxLayout)

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]  
    
with open("geo_namn.json", "r") as geo_file:
    geo_data = json.load(geo_file)
    geo_dict = geo_data

geologer_namn = [geo_dict[str(num)] for num in geologer]    
    
### Hantera först att det är nån inkonsekvens i sökmönstret, sen gör en running2.py för explorers... fast det borde eg gå att kombinera?
### Bla verkar den klicka på stjärnan trots att stjärnmeny-bilden hittats...
### Sen så behöver jag se över time.sleep som är obalanserad.
### Och optimera genom att skapa en lokal sökruta.

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pågår...")
        self.setFixedSize(300, 150)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Fönstret alltid överst

        self.setStyleSheet(open("stil.css").read())  # Länk till stil.css

        layout = QVBoxLayout(self)

        self.label = QLabel(f"Process pågår...\nSöker {geologer_namn} som ska leta {resurs}\nnödstopp genom att flytta musen till skärmens hörn.", self)

        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.button = QPushButton("Starta om processen", self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.start_process)  # Anslut knappen till start_process-metoden
        self.button.setFocus()

        self.button = QPushButton("Avbryt", self)
        layout.addWidget(self.button)

        self.button.clicked.connect(self.stop_process)

    def stop_process(self):
        self.close()  # Stäng minifönstret och avbryt processen

    def start_process(self):
        #self.hide()  # Göm minifönstret
        leta_sten()  # Starta leta_sten-funktionen

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]


#def prepare(): # Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.

def hitta_skalfaktor(skalbild_sokvag):
    json_fil = "scale_data.json"

    if os.path.isfile(json_fil):
        with open(json_fil, "r") as json_file:
            json_data = json.load(json_file)
            tidigare_faktor = json_data.get("faktor")

            if tidigare_faktor is not None:
                print(f"Tidigare faktor: {tidigare_faktor}")
                hittad_skalfaktor = testa_faktor(skalbild_sokvag, tidigare_faktor)

                if hittad_skalfaktor is not None:
                    return hittad_skalfaktor

    return utforska_skalfaktor(skalbild_sokvag)


def testa_faktor(skalbild_sokvag, faktor):
    for _ in range(3):
        while faktor >= 0.2:
            skalbild = Image.open(skalbild_sokvag)
            skalad_bild = skalbild.resize((int(skalbild.width * faktor), int(skalbild.height * faktor)))
            skalbild_array = np.array(skalad_bild)
            hittad_skalfaktor = pyautogui.locateOnScreen(skalbild_array, confidence=0.7, grayscale=True)

            if hittad_skalfaktor is not None:
                faktor = round(faktor, 1)
                data = {"faktor": faktor}
                with open("scale_data.json", "w") as json_file:
                    json.dump(data, json_file)
                return faktor

            print(".", end="", flush=True)
            time.sleep(0.5)

            faktor -= 0.02

    return None

hitta_skalfaktor("img/01_image.bmp")

with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]

#starmenu_area = None ### Jag vill ha den här funktionen, men den är inte helt bra just nu. dessutom måste jag ha en separat just för resurs/typ-fönster. De hamnar inte alltid på samma ställe....
def oppna_stjarna(bild_sokvag, faktor): # Definitionen måste ligga före anropet.
    hittad = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    time.sleep(1)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None: #klicka
        hittad = pyautogui.center(hittad_position)
        time.sleep(0.5)  # minskar fel
        pyautogui.moveTo(hittad)
        time.sleep(0.1) 
        pyautogui.mouseDown(2)
        pyautogui.mouseUp()
        time.sleep(4)  # minskar fel, starmenu tar ofta lång tid
        print(f"{bild_sokvag} klickad")
    else:
        print(f"{bild_sokvag} inte hittad") # Testfas

def hitta_bild_stjarna(bild_sokvag, faktor):
    #global starmenu_area
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None:
        # Om stjärnan hittas
        #x, y, bredd, hojd = hittad_position
        #starmenu_bredd = bredd * 10
        #starmenu_höjd = hojd * 7.5

        # Beräkna det begränsade området
      #  starmenu_x = x + int(bredd / 2) - int(starmenu_bredd / 2)
       # starmenu_y = y
        #starmenu_area = (starmenu_x, starmenu_y, starmenu_bredd, starmenu_höjd)

        time.sleep(0.5)  # Minskar antalet fel. 0.1 där det görs nya variabler o data, 3-4 mellan långsamma menyklick
        print("\nstjärnan öppen")

        # Utför nästa sökning inom det begränsade området
        ##hittad_position_ny = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True) #, region=starmenu_area)

    else:
        print(f"{bild_sokvag} inte hittad")
        oppna_stjarna("img/03_image.bmp", faktor) # Här öppnas stjärnan om stjärnmenyn inte hittats.
        
hitta_bild_stjarna("img/02_image.bmp", faktor)



with open("scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor
    data = json.load(json_file)
    faktor = data["faktor"]
    
def tab_stjarna(bild_sokvag, faktor):
    #global starmenu_area
    hittad = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array

    try:
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False) #, region=starmenu_area)
        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            time.sleep(0.5)  # minskar fel
            pyautogui.moveTo(hittad)
            time.sleep(0.1) 
            pyautogui.mouseDown(2)
            pyautogui.mouseUp()
            print(f"{bild_sokvag} klickad")
            time.sleep(1)  # minskar fel
    except:
        pass

tab_stjarna("img/04_image.bmp", faktor)

#
#   Nu börjar sökningen på riktigt, först läser vi in alla json
#


with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]

#
#   Finns en ide här om att pröva geolog vs explorer, för att köra båda i samma fil
#

with open("scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor
    data = json.load(json_file)
    faktor = data["faktor"]

flagga = True
def hitta_geolog(bild_sokvag, faktor):
    global flagga  # Använd nonlocal för att ändra flagga i den yttre funktionen
    #global starmenu_area
    hittad = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True) #, region=starmenu_area)

    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        time.sleep(1)  # minskar fel
        pyautogui.moveTo(hittad)
        time.sleep(0.1) 
        pyautogui.mouseDown(2)
        pyautogui.mouseUp()
        pyautogui.moveTo(200, 200) # För att bli av med popup-bubblan
        print(f"{bild_sokvag} klickad")
        time.sleep(3)
    else:
        flagga = False
        print(f"{bild_sokvag} inte hittad") #testfas
    return hittad

def leta_sten(): # Här bakar jag ihop för att (ev?) kunna välja explorer el geolog
    global flagga  # Använd global för att referera till den globala variabeln
    flagga = True
    for geolog in geologer:
        flagga = True  # Återställ flagga till True vid varje iteration
        while flagga == True: # Loopar geolog+resurs tills geologen inte hittas, därefter tar den nästa geolog och upprepar

            hittad_geolog = hitta_geolog(f"img/geo_{geolog}.bmp", faktor)
            if not hittad_geolog:
                flagga = False

            #hitta_geolog(f"img/geo_{geolog}.bmp", faktor)

            def hitta_resurs(bild_sokvag, faktor):
                for _ in range(3): # Loopa 3ggr
                    #global starmenu_area
                    bild = Image.open(bild_sokvag)
                    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True) #, region=starmenu_area)

                    if hittad_position is not None:
                        x, y, width, height = hittad_position # Klickar i högra hörnet för att kunna ha med texten brevid knappen
                        knappens_plats = x + width - (width // 5), y + (height // 2)
                        time.sleep(0.5)  # minskar fel
                        pyautogui.moveTo(knappens_plats)
                        time.sleep(0.1) 
                        pyautogui.mouseDown(2)
                        pyautogui.mouseUp()
                        pyautogui.moveTo(200, 200)
                        time.sleep(3)  # minskar fel
                        print(f"{bild_sokvag} klickad")
                        break
                    else:
                        print("resurs inte hittad")
                        time.sleep(1)

            hitta_resurs(f"img/resurs_{resurs}.bmp", faktor)

            def hitta_check(bild_sokvag, faktor):
                for _ in range(3): # Loopa 3ggr
                    hittad = None
                    time.sleep(1)
                    bild = Image.open(bild_sokvag)
                    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                    if hittad_position is not None:
                        hittad = pyautogui.center(hittad_position)
                        time.sleep(0.5)  # minskar fel
                        pyautogui.moveTo(hittad)
                        time.sleep(0.1) 
                        pyautogui.mouseDown(2)
                        pyautogui.mouseUp()
                        time.sleep(3)  # minskar fel
                        print(f"{bild_sokvag} klickad")
                        break
                    else:
                        print("check inte hittad")
                        time.sleep(1)


            hitta_check("img/check.png", faktor)



    leta_sten()
    print("Alla möjliga klick är genomförda.")

if __name__ == "__main__":
    app = QApplication([])
    miniprogram = ProgressDialog()
    #miniprogram.show()
    leta_sten()
    app.exec_()
    sys.exit()
