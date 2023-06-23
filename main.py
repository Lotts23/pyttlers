import sys
import json
from PyQt5 import QtWidgets, QtGui
from geo import GeoWindow
from expl import ExplWindow
from p1 import hitta_skalfaktor

class StartDialog(QtWidgets.QDialog):
    def __init__(self):
        super(StartDialog, self).__init__()
        self.setWindowTitle("Välj läge")
        self.setFixedSize(300, 200)

        # Skapa en layout för dialogrutan
        layout = QtWidgets.QHBoxLayout(self)

        # Hänvisning till en extern CSS-fil
        with open("stil.css", "r") as file:
            self.setStyleSheet(file.read())

        # Skapa knappen för geolog-läget
        geo_button = QtWidgets.QPushButton()
        geo_button.setFixedSize(57, 68)
        geo_button.setIcon(QtGui.QIcon("img/geo_knapp.png"))
        geo_button.setIconSize(geo_button.rect().size())
        geo_button.clicked.connect(self.open_geo_window)
        layout.addWidget(geo_button)

        # Skapa knappen för explorer-läget
        expl_button = QtWidgets.QPushButton()
        expl_button.setFixedSize(57, 68)
        expl_button.setIcon(QtGui.QIcon("img/expl_knapp.png"))
        expl_button.setIconSize(expl_button.rect().size())
        expl_button.clicked.connect(self.open_expl_window)
        layout.addWidget(expl_button)

    def open_geo_window(self):
        # Stäng dialogrutan och öppna geo-fönstret
        self.accept()
        p1()
        geo_window = GeoWindow()
        self.hide()
        geo_window.returnToDialog.connect(self.show)  # Lägg till signalhantering för att visa dialogrutan igen
        geo_window.show()

    def open_expl_window(self):
        # Stäng dialogrutan och öppna expl-fönstret
        self.accept()
        p1()
        expl_window = ExplWindow()
        self.hide()
        expl_window.returnToDialog.connect(self.show)  # Lägg till signalhantering för att visa dialogrutan igen
        expl_window.show()

def p1():
    faktor = hitta_skalfaktor("img/01_image.JPG")
    print(f"Skalfaktor hittad: {faktor}")

    # Skriv skalfaktor till scale_data.json
    data = {"skalfaktor": faktor}
    with open("scale_data.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    start_dialog = StartDialog()
    if start_dialog.exec_() == QtWidgets.QDialog.Accepted:
        sys.exit(app.exec_())
