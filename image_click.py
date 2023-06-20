import cv2
import numpy as np
import pyautogui
import timeit

def click_image(scale_factor):
    def search_image(image):
        try:
            template = cv2.imread(image)
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
            
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= 0.6:
                top_left = max_loc
                bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
                return True, top_left, bottom_right
            else:
                return False, None, None
        except Exception as e:
            print(f"Fel vid bildsökning: {str(e)}")
            return False, None, None

    def resize_image(image, scale):
        # Skalera om bilden med angiven skalfaktor
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        # Läs in den ursprungliga bilden
        image_path = "img/01_image.JPG"
        original_image = cv2.imread(image_path)

        print("Originalbildens storlek:", original_image.shape)

        print("Skalar om bilden...", end="")

        start_time = timeit.default_timer()

        # Skala om bilden med angiven skalfaktor från scaledefine
        resized_image = resize_image(original_image, scale_factor)

        end_time = timeit.default_timer()
        execution_time = end_time - start_time

        success, top_left, bottom_right = search_image(image_path)

        if success:
            print("\nBilden hittades.")
            print(f"Exekveringstid för image_click: {execution_time} sekunder")
            resized_image = resize_image(original_image, scale_factor)
            print("Skalade bildens storlek:", resized_image.shape)
            return image_path, top_left, bottom_right
        else:
            print("\nBilden hittades inte.")
            resized_image = resize_image(original_image, scale_factor)
            print("Skalade bildens storlek:", resized_image.shape)
            return None, None, None
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")
        return None, None, None
