import json
import os
import sys
import threading
import time

import cv2
import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtCore import QEvent, QRect, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QLabel,
                             QPushButton, QVBoxLayout, qApp)

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]  
    
with open("geo_namn.json", "r") as geo_file:
    geo_data = json.load(geo_file)
    geo_dict = geo_data
    
with open("resurs_namn.json", "r") as resurs_file:
    resurs_data = json.load(resurs_file)
    resurs_dict = resurs_data    

faktor = None
geologer_namn = [geo_dict[str(num)] for num in geologer]    
resurs_namn = resurs_dict[str(resurs)] 
geolog = None
try:
    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]
except FileNotFoundError:
    faktor = 0.5

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pågår...")
        self.setFixedSize(350, 200)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Fönstret alltid överst

        self.setStyleSheet(open("stil.css").read())  # Länk till stil.css

        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        self.setGeometry(QRect(screen_rect.width() - self.width(), 0, self.width(), self.height()))

        layout = QVBoxLayout(self)

        self.label = QLabel(self)
        geologer_str = ", ".join(geologer_namn)
        self.label.setText(f"Process pågår...\n\nSöker {geologer_str} som ska leta efter {resurs_namn}.\n\nNödstopp genom att flytta musen till skärmens hörn.")
        self.label.setWordWrap(True)
        
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.restart_button = QPushButton("Upprepa", self)
        layout.addWidget(self.restart_button)
        self.restart_button.clicked.connect(self.start_process)
        
        self.stop_action = QAction("Avsluta (q)", self)
        self.stop_action.setShortcut(QKeySequence("q"))
        self.stop_action.triggered.connect(self.stop_process)
        self.addAction(self.stop_action)

        self.stop_button = QPushButton("Avsluta", self)
        layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_process)

    def stop_process(self):
        self.close()  # Stäng minifönstret och avbryt processen
        qApp.quit()  # Avsluta programmet

    def start_process(self):
        #self.hide()  # Göm minifönstret
        leta_sten()  # Starta leta_sten-funktionen
        self.process_completed()
        
    def process_completed(self):
        self.label.setText("Processen är klar.\nAlla möjliga klick är genomförda.")
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.stop_process()
        else:
            super().keyPressEvent(event)


# Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.
def hitta_skalfaktor(skalbild_sokvag):
    tillatna_varden = [0.25, 0.375, 0.45, 0.5, 0.55, 0.625, 0.75, 1]
    global faktor
    faktor = faktor
    for faktor in tillatna_varden:
        skalbild = Image.open(skalbild_sokvag)
        skalad_bild = skalbild.resize((int(skalbild.width * faktor), int(skalbild.height * faktor)))
        skalbild_array = np.array(skalad_bild)
        hittad_skalfaktor = pyautogui.locateOnScreen(skalbild_array, confidence=0.7, grayscale=True)
        if hittad_skalfaktor is not None:
            data = {"faktor": faktor}
            with open("scale_data.json", "w") as json_file:
                json.dump(data, json_file)
            return faktor

        print(".", end="", flush=True)
        time.sleep(0.01)

    return #tillatna_varden[3]  # Returnera 100% om ingen match hittades

def testa_skalfaktor(skalbild_sokvag, faktor):
    testbild = Image.open(skalbild_sokvag)
    testad_bild = testbild.resize((int(testbild.width * faktor), int(testbild.height * faktor)))
    testbild_array = np.array(testad_bild)
    hittad_testbild = pyautogui.locateOnScreen(testbild_array, confidence=0.8, grayscale=True)

    if hittad_testbild is not None:
        return faktor
    else:
        hitta_skalfaktor("img/01_image.bmp")
        return faktor

def prepare(): # Kolla om tidigare faktor fortfarande funkar.
    json_fil = "scale_data.json"
    global faktor
    faktor = None
    if os.path.isfile(json_fil):  # Om det finns en fil
        with open(json_fil, "r") as json_file:  # öppna den
            json_data = json.load(json_file)  # och läs datan
            faktor = json_data.get("faktor")  # Hämta tidigare faktor
        if faktor is not None: # Om faktor-värdet inte är tomt, testa det
            testa_skalfaktor("img/01_image.bmp", faktor) # Testar om gamla faktorn funkar
            if faktor is None:
                hitta_skalfaktor("img/01_image.bmp")
            else:
                #print("Tidigare skalfaktor accepterad")
                return faktor
    else:
        hitta_skalfaktor("img/01_image.bmp")
    
prepare()

with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]
    #print(faktor)

def oppna_stjarna(bild_sokvag, faktor): # Definitionen måste ligga före anropet.
    hittad = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    #print(skalad_bild)
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    time.sleep(1)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None: #klicka
        hittad = pyautogui.center(hittad_position)
        time.sleep(0.5)  # minskar fel
        pyautogui.moveTo(hittad)
        time.sleep(0.1) 
        pyautogui.mouseDown(hittad)
        pyautogui.mouseUp()
        time.sleep(4)  # minskar fel, starmenu tar ofta lång tid
        #print(f"{bild_sokvag} klickad")
    #else:
        #print(f"{bild_sokvag} inte hittad") # Testfas

def hitta_bild_stjarna(bild_sokvag, faktor):    # kolla om stjärnmeny Else öppna stjärna
    #global starmenu_area
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None:
        time.sleep(0.1)  # Minskar antalet fel. 0.1 där det görs nya variabler o data, 3-4 mellan långsamma menyklick
        print("\nStjärnan öppen")
    else:
        oppna_stjarna("img/03_image.bmp", faktor) # Här öppnas stjärnan om stjärnmenyn inte hittats.
        
hitta_bild_stjarna("img/02_image.bmp", faktor) # Kör hitta om stjärnmenyn är öppen, else kör öppna stjärnan.

with open("scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor, ja jäkligt onödigt men en del problem försvann. Tror man istället skulle kunna starta programmet med å rensa nån cache?
    data = json.load(json_file)
    faktor = data["faktor"]
 
def tab_stjarna(bild_sokvag, faktor): 
    hittad = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True) #, region=starmenu_area)
    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        time.sleep(0.1)  # minskar fel
        pyautogui.moveTo(hittad)
        time.sleep(0.1) 
        pyautogui.mouseDown(hittad)
        pyautogui.mouseUp()
        #print(f"{bild_sokvag} klickad")
        time.sleep(1)  # minskar fel

tab_stjarna("img/04_image.bmp", faktor)

# Definierar starmenu_area
def berakna_starmenu(bild_sokvag, faktor):    
    global starmenu_area
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None: #Om stjärnan hittas
        x, y, bredd, hojd = hittad_position
        starmenu_bredd = bredd * 11
        starmenu_höjd = hojd * 8.8

        #Beräkna det begränsade området
        starmenu_x = x + int(bredd / 2) - int(starmenu_bredd / 2)
        starmenu_y = y
        starmenu_area = (starmenu_x, starmenu_y, round(starmenu_bredd), round(starmenu_höjd))
        return starmenu_area
        
starmenu_area = berakna_starmenu("img/02_image.bmp", faktor)

#
#   Nu börjar sökningen på riktigt, först läser vi in alla json
#

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]

with open("scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor
    data = json.load(json_file)
    faktor = data["faktor"]

rad = 0



def hitta_scroll(bild_sokvag, faktor):
    global starmenu_area 
    global individ
    hittad_position = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True, region=starmenu_area)
    
    if hittad_position is None:
        time.sleep(0.01)
        return False
    else:
        return True

def scroll(geolog):
    global geologer
    global individ
    geolog_index = 0
    vimpel = False
    riktning = -2
    counting = 0
    if geolog is not None: # Om vi ska leta efter en speciell geolog
        individ = geolog
        hittad_geolog = hitta_scroll(f"img/geo_{individ}.bmp", faktor)
        if hittad_geolog:
            vimpel = True 
        while vimpel is False and geolog is not None:
            pyautogui.scroll(riktning)
            hittad_geolog = hitta_scroll(f"img/geo_{individ}.bmp", faktor)
            counting += 1 # Håll reda på hur många scroll-sök
            if hittad_geolog:
                vimpel = True
                break
            if counting >= 11 and riktning == -2:
                riktning = 2
                counting = 0
            if counting >= 11 and riktning == 2:
                geolog = None
        
    while vimpel is False and geolog is None: # Och vi inte söker efter nån särskilld.
        for _ in range(len(geologer)):
            individ = geologer[geolog_index]
            hittad_geolog = hitta_scroll(f"img/geo_{individ}.bmp", faktor)
            if hittad_geolog:
                vimpel = True
                break    
            geolog_index = (geolog_index + 1) % len(geologer)
        counting += 1
        pyautogui.scroll(riktning) # Scrollar neråt
        if counting >= 11 and riktning == -2:
            riktning = 2
            counting = 0
        if counting >= 11 and riktning == 2:
            break



sovplats = 200, 200 # Bara för att alltid iallf ha nån giltlig sovplats - alltså där inga inforutor stör sökningen
rad = 0

def hitta_starmenu(bild_sokvag, faktor):
    hittad_starmenu = None
    global sovplats
    global geologer
    time.sleep(1)
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False)

    if hittad_position is not None:
        hittad_starmenu = pyautogui.center(hittad_position)
        time.sleep(0.1)
        x, y, width, height = starmenu_area
        sovplats = (x + width - 40, y + 100)
        time.sleep(0.1)
        pyautogui.mouseDown(hittad_starmenu)
        pyautogui.mouseUp()
        pyautogui.moveTo(sovplats)
        #scroll() 
        return sovplats
    else:
        #print("Stjärnmeny inte hittad")
        time.sleep(1)
        return None

with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"] 

hitta_starmenu("img/02_image.bmp", faktor)

def berakna_command(bild_sokvag, faktor): # Hitta sökområdet för resurser och check.
    global command_area
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None: #Om stjärnan hittas
        x, y, bredd, hojd = hittad_position
        command_bredd = bredd * 5
        command_höjd = hojd * 10

        #Beräkna det begränsade området
        command_x = x + int(bredd / 2) - int(command_bredd / 2)
        command_y = y
        command_area = (command_x, command_y, round(command_bredd), round(command_höjd))
        return command_area

print(f"Process pågår...\nSöker {', '.join(geologer_namn)} som ska leta efter {resurs_namn}")


def hitta_resurs(bild_sokvag, faktor):
    for _ in range(3): # Loopa 3ggr
        command_area = berakna_command("img/05_image.bmp", faktor)
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.85, grayscale=False, region=command_area)

        if hittad_position is not None:
            x, y, width, height = hittad_position # Klickar i högra hörnet för att kunna ha med texten brevid knappen
            knappens_plats = x + width - (width // 5), y + (height // 2)
            pyautogui.moveTo(knappens_plats)
            time.sleep(0.1) 
            pyautogui.mouseDown(knappens_plats)
            pyautogui.mouseUp()
            pyautogui.moveTo(sovplats)
            #print(f"{bild_sokvag} klickad")
            return True
        else:
            time.sleep(0.1)

def hitta_check(bild_sokvag, faktor):
    for _ in range(3): # Loopa 3ggr
        hittad_check = None
        time.sleep(0.1)
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False)

        if hittad_position is not None:
            hittad_check = pyautogui.center(hittad_position)
            pyautogui.moveTo(hittad_check)
            pyautogui.mouseDown(hittad_check)
            pyautogui.mouseUp()
            time.sleep(4)  # minskar fel
            #print(f"{bild_sokvag} klickad")
            break
        else:
            time.sleep(0.1)

def error_bild(bild_sokvag, faktor):
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    bild_array = cv2.cvtColor(bild_array, cv2.COLOR_RGB2BGR)
    error_found = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False)
    if error_found is not None:
        pyautogui.press('esc')
        popup_flagga.set()
    
def hantera_popup():
    while not popup_flagga.is_set():
        error_bild("img/error.png", faktor)

popup_flagga = threading.Event()        
def hitta_geolog(bild_sokvag, faktor):
    global flagga
    flagga = True
    global starmenu_area
    #global geolog
    #global rad
    
    for _ in range(3): # Loopa 3ggr om den inte hittar
        hittad = None
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.77, grayscale=True, region=starmenu_area)

        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            pyautogui.moveTo(hittad)
            time.sleep(0.1) 
            pyautogui.mouseDown(hittad)
            pyautogui.mouseUp()
            pyautogui.moveTo(sovplats) # För att bli av med popup-bubblan
            time.sleep(0.1)
            
            hitta_resurs(f"img/resurs_{resurs}.bmp", faktor)
            hitta_check("img/check.bmp", faktor)

            x, y, width, height = hittad_position
            area_width, area_height = starmenu_area[2], starmenu_area[3]
            if x + width >= starmenu_area[0] + area_width - (width * 2) and y + height >= starmenu_area[1] + area_height - (height * 2):
                pyautogui.moveTo(sovplats)
                pyautogui.scroll(-2)
                #hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.77, grayscale=True, region=starmenu_area)
            if x + width <= starmenu_area[0] - (width * 2) and y + height <= starmenu_area[1] - (height * 3):
                pyautogui.moveTo(sovplats)
                pyautogui.scroll(2)
                #hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.77, grayscale=True, region=starmenu_area)                
        else:
            flagga = False
            time.sleep(0.1)
            
    return hittad
"""         rad = rad + 1
            #print(rad)
            if rad >= 9: # En rad rymmer 9 specialister, scrolla sedan en rad ner.
                pyautogui.scroll(-2)
                rad = 0 """

def leta_sten(): # Här bakar jag ihop för att (ev?) kunna välja explorer el geolog senare
    global flagga  
    global geolog
    global sovplats
    
    for geolog in geologer:
        flagga = True
        while flagga:
            hittad_geolog = hitta_geolog(f"img/geo_{geolog}.bmp", faktor)
            popup_flagga.clear()
            popup_trad = threading.Thread(target=hantera_popup)
            popup_trad.start()
            if not hittad_geolog:
                pyautogui.moveTo(sovplats)
                pyautogui.mouseDown(sovplats)
                pyautogui.mouseUp()
                scroll(geolog)
                hittad_geolog = hitta_geolog(f"img/geo_{geolog}.bmp", faktor)
                for geolog_inre in geologer:
                    hittad_geolog_inre = hitta_geolog(f"img/geo_{geolog_inre}.bmp", faktor)
                    if not hittad_geolog_inre:
                        flagga = False
                        break
        if geolog == geologer[-1]:
            hittad_sista_geolog = hitta_geolog(f"img/geo_{geolog}.bmp", faktor)
            if not hittad_sista_geolog:
                flagga = False
                popup_flagga.set()
                break                    
    return geolog

#leta_sten() # Används bara när koden testas.

def stop_program():
    app.quit()

def process_completed():
    miniprogram.process_completed()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    miniprogram = ProgressDialog()
    miniprogram.show()
    geolog = leta_sten()
    miniprogram.process_completed()
    sys.exit(app.exec_())