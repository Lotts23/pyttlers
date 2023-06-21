import numpy as np
from PIL import Image
import pyautogui
import json

with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]

def hitta_bild(bild_sökväg, faktor):
    faktor = data["faktor"]
    bild = Image.open(bild_sökväg)

   
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    #if hittad is not None:
        #print(f"specialisten har skala {faktor}")
    return hittad



# Kör sökningen med angiven bild
#hitta_bild("img/002_image.JPG")
