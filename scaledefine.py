import subprocess
import pyautogui
import platform
import os
import ctypes
import cv2

def adjust_coordinates(x, y):
    screen_width, screen_height = pyautogui.size()
    os_name = platform.system()

    if os_name == 'Darwin':
        if pyautogui.is_retina():
            screen_width *= 2
            screen_height *= 2
    elif os_name == 'Windows':
        try:
            user32 = ctypes.windll.user32
            screen_width = user32.GetSystemMetrics(0)
            screen_height = user32.GetSystemMetrics(1)
        except:
            pass
    elif os_name == 'Linux':
        try:
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

def tested_scale():
    def search_image():
        try:
            # Sök efter bilden på skärmen
            found_image = pyautogui.locateOnScreen('img/01_image.JPG', confidence=0.8, region=adjust_coordinates(0, 0) + adjust_coordinates(1, 1))

            if found_image is not None:
                return True
            else:
                return False
        except Exception as e:
            print(f"Fel vid bildsökning: {str(e)}")
            return False

    def scale_image():
        scale = 2.0
        while scale >= 0.2:
            # Skala om bilden med angiven skalfaktor
            if search_image():
                return scale

            print(".", end="", flush=True)
            scale -= 0.05

        return None  # Returnera None om ingen bild hittas

    try:
        print("Detekterar skalning...", end=".")
        scale_factor = scale_image()
        if scale_factor is not None:
            print(f"\nSkaldefinitionsbild hittad med Skala: 1:{scale_factor}")
            return scale_factor, True
        elif scale_factor is None or not isinstance(scale_factor, (float, int)):
            print("Ogiltig skalningsfaktor. Avslutar programmet.")
            exit(1)
        else:
            print("\nIngen bild hittades.")
            return None, False
    except Exception as e:
        print(f"Fel vid bildsökning: {str(e)}")
        scale_factor = None
        return None, False

# Hämta skalfaktorn från tested_scale
scale_factor, _ = tested_scale()

# Starta image_click och skicka skalfaktorn som argument
subprocess.Popen(["python", "image_click.py", str(scale_factor)])

def get_scale_factor():
    return scale_factor
