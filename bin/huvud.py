from p1 import hitta_skalfaktor
from p2 import hitta_bild, hittad
import pyautogui

def hittad = ""

faktor = hitta_skalfaktor("img/01_image.JPG")
print(f"Skalfaktor hittad: {faktor}")

print("Vill du börja leta?")
choice = input("Skriv 'y' för att börja leta eller valfritt tecken för att avsluta: ")

if choice == 'y':
    hittad_bild = hitta_bild("img/004_image.JPG", faktor)
    print("Specialisten hittad")
    pyautogui.moveTo(hittad)
else:
    print("Avslutar programmet.")
