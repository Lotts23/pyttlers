import subprocess
import scaledefine
import image_click

def run_program1():
    subprocess.run(["python", "scaledefine.py"])

def main():
    scale_factor = scaledefine.get_scale_factor()
    if scale_factor is not None:
        print(f"Skalfaktor: 1:{scale_factor}")
        image_path, top_left, bottom_right = image_click.click_image(scale_factor)
        if image_path is not None and top_left is not None and bottom_right is not None:
            print("Bildinformation:")
            print("Image Path:", image_path)
            print("Top Left:", top_left)
            print("Bottom Right:", bottom_right)
            # Använd bildinformationen för att utföra önskad åtgärd
        else:
            print("Bilden hittades inte.")
    else:
        print("Kontrollera att programmet är på samma skärm som spelet.")


if __name__ == "__main__":
    main()
