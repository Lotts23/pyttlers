import numpy as np
from PIL import Image
import pyautogui

def hitta_bild(bild_sökväg):
    faktor = float(0.4599999999999995)
    bild = Image.open(bild_sökväg)

   
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    if hittad is not None:
        print(f"yeah, skala {faktor}")
        pyautogui.moveTo(hittad)
        return faktor

    return

# Kör sökningen med angiven bild
hitta_bild("img/004_image.JPG")
