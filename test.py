import json
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
import keyboard

time.sleep(0.5)  # minskar fel
hittad = None  # Rensa minnet inför letningen
flagga = True
with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]


# läser värdet som faktor i json
with open("scale_data.json", "r") as json_file:
    data = json.load(json_file)
    faktor = data["faktor"]


def leta_sten():
    global flagga
    for geolog in geologer:
        flagga = True
        while flagga:
            hittad_geolog = hitta_geolog(f"img/{geolog}_geo.JPG", faktor)
            if hittad_geolog is None:
                print(f"{geolog} inte hittad")
                flagga = False
                break

            hittad_resurs = hitta_resurs(f"img/{resurs}_.JPG", faktor)
            if hittad_resurs is None:
                print("resurs inte hittad")
                flagga = False
                break

            hitta_check("img/check.JPG", faktor)

            return

def hitta_geolog(bild_sökväg, faktor):
    global hittad

    bild = Image.open(bild_sökväg)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

    if hittad_position is not None:
        flagga = True
        hittad = pyautogui.center(hittad_position)
        time.sleep(1)
        pyautogui.moveTo(hittad)
        pyautogui.click(duration=1)
    else:
        hittad = None
        print(f"{bild_sökväg} inte hittad")
        flagga = False

    return hittad

def hitta_resurs(bild_sökväg, faktor):
    global hittad

    bild = Image.open(bild_sökväg)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        time.sleep(1)
        pyautogui.moveTo(hittad)
        pyautogui.click(duration=1)
        time.sleep(0.5)
    else:
        hittad = None
        print("resurs inte hittad")
        leta_sten()

    return hittad

def hitta_check(bild_sökväg, faktor):
    global hittad

    bild = Image.open(bild_sökväg)
    skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
    bild_array = np.array(skalad_bild)
    hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=False)

    if hittad_position is not None:
        hittad = pyautogui.center(hittad_position)
        time.sleep(1)
        pyautogui.moveTo(hittad)
        pyautogui.click(duration=1)
        time.sleep(0.5)
    else:
        hittad = None
        print("check inte hittad")
        leta_sten()

    return hittad

leta_sten()