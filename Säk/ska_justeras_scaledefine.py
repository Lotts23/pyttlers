import pyautogui
import cv2
import platform
import time
import tempfile
import os
import json

def tested_scale():
    # Läs in namnet på den fil som används som skaldefinition
    # Namnet på bildfilen ska vara name_image.png och den ska
    # ligga i mappen img.

    with open('scaleimage.json', 'r') as file:
        data = json.load(file)

    name = data[0]['name']
    bildadress = f"img/{name}_image.png"

    def search_image(bildadress):
        try:
            found_image = pyautogui.locateOnScreen(bildadress, confidence=0.8)

            if found_image is not None:
                adjusted_x = found_image.left + found_image.width // 2
                adjusted_y = found_image.top + found_image.height // 2
                pyautogui.moveTo(adjusted_x, adjusted_y)
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
            scale_factor = original_width / resized_width

            time.sleep(0.01)  # hur länge den ska vänta mellan varje loop

            if search_image(resized_image):
                return resized_height, resized_width, scale_factor

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
        result = scale_image(name)
        if result[0] is not None:
            resized_height, resized_width, scale_factor = result
            print(f"\nSkala: 1:{scale_factor}")
            return scale_factor
        else:
            print("\nIngen bild hittades.")
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")

    return None

if __name__ == '__main__':
    result = tested_scale()
    if result is not None:
        resized_height, resized_width = result
        # print(f"Resized Height: {resized_height}")
        # print(f"Resized Width: {resized_width}")
    else:
        print("Kontrollera att programmet är på samma skärm som spelet.")
