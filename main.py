import subprocess
import pyautogui
from scaledefine import get_scale_factor
import timeit
import image_click

def run_program1():
    subprocess.run(["python", "scaledefine.py"])

def main():
    start_time = timeit.default_timer()

    # Kör scaledefine och få skalinformation
    run_program1()

    # Hämta skalinformation från scaledefine
    scale_factor = get_scale_factor()

    # Kör image_click med skalinformationen och få tillbaka bildnamnet och sökvägen
    image_path, found_image = image_click.click_image(scale_factor)
    
    if found_image is not None:
        center_x, center_y = pyautogui.center(found_image)
        pyautogui.moveTo(center_x, center_y)

    print("Bildnamn:", image_path)
    end_time = timeit.default_timer()

    execution_time = end_time - start_time
    print(f"Exekveringstid för main: {execution_time} sekunder")

if __name__ == "__main__":
    main()
