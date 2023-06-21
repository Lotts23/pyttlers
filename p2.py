import numpy as np
from PIL import Image
import pyautogui
import json
import p1

with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)

def hitta_bild(bild_sökväg):
    faktor = data["faktor"]
    bild = Image.open(bild_sökväg)

   
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad is not None:
        print(f"yeah, skala {faktor}")
        pyautogui.moveTo(hittad)
        return
    else:
        return p1.hitta_skalfaktor(bild_sökväg)

    return

# Kör sökningen med angiven bild
#hitta_bild("img/002_image.JPG")
