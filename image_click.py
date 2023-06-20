import pyautogui
import cv2
import time
import json
import timeit

def click_image(scale_factor):
    def search_image(image):
        try:
            found_image = pyautogui.locateOnScreen(image, confidence=0.6)
            if found_image is not None:
                return True, found_image
            else:
                return False, None
        except Exception as e:
            print(f"Fel vid bildsökning: {str(e)}")
            return False, None

    def resize_image(image, scale):
        # Skala om bilden med angiven skalfaktor
        resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        return resized_image

    try:
        # Läs in den ursprungliga bilden
        with open('scaleimage.json', 'r') as file:
            data = json.load(file)

        name = data[0]['name']
        image_path = f"img/{name}_image.JPG"
        original_image = cv2.imread(image_path)

        print("Originalbildens storlek:", original_image.shape)

        print("Skalar om bilden...", end="")

        start_time = timeit.default_timer()

        # Skala om bilden med angiven skalfaktor från scaledefine
        resized_image = resize_image(original_image, scale_factor)

        end_time = timeit.default_timer()
        execution_time = end_time - start_time

        success, found_image = search_image(resized_image)

        if success:
            print("\nBilden hittades.")
            print(f"Exekveringstid för image_click: {execution_time} sekunder")
            print("Skalade bildens storlek:", resized_image.shape)
            return image_path, found_image
        else:
            print("\nBilden hittades inte.")
            print("Skalade bildens storlek:", resized_image.shape)
            return None, None
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")
        return None, None
