import pyautogui
import cv2
import time
#import json
import timeit

# Läs in konfigurationsdata från JSON-filen
#with open('scaleimage.json', 'r') as file:
#    data = json.load(file)

# Extrahera namnet från JSON-data
#name = data[0]['name']
bildadress = f"img/01_image.JPG"
name = "01_image.JPG"

def tested_scale():
    def search_image(bildadress):
        try:
            # Sök efter bilden på skärmen med angiven bildadress
            found_image = pyautogui.locateOnScreen(bildadress, confidence=0.8)

            if found_image is not None:
                # Justera koordinaterna för att hitta bildens mitt
                # adjusted_x = found_image.left + found_image.width // 2
                # adjusted_y = found_image.top + found_image.height // 2
                # pyautogui.moveTo(adjusted_x, adjusted_y)
                return True
            else:
                return False
        except Exception as e:
            print(f"Fel vid bildsökning: {str(e)}")
            return False

    def scale_image(name):
        # Läs in den ursprungliga bilden
        original_image = cv2.imread(bildadress)
        original_height, original_width, _ = original_image.shape

        scale = 2.0
        while scale >= 0.2:
            # Skala om bilden med angivet namn och skalfaktor
            resized_image = resize_image(name, scale)
            resized_height, resized_width, _ = resized_image.shape
            scale_factor = resized_width / original_width

            time.sleep(0.001)

            if search_image(resized_image):
                # Returnera skalfaktorn om bilden hittas
                return scale_factor

            print(".", end="", flush=True)

            scale -= 0.05

        return scale_factor

    def resize_image(name, scale):
        # Läs in bilden och ändra dess storlek med angiven skalfaktor
        image_path = f"{bildadress}"
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        print("Detekterar skalning...", end=".")

        start_time = timeit.default_timer()  # Starta timern

        scale_factor = scale_image(name)

        end_time = timeit.default_timer()  # Stoppa timern
        execution_time = end_time - start_time

        if scale_factor is not None:
            print(f"\nSkaldefinitionsbild {bildadress} hittad med Skala: 1:{scale_factor}")
            print(f"Exekveringstid för scaledefine: {execution_time} sekunder")
            return scale_factor, True
        else:
            print("\nIngen bild hittades.")
            return None, False
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")
        scale_factor = None
        return None, False

def get_scale_factor():
    scale_factor, _ = tested_scale()
    return scale_factor

#if __name__ == '__main__':
    # Kör skalningstestet och spara skalfaktorn
#    scale_factor = tested_scale()
#    if scale_factor is not None:
        # Använd scale_factor i image_click för att skala om en annan bild
#        pass
#    else:
#        print(scale_factor, name, bildadress, "Kontrollera att programmet är på samma skärm som spelet.")