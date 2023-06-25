import json
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

def prepare(): # Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.

    def hitta_skalfaktor(skalbild_sokvag): # Som det låter, vi kollar skalan
        faktor = 1 # Vi kan börja med faktor 2 också och först skala upp bilden, med sämre resultat och längre tid
        skalbild = Image.open(skalbild_sokvag)

        while faktor >= 0.2: # Den behöver aldrig pröva mindre än så här. Om faktor 1 är 200% i spelet så är 0.2 20% och spelet går bara ner till 50%
            skalad_bild = skalbild.resize((int(skalbild.width * faktor), int(skalbild.height * faktor)))
            skalbild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
            hittad_skalfaktor = pyautogui.locateOnScreen(skalbild_array, confidence=0.7, grayscale=True)

            if hittad_skalfaktor is not None:
                pyautogui.moveTo(hittad_skalfaktor)
                data = {"faktor": faktor}
                with open("scale_data.json", "w") as json_file: # Skriv i json
                    json.dump(data, json_file)
                return faktor

            print(".", end="", flush=True)
            time.sleep(0.1) # Vid många fel kan denna ökas.

            faktor -= 0.02 # Lägre tal ger större nogrannhet i sökningen.

        return None

    hitta_skalfaktor("img/01_image.JPG")

    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    def oppna_stjarna(bild_sokvag, faktor):
        hittad = None
        bild = Image.open(bild_sokvag)
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
            time.sleep(0.2)  # minskar antalet fel
            print("stjärnan öppen")
        else:
            oppna_stjarna("img/03_image.JPG", faktor) # Här öppnas stjärnan om stjärnmenyn inte hittats.

    hitta_bild_stjarna("img/02_image.JPG", faktor) # Detta är den öppna stjärnmenyn, om den hittas går vi vidare, annars öppnas stjärnan

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
                time.sleep(0.5)  # minskar fel
        except:
            pass

    tab_stjarna("img/04_image.JPG", faktor)
prepare() # Kör hela ovanstående förberedelser inför att ta tag i uppdraget

    
time.sleep(0.5)  # minskar fel

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]

flagga = True  # Deklarera flagga som en global variabel här

def leta_sten():
    global flagga  # Använd global för att referera till den globala variabeln

    for geolog in geologer:
        flagga = True  # Återställ flagga till True vid varje iteration

        while flagga:
            def hitta_geolog(bild_sokvag, faktor):
                nonlocal flagga  # Använd nonlocal för att ändra flagga i den yttre funktionen

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
                else:
                    flagga = False
                    print(f"{bild_sokvag} inte hittad")
                    

                return hittad

            hittad_geolog = hitta_geolog(f"img/{geolog}_image.JPG", faktor)
            if not hittad_geolog:
                flagga = False

            hitta_geolog(f"img/{geolog}_image.JPG", faktor)

            def hitta_resurs(bild_sokvag, faktor):
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
                    time.sleep(0.5)  # minskar fel
                else:
                    hittad = None
                    print("resurs inte hittad")

                return 

            hitta_resurs(f"img/{resurs}_image.JPG", faktor)

            def hitta_check(bild_sokvag, faktor):
                hittad = None

                bild = Image.open(bild_sokvag)
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
                    print("check inte hittad")
                 

            hitta_check("img/check.JPG", faktor)

            

leta_sten()
print("Alla möjliga klick är genomförda.")