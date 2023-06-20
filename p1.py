from PIL import Image
import pyautogui

def hitta_skalfaktor(bild_sökväg, *confidence):
    faktor = int(1.0)
    bild = Image.open(bild_sökväg)

    while faktor >= 0.2:
        skalad_bild_objekt = bild.resize((int(bild.width * faktor), int(bild.width * faktor)))
        hittad = pyautogui.locateOnScreen(skalad_bild_objekt, *confidence, grayscale=True)

        if hittad:
            print(f"Bild {bild_sökväg} hittad! Skala {faktor}")
            return faktor

        print(".", end="", flush=True)
        faktor -= 0.05

    return


# Kör sökningen med angiven bild och tröskelvärde
hitta_skalfaktor("img/01_image.JPG", 0.8)
print(f"Bild {bild_sökväg} hittad! Skala {faktor}")
