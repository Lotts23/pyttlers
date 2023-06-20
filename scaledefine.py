import pyautogui
import cv2
import time
import timeit

bildadress = "img/01_image.JPG"

def tested_scale():
    def search_image(bildadress):
        try:
            # Sök efter bilden på skärmen med angiven bildadress
            found_image = pyautogui.locateOnScreen(bildadress, confidence=0.8)

            if found_image is not None:
                return True
            else:
                return False
        except Exception as e:
            print(f"Fel vid bildsökning: {str(e)}")
            return False

    def scale_image(bildadress):
        # Läs in den ursprungliga bilden
        original_image = cv2.imread(bildadress)
        original_height, original_width, _ = original_image.shape

        scale = 2.0
        while scale >= 0.2:
            # Skala om bilden med angivet namn och skalfaktor
            resized_image = resize_image(bildadress, scale)
            resized_height, resized_width, _ = resized_image.shape
            scale_factor = resized_width / original_width

            time.sleep(0.001)

            if search_image(resized_image):
                # Returnera skalfaktorn om bilden hittas
                return scale_factor

            print(".", end="", flush=True)

            scale -= 0.05

        return scale_factor

    def resize_image(bildadress, scale):
        # Läs in bilden och ändra dess storlek med angiven skalfaktor
        image = cv2.imread(bildadress)
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        print("Detekterar skalning...", end=".")

        start_time = timeit.default_timer()  # Starta timern

        scale_factor = scale_image(bildadress)

        end_time = timeit.default_timer()  # Stoppa timern
        execution_time = end_time - start_time

        if scale_factor is not None:
            print(f"\nSkaldefinitionsbild {bildadress} hittad med Skala: 1:{scale_factor}")
            print(f"Exekveringstid för scaledefine: {execution_time} sekunder")
            return scale_factor, (0, 0), (0, 0)
        else:
            print("\nIngen bild hittades.")
            return None, None, None
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")
        scale_factor = None
        return None, None, None

def get_scale_factor():
    scale_factor, _, _ = tested_scale()
    return scale_factor
