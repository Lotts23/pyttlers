import subprocess
import pyautogui

def tested_scale():
    def search_image():
        try:
            # Sök efter bilden på skärmen
            found_image = pyautogui.locateOnScreen('img/01_image.JPG', confidence=0.8)

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

# Hämta skalfaktorn från scaledefine
scale_factor, _ = tested_scale()

# Starta image_click och skicka skalfaktorn som argument
subprocess.Popen(["python", "image_click.py", str(scale_factor)])

def get_scale_factor():
    scale_factor, _ = tested_scale()
    return scale_factor
