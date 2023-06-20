import pyautogui
from PIL import Image

def leta_bild(hittad_sökväg, confidence):
    bild = Image.open(hittad_sökväg)
    faktor = (1)
    bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
  
    hittad = pyautogui.locateOnScreen(bild, confidence=confidence, grayscale=True)

    print("Bild hittad!" if hittad else "Ingen matchande bild hittades.")

# Kör sökningen med angiven bild och tröskelvärde
leta_bild("img/004_image.JPG", 0.8)
