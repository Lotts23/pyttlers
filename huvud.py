from p1 import hitta_skalfaktor
from p2 import hitta_bild

# Kör p1 och få värdet på faktor
faktor = hitta_skalfaktor("img/01_image.JPG", 0.8)

# Använd värdet på faktor och skicka till p2
hitta_bild("img/02_image.JPG", faktor, 0.8)

# Skriv ut meddelande om båda bilderna hittades
print("Sökning klar")