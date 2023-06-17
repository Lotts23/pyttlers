import pyautogui
import cv2
import platform
import time
import tempfile
import os
import json

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
            print("Bilden har hittats på skärmen och musen har flyttats till dess centrum.")
            return True
        else:
            print(f"Bilden på {name} kunde inte hittas. Se till att bilden ligger i img och har formen name_image.jpg")
            return False
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")
        return False

def adjust_coordinates(x, y):
    screen_width, screen_height = pyautogui.size()
    os_name = platform.system()

    if os_name == 'Darwin':  # För macOS
        if pyautogui.is_retina():  # Kontrollera om det är en Retina-skärm
            screen_width *= 2
            screen_height *= 2
    elif os_name == 'Windows':  # För Windows
        try:
            import ctypes
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
        except:
            pass
    elif os_name == 'Linux':  # För Linux
        try:
            import subprocess
            output = subprocess.check_output(['xrandr']).decode('utf-8')
            for line in output.splitlines():
                if ' connected' in line:
                    line_parts = line.split()
                    screen_size = line_parts[line_parts.index('connected') + 1]
                    screen_width, screen_height = map(int, screen_size.split('x'))
                    break
        except:
            pass

    adjusted_x = x * screen_width
    adjusted_y = y * screen_height
    return adjusted_x, adjusted_y


def scale_image(name):
    original_image = cv2.imread(bildadress)
    original_height, original_width, _ = original_image.shape

    scale = 2.0
    while scale >= 0.2:
        resized_image = resize_image(name, scale)
        resized_height, resized_width, _ = resized_image.shape

        scale_factor = original_width / resized_width
        print(f"Skalning: {int(scale * 100)}%, Faktor: {scale_factor} och söker...")  # Skriv ut skalningsinformationen

        time.sleep(0.01)  # hur länge den ska vänta mellan varje loop
        
        if search_image(resized_image):

#        if search_image(temp_path):  # Sök efter bilden i temp med den nya skalningen
            return None

        scale -= 0.02  # Här kan jag ställa in hur stora steg den tar

    return None

def resize_image(name, scale):
    image_path = f"{bildadress}"
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    return resized_image

try:
    scale_image(name)
    print("Programmet avslutas.")
except Exception as e:
    print(f"Fel vid bildsökning: {str(e)}")
