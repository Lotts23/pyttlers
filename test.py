import json
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
import keyboard

# läser värdet som faktor i json
with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]

def hitta_check(bild_sökväg, faktor):
    global hittad  # Använd global för att ändra värdet på den globala variabeln

    bild = Image.open(bild_sökväg)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=False)

    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        time.sleep(1)  # minskar fel
        pyautogui.moveTo(hittad)  
        pyautogui.click(duration=1)
        time.sleep(0.5)  # minskar fel
    else:
        hittad = None
        print("tab inte hittad")


    return hittad
hitta_check("img/04_image.JPG", faktor)