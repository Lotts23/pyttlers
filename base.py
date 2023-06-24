import json
import time

import numpy as np
import pyautogui
from PIL import Image


def hitta_skalfaktor(bild_sökväg):
    faktor = 1.0
    bild = Image.open(bild_sökväg)

    while faktor >= 0.05:
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad:
            data = {"faktor": faktor}
            with open("scale_data.json", "w") as json_file:
                json.dump(data, json_file)
            return faktor

        print(".", end="", flush=True)
        time.sleep(0.001)

        faktor -= 0.02

    return 

# Kör sökningen med angiven bild
hitta_skalfaktor("img/01_image.JPG")

with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]

hittad = None # Nollställer innan loopen börjar

def hitta_bild(bild_sökväg, faktor):
    #global hittad  # Använd global för att ändra värdet på den globala variabeln


    bild = Image.open(bild_sökväg)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        pyautogui.moveTo(hittad)
        pyautogui.click(duration=1)
    else:
        hittad = None
        print("bild inte hittad")

    return hittad

hitta_bild("img/02_image.JPG", faktor)