import json
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
import keyboard


def prepare():

    def nödstopp():
        if keyboard.is_pressed('q'):
            print("Nödstopp!")
            exit()
    nödstopp()        
    # Först fastställer vi skalan på spelet
    def hitta_skalfaktor(bild_sökväg):
        faktor = 1.0
        bild = Image.open(bild_sökväg)

        while faktor >= 0.05:
            skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
            bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
            hittad = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

            if hittad:
                pyautogui.moveTo(hittad)  
                data = {"faktor": faktor}
                with open("scale_data.json", "w") as json_file:
                    json.dump(data, json_file)
                return faktor

            print(".", end="", flush=True)
            time.sleep(0.5)

            faktor -= 0.02

        return None

    # Kör sökningen efter skala med samma bild alltid
    hitta_skalfaktor("img/01_image.JPG")

    # läser värdet som faktor i json
    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    # Först måste vi se till att rätt fönster är öppnat, annars öppna det (stjärnan)

    hittad = None  # Nollställer innan loopen börjar
    open_stjarna = None  # Kollar om stjärnfönstret är öppet
    def oppna_stjarna(bild_sökväg, faktor):
        global hittad  # Använd global för att ändra värdet på den globala variabeln

        bild = Image.open(bild_sökväg)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            time.sleep(0.1)  # minskar fel
            pyautogui.moveTo(hittad)  
            pyautogui.click(duration=1)
            time.sleep(1)  # minskar fel
        else:
            hittad = None
            print("bild inte hittad")
            hitta_skalfaktor("img/01_image.JPG")  # kolla skalan igen om nåt går fel
            # FÖrsök öppna stjärnan igen men utan att skapa oändlig loop
        return hittad
    def hitta_bild_stjarna(bild_sökväg, faktor):
        global open_stjarna  # Använd global för att ändra värdet på den globala variabeln

        bild = Image.open(bild_sökväg)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            time.sleep(0.5)  # minskar antalet fel
            open_stjarna = pyautogui.center(hittad_position)
            print("stjärnan öppen")
        else:
            open_stjarna = None
            oppna_stjarna("img/03_image.JPG", faktor)  # då letar vi upp och klickar på denna bilden som öppnar stjärnan.
    hitta_bild_stjarna("img/02_image.JPG", faktor)  # Denna bild är bara synlig om stjärnfönstret är öppet. Om fönstret är öppet så går vi vidare, annars ska vi söka efter och klicka:

    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    #kontrollerar att vi är i rätt tab på stjärnan:
    def tab_stjarna(bild_sökväg, faktor):
        global hittad  # Använd global för att ändra värdet på den globala variabeln

        bild = Image.open(bild_sökväg)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            time.sleep(0.1)  # minskar fel
            pyautogui.moveTo(hittad)  # det går alltid att klicka på tabbem, även om den redan är vald
            pyautogui.click(duration=1)
            time.sleep(0.5)  # minskar fel
        else:
            hittad = None
            print("bild inte hittad")
            hitta_skalfaktor("img/01_image.JPG")  # kolla skalan igen om nåt går fel
            #och här ska vi öppna geo.py istället för att omstarta sökningen
        return hittad
    tab_stjarna("img/04_image.JPG") # Det här ska vara tabben

    
time.sleep(0.5)  # minskar fel        
hittad = None # Rensa minnet inför letningen    

#läs in data från nummer.json
with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]


# Här börjar leta-stenfunktionen  
for geolog in geologer:
    flagga = True
    while flagga:   
        app = QApplication([])  # Skapa en QApplication-instans    
        def leta_sten():     
            while True:
                def hitta_bild(bild_sökväg, faktor):
                    global hittad  # Använd global för att ändra värdet på den globala variabeln

                    bild = Image.open(bild_sökväg)
                    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                    if hittad_position is not None:
                        flagga = True
                        hittad = pyautogui.center(hittad_position)
                        time.sleep(1)  # minskar fel
                        pyautogui.moveTo(hittad)  
                        pyautogui.click(duration=1)
                    else:
                        hittad = None
                        print("bild inte hittad")
                        flagga = False

                    return hittad
                hitta_bild(f"img/{geolog}_image.JPG", faktor)

                def hitta_bild(bild_sökväg, faktor):
                    global hittad  # Använd global för att ändra värdet på den globala variabeln

                    bild = Image.open(bild_sökväg)
                    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                    if hittad_position is not None:
                        hittad = pyautogui.center(hittad_position)
                        time.sleep(1)  # minskar fel
                        pyautogui.moveTo(hittad)  
                        pyautogui.click(duration=1)
                        time.sleep(0.5)  # minskar fel
                    else:
                        hittad = None
                        print("sten inte hittad")
                        leta_sten()

                    return hittad
                hitta_bild(f"img/{resurs}_image.JPG", faktor)

                def hitta_bild(bild_sökväg, faktor):
                    global hittad  # Använd global för att ändra värdet på den globala variabeln

                    bild = Image.open(bild_sökväg)
                    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=False)

                    if hittad_position is not None:
                        hittad = pyautogui.center(hittad_position)
                        time.sleep(1)  # minskar fel
                        pyautogui.moveTo(hittad)  
                        pyautogui.click(duration=1)
                        time.sleep(0.5)  # minskar fel
                    else:
                        hittad = None
                        print("check inte hittad")
                        leta_sten()

                    return hittad
                hitta_bild("img/check.JPG", faktor)
                # Här slutar leta sten-funktionen
                
                svar = QMessageBox.question(None, "En geolog till?", "Vill du ha en till geolog?", QMessageBox.Yes | QMessageBox.No)
                if svar == QMessageBox.No:
                    break  # Avsluta loopen om användaren svarar "Nej"

            return
        leta_sten()
        app.exec()  # Starta händelseloopen för PyQt5-applikationen


