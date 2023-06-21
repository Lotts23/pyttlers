from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Användargränssnitt")
        self.setGeometry(100, 100, 800, 700) 

        # Skapa en huvudwidget som innehåller allt innehåll
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QtWidgets.QHBoxLayout(self.centralWidget)

        # Skapa en box för vänsterinnehållet (geologknapparna)
        self.leftBox = QtWidgets.QGroupBox("Geologer")
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftBox)

        # Skapa en box för högerinnehållet (resurserna)
        self.rightBox = QtWidgets.QGroupBox("Resurser")
        self.rightLayout = QtWidgets.QGridLayout(self.rightBox)

        # Lägg till de två boxarna i huvudlayouten
        self.centralLayout.addWidget(self.leftBox)
        self.centralLayout.addWidget(self.rightBox)

        # Bakgrundsfärg och textstil för hela fönstret
        self.setStyleSheet("background-color: #5c5444; color: white; font-weight: bold;")

        # Skapa scrollområdet för geologknapparna
        self.scrollArea = QtWidgets.QScrollArea(self.leftBox)
        self.scrollArea.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scrollArea)

        self.scrollContent = QtWidgets.QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollContent)

        self.gridLayout = QtWidgets.QGridLayout(self.scrollContent)

        self.buttons = []
        self.button_images = []
        self.selected_buttons = []

        for i in range(10, 26):
            value = str(i)  # Uppdaterad numrering 10-25

            button = QtWidgets.QPushButton(self.scrollContent)
            button.setFixedSize(55, 66)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayout.addWidget(button, (i-10) // 4, (i-10) % 4)
            self.buttons.append(button)

            image = QtGui.QPixmap(f"img/{value}_knapp.png")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())

        # Skapa knapparna för resurserna
        for i in range(100, 110):
            value = str(i)  # Uppdaterad numrering 100-109

            button = QtWidgets.QPushButton(self.rightBox)
            button.setFixedSize(40, 32)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))

            if i < 106:
                self.rightLayout.addWidget(button, 0, i - 100)
            else:
                self.rightLayout.addWidget(button, 1, i - 106)

            self.buttons.append(button)

            image = QtGui.QPixmap(f"img/{value}_rknapp.png")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())

            # Endast en knapp åt gången kan väljas i den högra boxen
            button.setAutoExclusive(True)

    def button_click(self, button, value):
        if button.isChecked():
            button.setStyleSheet("border: 6px solid yellow")
            if self.sender() in self.buttons:  # Kommer från vänstra boxen
                self.selected_buttons.append(value)
            else:  # Kommer från högra boxen
                if self.selected_buttons:  # Om det redan finns en markerad knapp, avmarkera den
                    self.selected_buttons[0] = value
                    self.buttons[10].setChecked(False)  # Avmarkera den föregående knappen
                else:
                    self.selected_buttons.append(value)
        else:
            button.setStyleSheet("")
            if self.sender() in self.buttons:  # Kolla om knappen kommer från vänstra boxen
                self.selected_buttons.remove(value)
            else:  # Kommer från högra boxen
                self.selected_buttons = []

        print("Markerade knappar:", self.selected_buttons)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
