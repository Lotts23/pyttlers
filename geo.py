from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Välj geologer att sända")
        self.setGeometry(500, 100, 600, 500)  # Uppdatera storleken på fönstret

        # Skapa en huvudwidget som innehåller allt innehåll
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        # Skapa en box för den övre layouten (geologer och resurser)
        self.upperBox = QtWidgets.QGroupBox()
        self.upperLayout = QtWidgets.QHBoxLayout(self.upperBox)
        self.upperBox.setStyleSheet("border: none; padding: 5px;")


        # Skapa en box för vänsterinnehållet (geologknapparna)
        self.leftBox = QtWidgets.QGroupBox("Geologer")
        self.leftLayout = QtWidgets.QGridLayout(self.leftBox)  # Uppdaterad layout för vänsterboxen

        # Skapa en box för högerinnehållet (resurserna)
        self.rightBox = QtWidgets.QGroupBox("Resurser")
        self.rightLayout = QtWidgets.QGridLayout(self.rightBox)  # Uppdaterad layout för högerboxen

        # Skapa en box för bottom-innehållet (check-knappen och de två nya knapparna)
        self.bottomBox = QtWidgets.QGroupBox()
        self.bottomLayout = QtWidgets.QHBoxLayout(self.bottomBox)
        self.bottomBox.setStyleSheet("border: 0px; padding: 5px;")

        # Lägg till vänster- och högerboxen i den övre layouten
        self.upperLayout.addWidget(self.leftBox)
        self.upperLayout.addWidget(self.rightBox)

        # Lägg till den övre boxen och bottom-boxen i huvudlayouten
        self.centralLayout.addWidget(self.upperBox)
        self.centralLayout.addWidget(self.bottomBox)

        # Hänvisning till en extern CSS-fil
        with open("stil.css", "r") as file:
            self.setStyleSheet(file.read())

        # Skapa id för de två områdena
        self.leftBox.setObjectName("leftBox")
        self.rightBox.setObjectName("rightBox")

        # Skapa scrollområdet för geologknapparna
        self.scrollArea = QtWidgets.QScrollArea(self.leftBox)
        self.scrollArea.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scrollArea)

        self.scrollContent = QtWidgets.QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollContent)

        self.gridLayout = QtWidgets.QGridLayout(self.scrollContent)

        self.buttonsLeft = []
        self.buttonsRight = []
        self.button_images = []
        self.selected_buttons = []

        # Skapa knapparna för geologerna
        for i in range(10, 26):
            value = str(i)  # Uppdaterad numrering 10-25

            button = QtWidgets.QPushButton(self.scrollContent)
            button.setFixedSize(57, 68)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayout.addWidget(button, (i-10) // 4, (i-10) % 4)  # Uppdatera layout för vänsterknapparna
            self.buttonsLeft.append(button)  # Uppdaterad namn på listan

            image = QtGui.QPixmap(f"img/{value}_gknapp.png")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())

        # Skapa scrollområdet för resursknapparna
        self.scrollAreaRight = QtWidgets.QScrollArea(self.rightBox)
        self.scrollAreaRight.setWidgetResizable(True)
        self.rightLayout.addWidget(self.scrollAreaRight)

        self.scrollContentRight = QtWidgets.QWidget(self.scrollAreaRight)
        self.scrollAreaRight.setWidget(self.scrollContentRight)

        self.gridLayoutRight = QtWidgets.QGridLayout(self.scrollContentRight)

        # Skapa knapparna för resurserna
        for i in range(100, 109):
            value = str(i)

            button = QtWidgets.QPushButton(self.scrollContentRight)
            button.setFixedSize(40, 32)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayoutRight.addWidget(button, (i-100) // 2, (i-100) % 2)
            self.buttonsRight.append(button)  # Uppdaterad namn på listan

            image = QtGui.QPixmap(f"img/{value}_rknapp.png")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())

            # Endast en knapp åt gången kan väljas i den högra boxen
            button.setAutoExclusive(True)

        # Skapa knapparna för bottom-innehållet
        undo_button = QtWidgets.QPushButton("Åter")
        undo_button.setFixedSize(50, 20)
        self.bottomLayout.addWidget(undo_button)

        clear_button = QtWidgets.QPushButton("Rensa")
        clear_button.setFixedSize(50, 20)
        clear_button.clicked.connect(self.clear_button_click)
        self.bottomLayout.addWidget(clear_button)

        send_button = QtWidgets.QPushButton("Skicka")
        send_button.setFixedSize(50, 20)
        send_button.clicked.connect(self.send_button_click)
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(send_button)

    def button_click(self, button, value):
        if button.isChecked():
            if button in self.buttonsLeft:  # Kommer från vänstra boxen
                self.selected_buttons.append(value)
            elif button in self.buttonsRight:  # Kommer från högra boxen
                if button in self.selected_buttons:  # Om knappen redan är markerad, avmarkera den
                    button.setChecked(False)
                    button.setStyleSheet("")
                    self.selected_buttons.remove(value)
                else:  # Annars avmarkera den tidigare markerade knappen och lägg till den nya i listan
                    self.selected_buttons = [value]
                    for btn in self.buttonsRight:
                        if btn.isChecked() and btn != button:
                            btn.setChecked(False)
                            btn.setStyleSheet("")

        else:  # Kommer från högra boxen
            button.setStyleSheet("")
            if button in self.buttonsLeft:  # Kommer från vänstra boxen
                self.selected_buttons.remove(value)
            elif button in self.buttonsRight:  # Kommer från högra boxen
                if button in self.selected_buttons:  # Om knappen redan är markerad, avmarkera den
                    button.setChecked(False)
                    button.setStyleSheet("")
                    self.selected_buttons = [v for v in self.selected_buttons if v != value]

        print("Markerade knappar:", self.selected_buttons)

    def clear_button_click(self):
        self.selected_buttons = []
        for btn in self.buttonsLeft:
            btn.setChecked(False)
            btn.setStyleSheet("")
        for btn in self.buttonsRight:
            btn.setChecked(False)
            btn.setStyleSheet("")

    def send_button_click(self):
        print("Skicka-knappen klickad")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
