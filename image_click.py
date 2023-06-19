import pyautogui
import platform
import os
import sys
import time
import cv2
import numpy as np
import pyautogui
import cv2
import numpy as np
from scaledefine import get_scale_factor

def resize_image(image, scale_factor):
    # Ändra bildens storlek med angiven skalfaktor
    resized_image = cv2.resize(image, (0, 0), fx=1/scale_factor, fy=1/scale_factor, interpolation=cv2.INTER_LINEAR)
    return resized_image

def image_click(): #?scale_factor):
    try:
        image_path = 'img/01_image.JPG'

        # Läs in sökbilden
        search_image = cv2.imread(image_path)

        if scale_factor is not None:
            # Skapa en skärmbild med pyautogui.screenshot()
            screen_image = pyautogui.screenshot()
            screen_image_np = np.array(screen_image)
            screen_image_bgr = cv2.cvtColor(screen_image_np, cv2.COLOR_RGB2BGR)

            # Skala om den sökta bilden med hjälp av den mottagna skalfaktorn
            resized_image = resize_image(search_image, scale_factor)

            # Sök efter den skalade bilden i skärmbilden
            result = cv2.matchTemplate(screen_image_bgr, resized_image, cv2.TM_CCOEFF_NORMED)
            threshold = 0.5
            locations = np.where(result >= threshold)
            locations = list(zip(*locations[::-1]))

            if locations:
                center_x = int(locations[0][0] + resized_image.shape[1] / 2)
                center_y = int(locations[0][1] + resized_image.shape[0] / 2)

                print(f"Bilden hittades!")
                pyautogui.moveTo(center_x, center_y)
            else:
                print(f"Bilden hittades inte.")

        time.sleep(1)  # Vänta 1 sekund mellan varje sökning

    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")

# Kontrollera om det finns tillräckligt med argument
if len(sys.argv) < 2:
    print("Fel: Skalfaktorn saknas som argument.")
    sys.exit(1)

# Hämta skalfaktorn från argumenten
scale_factor = float(sys.argv[1])
print(f"Skalfaktor: {scale_factor}")

# Anropa image_click-funktionen med skalfaktorn
image_click(scale_factor)

if __name__ == "__main__":
    image_click()