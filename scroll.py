import json
import time
import numpy as np
import pyautogui
from PIL import Image

def hitta_scroll(bild_sokvag, faktor):
    hittad_check = None
    hittad_position = None
    time.sleep(1)
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)
    
    while hittad_position is None:
        pyautogui.scroll(-2)
        print(f"Check inte hittad, faktor: {faktor}")
        time.sleep(1)
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

    hittad_check = pyautogui.center(hittad_position)
    time.sleep(1)
    x, y = hittad_check
    time.sleep(0.1)
    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    print("hittad")


def hitta_check(bild_sokvag, faktor):
    hittad_check = None
    time.sleep(1)
    bild = Image.open(bild_sokvag)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False)

    if hittad_position is not None:
        hittad_check = pyautogui.center(hittad_position)
        time.sleep(1)
        x, y = hittad_check
        time.sleep(0.1)
        pyautogui.mouseDown(x, y)
        pyautogui.mouseUp()
        pyautogui.moveTo(x + 100, y + 100)
        time.sleep(0.5)
        print("scrollar...")
        hitta_scroll("img/geo_10.bmp", faktor)
    else:
        print("Stjärnmeny inte hittad")
        time.sleep(1)


with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]

hitta_check("img/02_image.bmp", faktor)
