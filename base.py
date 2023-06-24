import json
import time

import numpy as np
import pyautogui
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
import keyboard


def prepare():
    def nödstopp():
        if keyboard.is_pressed('q'):
            print("Nödstopp!")
            exit()

    nödstopp()

    def hitta_skalfaktor(bild_sökväg):
        faktor = 1.0
        bild = Image.open(bild_sökväg)

        while faktor >= 0.05:
            skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
            bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
            hittad = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

            if hittad:
                pyautogui.moveTo(hittad)
                data = {"faktor": faktor}
                with open("scale_data.json", "w") as json_file:
                    json.dump(data, json_file)
                return faktor

            print(".", end="", flush=True)
            time.sleep(0.5)

            faktor -= 0.02

        return None

    hitta_skalfaktor("img/01_image.JPG")

    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    hittad = None
    open_stjarna = None

    def oppna_stjarna(bild_sökväg, faktor):
        global hittad

        bild = Image.open(bild_sökväg)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            time.sleep(0.1)  # minskar fel
            pyautogui.moveTo(hittad)
            pyautogui.click(duration=1)
            time.sleep(1)  # minskar fel
        else:
            hittad = None
            print(f"{bild_sökväg} inte hittad")
            hitta_skalfaktor("img/01_image.JPG")

    def hitta_bild_stjarna(bild_sökväg, faktor):
        global open_stjarna

        bild = Image.open(bild_sökväg)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            time.sleep(0.5)  # minskar antalet fel
            open_stjarna = pyautogui.center(hittad_position)
            print("stjärnan öppen")
        else:
            open_stjarna = None
            oppna_stjarna("img/03_image.JPG", faktor)

    hitta_bild_stjarna("img/02_image.JPG", faktor)

    with open("scale_data.json", "r") as json_file:
        data = json.load(json_file)
        faktor = data["faktor"]

    def tab_stjarna(bild_sökväg, faktor):
        global hittad
        time.sleep(1)  # minskar fel
        bild = Image.open(bild_sökväg)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=True)

        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            time.sleep(1)  # minskar fel
            pyautogui.moveTo(hittad)
            pyautogui.click(duration=1)
            time.sleep(0.5)  # minskar fel

    tab_stjarna("img/04_image.JPG", faktor)


prepare()

time.sleep(0.5)  # minskar fel
hittad = None  # Rensa minnet inför letningen

with open("nummer.json", "r") as json_file:
    data = json.load(json_file)
    geologer = data["geologer"]
    resurs = data["resurs"]


def leta_sten():
    for geolog in geologer:
        flagga = True
        while flagga:
            def hitta_geolog(bild_sökväg, faktor):
                global hittad

                bild = Image.open(bild_sökväg)
                skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                if hittad_position is not None:
                    flagga = True
                    hittad = pyautogui.center(hittad_position)
                    time.sleep(1)  # minskar fel
                    pyautogui.moveTo(hittad)
                    pyautogui.click(duration=1)
                else:
                    hittad = None
                    print(f"{bild_sökväg} inte hittad")
                    flagga = False

                return hittad

            hitta_geolog(f"img/{geolog}_image.JPG", faktor)

            def hitta_resurs(bild_sökväg, faktor):
                global hittad

                bild = Image.open(bild_sökväg)
                skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
                bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
                hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.7, grayscale=True)

                if hittad_position is not None:
                    hittad = pyautogui.center(hittad_position)
                    time.sleep(1)  # minskar fel
                    pyautogui.moveTo(hittad)
                    pyautogui.click(duration=1)
                    time.sleep(0.5)  # minskar fel
                else:
                    hittad = None
                    print("resurs inte hittad")
                    leta_sten()

                return hittad

            hitta_resurs(f"img/{resurs}_image.JPG", faktor)

            def hitta_check(bild_sökväg, faktor):
                global hittad

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
                    print("check inte hittad")
                    leta_sten()

                return hittad

            hitta_check("img/check.JPG", faktor)

            return


leta_sten()
