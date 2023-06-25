import time
import numpy as np
from PIL import Image
import pyautogui
import json

def hitta_skalfaktor(bild_sökväg):
    faktor = 1.0
    bild = Image.open(bild_sökväg)

    while faktor >= 0.05:
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad:
           # print(f"yeah, skala {faktor}")
           # pyautogui.moveTo(hittad)
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
