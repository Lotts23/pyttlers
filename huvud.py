from p1 import hitta_skalfaktor
from p2 import hitta_bild

# Kör p1 och få värdet på faktor
faktor = hitta_skalfaktor("img/01_image.JPG")

# Använd värdet på faktor och skicka till p2
hitta_bild("img/002_image.JPG")

# Skriv ut meddelande om båda bilderna hittades
print("Sökning klar")