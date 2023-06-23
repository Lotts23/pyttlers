import json
from p1 import hitta_skalfaktor
from p2 import hitta_bild
import pyautogui

def main():
    with open("nummer.json", "w") as f:
        json.dump({}, f)  # Skriv över filen med en tom dictionary

    p1()

def p1():
    faktor = hitta_skalfaktor("img/01_image.JPG")
    print(f"Skalfaktor hittad: {faktor}")

    with open('nummer.json', 'r') as f:
        data = json.load(f)

    tresiffrigt_nummer = data['tresiffrigt']
    resurs = ""

    if tresiffrigt_nummer:
        resurs = f"img/{tresiffrigt_nummer}_image.JPG"
        hittad_bild = hitta_bild(resurs, faktor)

        if hittad_bild:
            print("Specialisten hittad")
            pyautogui.moveTo(hittad_bild)
            pyautogui.mouseDown()
            pyautogui.mouseUp()
        else:
            print("Ingen bild hittad för det tresiffriga numret")

    for num in data['tvåsiffriga']:
        bild_adress = f"img/{num}_image.JPG"
        hittad_bild = hitta_bild(bild_adress, faktor)

        if hittad_bild:
            print("Resurs hittad")
            pyautogui.moveTo(hittad_bild)
            pyautogui.mouseDown()
            pyautogui.mouseUp()

            if resurs:
                resurs_bild_adress = f"img/{resurs}"
                hittad_resurs = hitta_bild(resurs_bild_adress, faktor)

                if hittad_resurs:
                    print(f"Resurs {resurs} hittad")
                    pyautogui.moveTo(hittad_resurs)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                else:
                    print(f"Ingen bild hittad för {resurs}")
        else:
            print(f"Ingen bild hittad för {bild_adress}")

    print("Klar")

if __name__ == "__main__":
    main()
