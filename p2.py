from PIL import Image
import pyautogui

def hitta_bild(bild_sökväg, faktor, *confidence):
    bild = Image.open(bild_sökväg)
    skalad_bild_objekt = bild.resize((int(bild.width * faktor), int(bild.width * faktor)))
    hittad = pyautogui.locateOnScreen(skalad_bild_objekt, *confidence, grayscale=True)

    if hittad:
        print(f"Bild {bild_sökväg} hittad! Skala {faktor}")
    else:
        print(f"Ingen matchande bild hittades för {bild_sökväg} med skala {faktor}.")


# Kör sökningen med angiven bild och tröskelvärde
# hitta_bild("img/02_image.JPG", 0.8)
