import pyautogui
import cv2
import platform
import time
import tempfile
import os

bildid = "geolog"
bildnamn = f"{bildid}_image.jpg"

def search_image(bildnamn):
    try:
        found_image = pyautogui.locateOnScreen(bildnamn, confidence=0.8)

        if found_image is not None:
            adjusted_x = found_image.left + found_image.width // 2
            adjusted_y = found_image.top + found_image.height // 2
            pyautogui.moveTo(adjusted_x, adjusted_y)
            print("Bilden har hittats på skärmen och musen har flyttats till dess centrum.")
            return True
        else:
            print(f"Bilden på {bildid}en kunde inte hittas.")
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

def scale_image(bildid): 
    scale = 2.0
    while scale >= 0.2:
        resized_image = resize_image(bildid, scale)
#        temp_path = save_temp_image(resized_image)

        print(f"Skalning: {int(scale * 100)}% och söker...")  # Skriv ut skalningsinformationen

        time.sleep(0.01)  # hur länge den ska vänta mellan varje loop
        
        if search_image(resized_image):

#        if search_image(temp_path):  # Sök efter bilden i temp med den nya skalningen
            return None

        scale -= 0.2  # Här kan jag ställa in hur stora steg den tar

    return None
# Här är en idé, programmet sätts på ex 0.05 scale och sedan kan man justera det i ui?

def resize_image(bildid, scale):
    image_path = f"{bildid}_image.jpg"
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    return resized_image

def save_temp_image(image):
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "temp_image.jpg")
    cv2.imwrite(temp_path, image)
    return temp_path

try:
    scale_image(bildid)
    print("Programmet avslutas.")
except Exception as e:
    print(f"Fel vid bildsökning: {str(e)}")
