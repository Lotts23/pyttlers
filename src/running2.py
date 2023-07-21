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

with open("./src/nummer.json", "r") as json_file:
    data = json.load(json_file)
    explorers = data["explorers"]
    typ = data["typ"]  
    tid = data["tid"]
    
with open("./src/expl_namn.json", "r") as expl_file:
    expl_data = json.load(expl_file)
    expl_dict = expl_data
    
with open("./src/typ_namn.json", "r") as typ_file:
    typ_data = json.load(typ_file)
    typ_dict = typ_data    
    
with open("./src/tid_namn.json", "r") as tid_file:
    tid_data = json.load(tid_file)
    tid_dict = tid_data       

faktor = None
explorers_namn = [expl_dict[str(num)] for num in explorers]    
typ_namn = typ_dict[str(typ)] 
tid_namn = tid_dict[str(tid)] 
explorer = None
sovplats = 200, 200 # Bara för att alltid iallf ha nån giltlig sovplats - alltså där inga inforutor stör sökningen

try:
    with open("./src/scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]
except FileNotFoundError:
    faktor = 0.5

class ProgressDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pågår...")
        self.setFixedSize(350, 220)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Fönstret alltid överst

        self.setStyleSheet(open("./src/stil.css").read())  # Länk till stil.css

        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        self.setGeometry(QRect(screen_rect.width() - self.width(), 0, self.width(), self.height()))

        layout = QVBoxLayout(self)

        self.label = QLabel(self)
        explorers_str = ", ".join(explorers_namn)
        self.label.setText(f"Process pågår...\n\nSöker {explorers_str} som ska leta efter {typ_namn} under {tid_namn} tid.\n\nNödstopp genom att flytta musen till skärmens hörn.")
        self.label.setWordWrap(True)
        
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.restart_button = QPushButton("Upprepa", self)
        layout.addWidget(self.restart_button)
        self.restart_button.clicked.connect(self.start_process_again)
        
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
        leta_skatt()  # Starta leta_skatt-funktionen
        self.process_completed()
     
    def start_process_again(self):
        self.label.clear()
        explorers_str = ", ".join(explorers_namn)
        self.label.setText(f"Upprepar...\n\nSöker {explorers_str} som ska leta efter {typ_namn} under {tid_namn}.\n\nNödstopp genom att flytta musen till skärmens hörn.")
        self.label.setWordWrap(True)
        QApplication.processEvents()  # Uppdatera GUI-tråden
        leta_skatt()
        self.process_completed()
        
    def process_completed(self):
        self.label.setText("Processen är klar.\nAlla möjliga klick är genomförda.")
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.stop_process()
        else:
            super().keyPressEvent(event)


def hitta_skalfaktor(skalbild_sokvag):# Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.
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
            with open("./src/scale_data.json", "w") as json_file:
                json.dump(data, json_file)
            return faktor

        #print(".", end="", flush=True)
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
        hitta_skalfaktor("./src/img/01_image.bmp")
        return faktor

def prepare(): 
    json_fil = "./src/scale_data.json"
    global faktor
    faktor = None
    if os.path.isfile(json_fil):  # Om det finns en fil
        with open(json_fil, "r") as json_file:  # öppna den
            json_data = json.load(json_file)  # och läs datan
            faktor = json_data.get("faktor")  # Hämta tidigare faktor
        if faktor is not None: # Om faktor-värdet inte är tomt, testa det
            testa_skalfaktor("./src/img/01_image.bmp", faktor) # Testar om gamla faktorn funkar
            if faktor is None:
                hitta_skalfaktor("./src/img/01_image.bmp")
            else:
                #print("Tidigare skalfaktor accepterad")
                return faktor
    else:
        hitta_skalfaktor("./src/img/01_image.bmp")
    
prepare()# Kolla om tidigare faktor fortfarande funkar.

with open("./src/scale_data.json", "r") as json_file:
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
        #print("\nStjärnan öppen")
    else:
        oppna_stjarna("./src/img/03_image.bmp", faktor) # Här öppnas stjärnan om stjärnmenyn inte hittats.
        
hitta_bild_stjarna("./src/img/02_image.bmp", faktor) # Kör hitta om stjärnmenyn är öppen, else kör öppna stjärnan.

with open("./src/scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor, ja jäkligt onödigt men en del problem försvann. Tror man istället skulle kunna starta programmet med å rensa nån cache?
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

tab_stjarna("./src/img/04_image.bmp", faktor) # Gå till rätt tab så blir det inte så mycket scroll

def berakna_starmenu(bild_sokvag, faktor):   # Definierar starmenu_area för att söka på begränsad yta 
    global starmenu_area
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None: # Om stjärnan hittas
        x, y, bredd, hojd = hittad_position
        starmenu_bredd = bredd * 10.1
        starmenu_höjd = hojd * 8

        #Beräkna det begränsade området
        starmenu_x = x - int(starmenu_bredd / 2.1)
        starmenu_y = y + int(y / 8)
        starmenu_area = (starmenu_x, starmenu_y, round(starmenu_bredd), round(starmenu_höjd))    
        return starmenu_area
        
starmenu_area = berakna_starmenu("./src/img/02_image.bmp", faktor)

#
#   Nu börjar sökningen på riktigt, först läser vi in alla json
#

with open("./src/nummer.json", "r") as json_file:
    data = json.load(json_file)
    explorers = data["explorers"]
    typ = data["typ"]
    tid = data["tid"]

with open("./src/scale_data.json", "r") as json_file: # Ser till att vi läser in färsk faktor
    data = json.load(json_file)
    faktor = data["faktor"]

def hitta_scroll(bild_sokvag, faktor):
    global starmenu_area 
    hittad_position = None
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True, region=starmenu_area)
    
    if hittad_position is None:
        time.sleep(0.01)
        return False # inte hittad
    else:
        return True # hittad


def scroll(explorer):
    global explorers
    vimpel = False
    riktning = -2
    counting = 0
    while vimpel is False and explorer is not None: # När en viss explorer saknas
        individ = explorer
        hittad_explorer = hitta_scroll(f"./src/img/expl_{individ}.bmp", faktor)
        if hittad_explorer:
            vimpel = True
            return vimpel
        pyautogui.moveTo(sovplats)
        pyautogui.mouseDown(sovplats)
        pyautogui.mouseUp()
        pyautogui.scroll(riktning)
        counting += 1 # Håll reda på hur många scroll-sök
        if counting >= 15 and riktning == -2:
            riktning = 2
            counting = 0
        if counting >= 15 and riktning == 2:
            vimpel = False
            return None

def hitta_starmenu(bild_sokvag, faktor):
    hittad_starmenu = None
    global sovplats
    global explorers
    time.sleep(1)
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False)

    if hittad_position is not None:
        hittad_starmenu = pyautogui.center(hittad_position)
        time.sleep(0.1)
        x, y, width, height = starmenu_area
        sovplats = (x + width, y + (height / 3))
        time.sleep(0.1)
        pyautogui.mouseDown(hittad_starmenu)
        pyautogui.mouseUp()
        pyautogui.moveTo(sovplats)
        time.sleep(0.1)
        return sovplats
    else:
        time.sleep(1)
        return None

with open("./src/scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"] 

hitta_starmenu("./src/img/02_image.bmp", faktor)

def berakna_command(bild_sokvag, faktor): # Hitta sökområdet för typer och check.
    global command_area
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)
    if hittad_position is not None:
        x, y, bredd, hojd = hittad_position
        command_bredd = bredd * 8
        command_höjd = hojd * 15
        #Beräkna det begränsade området
        command_x = x + int(bredd / 2) - int(command_bredd / 2)
        command_y = y
        command_area = (command_x, command_y, round(command_bredd), round(command_höjd))
        return command_area
    else:
        return None

def hitta_typ(bild_sokvag, faktor):
    for _ in range(3):  # Loopa 3 gånger
        command_area = berakna_command("./src/img/05_image.bmp", faktor)
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        for _ in range(3):  # Loopa 3 gånger för varje försök
            hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.85, grayscale=True, region=command_area)     
            if hittad_position is not None:
                x, y, width, height = hittad_position  # Klickar i högra hörnet för att kunna ha med texten brevid knappen
                knappens_plats = x + width - (width // 5), y + (height // 2)
                pyautogui.moveTo(knappens_plats)
                time.sleep(0.1)
                pyautogui.mouseDown(knappens_plats)
                pyautogui.mouseUp()
                pyautogui.moveTo(sovplats)
                return True
            time.sleep(0.5)
    return False, command_area

def hitta_tid(bild_sokvag, faktor):
    for _ in range(3):  # Loopa 3 gånger
        command_area = berakna_command("./src/img/05_image.bmp", faktor)
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        for _ in range(3):  # Loopa 3 gånger för varje försök
            hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.9, grayscale=True, region=command_area)     
            if hittad_position is not None:
                x, y, width, height = hittad_position  # Klickar i högra hörnet för att kunna ha med texten brevid knappen
                knappens_plats = x + width - (width // 5), y + (height // 2)
                pyautogui.moveTo(knappens_plats)
                time.sleep(0.1)
                pyautogui.mouseDown(knappens_plats)
                pyautogui.mouseUp()
                pyautogui.moveTo(sovplats)
                return True
            time.sleep(0.1)
    return False, command_area

def hitta_check(bild_sokvag, faktor):
    global command_area
    for _ in range(3): # Loopa 3ggr
        hittad_check = None
        time.sleep(0.1)
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False, region=command_area)

        if hittad_position is not None:
            hittad_check = pyautogui.center(hittad_position)
            pyautogui.moveTo(hittad_check)
            pyautogui.mouseDown(hittad_check)
            pyautogui.mouseUp()
            pyautogui.moveTo(sovplats)
            pyautogui.mouseDown(sovplats)
            pyautogui.mouseUp()
            time.sleep(4)  # minskar fel ### Här vill jag istället använda en koll att den klickade specialisten ger sig iväg.
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
        pyautogui.mouseDown(error_found)
        time.sleep(0.1)
        pyautogui.press('esc')
        popup_flagga.set()
    time.sleep(0.1)

def hantera_popup():
    while not popup_flagga.is_set():
        error_bild("./src/img/error.png", faktor)

popup_flagga = threading.Event()      

def hitta_explorer(bild_sokvag, faktor):
    global flagga
    flagga = True
    global starmenu_area
    global sort
    if typ == 100:
        sort = "t"
    else:
        sort = "a"
    for _ in range(3): # Loopa 3ggr om den INTE hittar
        hittad = None
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        pyautogui.moveTo(sovplats)
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.77, grayscale=True, region=starmenu_area)
        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            pyautogui.moveTo(hittad)
            time.sleep(0.1) 
            pyautogui.mouseDown(hittad)
            pyautogui.mouseUp()
            pyautogui.moveTo(sovplats) # För att bli av med popup-bubblan
            popup_flagga.clear()
            popup_trad = threading.Thread(target=hantera_popup)
            popup_trad.start()
            time.sleep(0.1)
            hitta_typ(f"./src/img/typ_{typ}.bmp", faktor)
            popup_flagga.set()
            hitta_tid(f"./src/img/tid_{sort}_{tid}.bmp", faktor)
            hitta_check("./src/img/check.bmp", faktor)
            # Om den hittar en explorer längst bort på en rad, scrolla åt det hållet            
            h_x, h_y, h_width, h_height = hittad_position
            lower_corner_x, lower_corner_y = h_x + h_width, h_y + h_height # Av den hittade bilden
            upper_corner_x, upper_corner_y = h_x, h_y
            x, y, bredd, hojd = starmenu_area
            if lower_corner_x <= (x + (h_width * 1.9)) and lower_corner_y <= (y + (h_height * 1.9)):
                pyautogui.moveTo(sovplats)
                pyautogui.mouseDown(sovplats)
                pyautogui.mouseUp()
                pyautogui.scroll(2)
                time.sleep(0.1)
            if upper_corner_x >= (x + bredd - (h_width * 1.9)) and upper_corner_y >= (y + hojd - (h_height * 1.9)):
                pyautogui.moveTo(sovplats)
                pyautogui.mouseDown(sovplats)
                pyautogui.mouseUp()
                pyautogui.scroll(-2)
                time.sleep(0.1)
            flagga = True # Vi har hittat den     
        else:
            time.sleep(0.1) ### Else hitta command-bilden, hittas den så tryck esc, kontrollera att stjärnan är öppen och fortsätt.
            error_bild("./src/img/05_image.bmp", faktor)
            time.sleep(0.1)
            hitta_bild_stjarna("./src/img/02_image.bmp", faktor)
            
           
    return hittad # Om den hittats har hittad ett värde, annars none

def leta_skatt():
    global flagga
    global explorer
    global sovplats
    hitta = None
    flagga_funnen = False
    scroll(explorers[0])
    for explorer in explorers:
        flagga = True
        pyautogui.moveTo(sovplats)
        while flagga:
            hittad_explorer = hitta_explorer(f"./src/img/expl_{explorer}.bmp", faktor) # Returnerar hittad/none
            if hittad_explorer is not None:
                flagga_funnen = True
                flagga = True
            elif hittad_explorer is None and flagga_funnen is False: # En tidigare hittad explorer behöver inte sökas efter utöver när-scrollet i hitta_explorer
                hitta = scroll(explorer)
                if hitta is not None:
                    flagga = True # Upprepa hitta_explorer
                else:
                    flagga = False # Avbryt och börja leta efter nästa explorer.
            elif hittad_explorer is None and flagga_funnen is True:
                flagga = False # Avbryt direkt och gå vidare i listan.
             
def stop_program():
    app.quit()

def process_completed():
    miniprogram.process_completed()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    miniprogram = ProgressDialog()
    miniprogram.show()
    leta_skatt()
    miniprogram.process_completed()
    sys.exit(app.exec_())
