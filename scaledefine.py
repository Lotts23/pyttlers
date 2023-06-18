import pyautogui
import cv2
import platform
import time
import tempfile
import os
import json

with open('scaleimage.json', 'r') as file:
    data = json.load(file)
name = data[0]['name']
bildadress = f"img/{name}_image.png"

def tested_scale():
    # Läs in namnet på den fil som används som skaldefinition
    # Namnet på bildfilen ska vara name_image.png och den ska
    # ligga i mappen img.

    def search_image(bildadress):
        try:
            found_image = pyautogui.locateOnScreen(bildadress, confidence=0.8)

            if found_image is not None:
                adjusted_x = found_image.left + found_image.width // 2
                adjusted_y = found_image.top + found_image.height // 2
                #pyautogui.moveTo(adjusted_x, adjusted_y)
                return True
            else:
                return False
        except Exception as e:
            print(f"Fel vid bildsökning: {str(e)}")
            return False

    def scale_image(name):
        original_image = cv2.imread(bildadress)
        original_height, original_width, _ = original_image.shape

        scale = 2.0
        while scale >= 0.2:
            resized_image = resize_image(name, scale)
            resized_height, resized_width, _ = resized_image.shape
            scale_factor = original_width / resized_width # Detta är det viktiga. Men det får inte vara för varje iteration utan ska bara beräknas EFTER att bilden hittats korrekt, DEN skalfaktorn behöver jag

            time.sleep(0.01)  # hur länge den ska vänta mellan varje loop

            if search_image(resized_image):
                return scale_factor #Oj Ännu en gång returnerar jag scale_factor. Konflikter nu?

            # Tryck på tangenten och skriv ut en punkt
            print(".", end="", flush=True)

            scale -= 0.02  # Här kan jag ställa in hur stora steg den tar

        return None, None, None

    def resize_image(name, scale):
        image_path = f"{bildadress}"
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        print("Detekterar skalning...", end=".")
        result = scale_image(name) # Nu skapar jag en ny result. Jag bryr mig inte om result, jag måste bara kunna returnera scale_factor korrekt
        if result[0] is not None:
            resized_height, resized_width, scale_factor = result #Här gör jag detta IGEN, varför result? Height och width har jag ingen användning av om scale_facor är beräknat
            print(f"\nSkala: 1:{scale_factor}")
            return scale_factor #resized_height, resized_width
        else:
            print("\nIngen bild hittades.")
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")

    return None

if __name__ == '__main__':
    result = tested_scale() # Varför skapar jag variabeln result? Redundant?
    if result is not None:
        scale_factor = result # och inte får jag omvandla scale_factor två gånger, här blir ju värdet fel
        # jag använder scale_factor i min andra fil
    else:
        print("Kontrollera att programmet är på samma skärm som spelet.")
