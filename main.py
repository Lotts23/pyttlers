import time
import subprocess
from scaledefine import get_scale_factor

def run_program1():
    subprocess.run(["python", "scaledefine.py"], capture_output=True)

def run_program2(scale_factor):
    subprocess.run(["python", "image_click.py", str(scale_factor)], capture_output=True)

def main():
    # Kör scaledefine och få skalinformation
    run_program1()

    # Hämta skalinformation från scaledefine
    scale_factor = get_scale_factor()

    # Kör image_click med skalinformationen
    run_program2(scale_factor)

if __name__ == "__main__":
    main()
