import numpy as np
from PIL import Image
import pyautogui
import json

hittad = None

def hitta_bild(bild_sökväg, faktor):
    global hittad  # Använd global för att ändra värdet på den globala variabeln
    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    bild = Image.open(bild_sökväg)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        print(f"Specialisten har hittats på position {hittad}")
    else:
        hittad = None

    return hittad
