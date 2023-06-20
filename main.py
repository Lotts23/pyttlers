import subprocess
from scaledefine import get_scale_factor
import timeit

def run_program1():
    subprocess.run(["python", "scaledefine.py"])

def run_program2(scale_factor):
    subprocess.run(["python", "image_click.py", str(scale_factor)])

def main():
    start_time = timeit.default_timer()
    # Kör scaledefine och få skalinformation
    run_program1()

    # Hämta skalinformation från scaledefine
    scale_factor = get_scale_factor()
    end_time = timeit.default_timer()

    execution_time = end_time - start_time
    print(f"Exekveringstid för main: {execution_time} sekunder")

if __name__ == "__main__":
    main()
