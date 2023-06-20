import pyautogui
import cv2
import time
import timeit

bildadress = "img/01_image.JPG"
name = "01_image.JPG"

def tested_scale():
    def search_image(bildadress):
        try:
            found_image = pyautogui.locateOnScreen(bildadress, confidence=0.9)
            if found_image is not None:
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
            scale_factor = resized_width / original_width

            time.sleep(0.001)

            if search_image(resized_image):
                return scale_factor

            print(".", end="", flush=True)

            scale -= 0.05

        return scale_factor

    def resize_image(name, scale):
        image_path = f"{bildadress}"
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        print("Detekterar skalning...", end=".")

        start_time = timeit.default_timer()

        scale_factor = scale_image(name)

        end_time = timeit.default_timer()
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
