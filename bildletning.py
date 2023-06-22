import p2
import pyautogui

class YourClass:
    def send_button_click(self):
        numbers = ['104', '19', '15', '16']
        faktor = 1.5  # Ersätt med den faktor du behöver

        for num in numbers:
            hundradel = int(num) // 100
            tvåsiffrigt = int(num) % 100

            while True:
                bild_adress = f"img/{tvåsiffrigt}_image.JPG"
                hitta_bild_resultat = p2.hitta_bild(bild_adress, faktor)

                if not hitta_bild_resultat:
                    break

                print("Resurs hittad")
                pyautogui.moveTo(hitta_bild_resultat)
                pyautogui.mouseDown()
                pyautogui.mouseUp()

            print("Klar")

        print("Ingen mer tvåsiffrig att hitta")

