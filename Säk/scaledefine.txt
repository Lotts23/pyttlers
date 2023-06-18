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
bildadress = f"img/{name}_image.jpg"

def tested_scale():
    # Läs in namnet på den fil som används som skaldefinition
    # Namnet på bildfilen ska vara name_image.jpg och den ska
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
        scale_factor = None  # Variabel för att spara skalfaktorn
        while scale >= 0.2:
            resized_image = resize_image(name, scale)
            resized_height, resized_width, _ = resized_image.shape

            time.sleep(0.01)  # hur länge den ska vänta mellan varje loop

            if search_image(resized_image):
                scale_factor = original_width / resized_width
                break  # Avsluta loopen om bilden hittas

            # Tryck på tangenten och skriv ut en punkt
            print(".", end="", flush=True)

            scale -= 0.02  # Här kan jag ställa in hur stora steg den tar

        return scale_factor

    def resize_image(name, scale):
        image_path = f"{bildadress}"
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        print("Detekterar skalning...", end=".")
        scale_factor = scale_image(name)
        if scale_factor is not None:
            print(f"\nSkala: 1:{scale_factor}")
            return scale_factor
        else:
            print("\nIngen bild hittades.")
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")

    return None

if __name__ == '__main__':
    scale_factor = tested_scale()
    if scale_factor is not None:
        # Använd scale_factor i din andra fil för att skala om en annan bild
        pass
    else:
        print("Kontrollera att programmet är på samma skärm som spelet.")
