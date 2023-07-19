import json
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox


class GeoWindow(QtWidgets.QMainWindow):
    returnToDialog = QtCore.pyqtSignal()

    def __init__(self):
        super(GeoWindow, self).__init__()
        self.setWindowTitle("Välj geologer att sända")
        self.setGeometry(500, 100, 600, 590)

        # Skapa en huvudwidget som innehåller allt innehåll
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        
        font = QtGui.QFont()
        font.setPointSize(10)  # Ange den önskade storleken på texten
               
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(QtCore.Qt.white))
        QtWidgets.QApplication.setPalette(palette)
        QtWidgets.QApplication.setFont(font)

        # Skapa en box för den övre layouten (geologer och resurser)
        self.upperBox = QtWidgets.QGroupBox()
        self.upperLayout = QtWidgets.QHBoxLayout(self.upperBox)
        self.upperBox.setStyleSheet("border: none; padding: 5px;")

        # Skapa en box för vänsterinnehållet (geologknapparna)
        self.leftBox = QtWidgets.QGroupBox("    Geologer")
        self.leftLayout = QtWidgets.QGridLayout(self.leftBox)  # Uppdaterad layout för vänsterboxen
        self.leftBox.setStyleSheet("QGroupBox {border-top: 1px solid rgb(230, 153, 10); border-bottom: 1px solid rgb(230, 153, 10); padding: 5px;}")

        # Skapa en box för högerinnehållet (resurserna)
        self.rightBox = QtWidgets.QGroupBox("   Resurser")
        self.rightLayout = QtWidgets.QGridLayout(self.rightBox)  # Uppdaterad layout för högerboxen
        self.rightBox.setStyleSheet("QGroupBox {border-top: 1px solid rgb(230, 153, 10); border-bottom: 1px solid rgb(230, 153, 10); padding: 5px;}")

        # Skapa en box för bottom-innehållet (check-knappen och de två knapparna)
        self.bottomBox = QtWidgets.QGroupBox()
        self.bottomLayout = QtWidgets.QHBoxLayout(self.bottomBox)
        self.bottomBox.setStyleSheet("border: 0px; padding: 5px;")

        # Lägg till vänster- och högerboxen i den övre layouten
        self.upperLayout.addWidget(self.leftBox)
        self.upperLayout.addWidget(self.rightBox)
                
        # Skapa textrutan för infotexten
        self.infoText = QtWidgets.QLabel()
        self.infoText.setFixedHeight(88)  # Höjden på textrutan
        self.infoText.setFixedWidth(540)
        self.infoText.setText("När du klickar på check så kommer programmet ta kontroll över musen och genomföra alla klick för sökningen. \nDra musen till skärmens hörn i några sekunder för att avbryta akut.\n\nEndast den sist klickade resursen kommer sökas, grafikfel.")
        self.infoText.setWordWrap(True)
        self.infoText.setStyleSheet("background-color: #4b453a; padding-left: 10px; padding-right: 10px; border: 2px ridge #363229")
        
        # Skapa en layout för att centrera infoText-rutan
        centerLayout = QtWidgets.QHBoxLayout()
        centerLayout.addStretch()
        centerLayout.addWidget(self.infoText)
        centerLayout.addStretch()

        # Skapa en yttre layout för att lägga till padding och justering
        outerLayout = QtWidgets.QHBoxLayout()
        outerLayout.addStretch()
        outerLayout.addLayout(centerLayout)
        outerLayout.addStretch()
        
        # Lägg till den övre boxen, text- och bottom-boxen i huvudlayouten
        self.centralLayout.addWidget(self.upperBox)
        self.centralLayout.addLayout(outerLayout)
        self.centralLayout.addWidget(self.bottomBox)

        # Hänvisning till en extern CSS-fil
        with open("./src/stil.css", "r") as file:
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

        self.selected_buttons_left = []  # Lista för markerade knappar i vänster box
        self.selected_buttons_right = []  # Lista för markerade knappar i höger box

        self.button_images = []
        self.selected_buttons = []
        self.buttonsLeft = []  # Lista för knapparna i vänster box
        self.buttonsRight = []  # Lista för knapparna i höger box

        # Skapa knapparna för geologerna
        for i in range(10, 26):
            value = str(i)  # Uppdaterad numrering 10-25

            button = QtWidgets.QPushButton(self.scrollContent)
            button.setFixedSize(57, 68)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayout.addWidget(button, (i-10) // 4, (i-10) % 4)  # Uppdatera layout för vänsterknapparna
            self.buttonsLeft.append(button)  # Uppdaterad namn på listan

            image = QtGui.QPixmap(f"./src/img/knapp/gknapp_{value}.png")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())
            button.setIconSize(QtCore.QSize(57, 68))  # Justera storleken på ikonen vid behov
            button.setStyleSheet("QPushButton::icon {"
                                "    position: absolute;"
                                "    bottom: 0;"
                                "    right: 0;"
                                "    border-radius: 5px;"
                                "}")            

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
            button.setFixedSize(42, 30)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayoutRight.addWidget(button, (i-100) // 2, (i-100) % 2)
            self.buttonsRight.append(button)  # Uppdaterad namn på listan

            image = QtGui.QPixmap(f"./src/img/knapp/rknapp_{value}.jpg")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())
            button.setIconSize(QtCore.QSize(38, 30))  # Justera storleken på ikonen vid behov
            button.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton::icon {"
                                "    position: absolute;"
                                "    bottom: -2;"
                                "    right: -2;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton:hover {"
                                "    border: 2px ridge #756d5b;"
                                "    border-radius: 5px;"
                                "}")

            # Endast en knapp åt gången kan väljas i den högra boxen
            button.setAutoExclusive(True)

        # Skapa knapparna för bottom-innehållet
        back_button = QtWidgets.QPushButton()
        back_button.setFixedSize(42, 30)
        self.bottomLayout.addWidget(back_button)
        image = QtGui.QPixmap(f"./src/img/knapp/back.jpg")
        self.button_images.append(image)
        back_button.setIcon(QtGui.QIcon(image))
        back_button.setIconSize(QtCore.QSize(38, 30))  # Justera storleken på ikonen vid behov
        back_button.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton::icon {"
                                "    position: absolute;"
                                "    bottom: -2;"
                                "    right: -2;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton:hover {"
                                "    border: 2px ridge #756d5b;"
                                "    border-radius: 5px;"
                                "}")

# Rensa
        clear_button = QtWidgets.QPushButton()
        clear_button.setFixedSize(42, 30)
        clear_button.clicked.connect(self.clear_button_click)
        self.bottomLayout.addWidget(clear_button)
        image = QtGui.QPixmap(f"./src/img/knapp/clear.jpg")
        self.button_images.append(image)
        clear_button.setIcon(QtGui.QIcon(image))
        clear_button.setIconSize(QtCore.QSize(38, 30))  # Justera storleken på ikonen vid behov
        clear_button.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton::icon {"
                                "    position: absolute;"
                                "    bottom: -2;"
                                "    right: -2;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton:hover {"
                                "    border: 2px ridge #756d5b;"
                                "    border-radius: 5px;"
                                "}")

        send_button = QtWidgets.QPushButton()
        send_button.setFixedSize(42, 30)
        send_button.clicked.connect(self.send_button_click)
        self.bottomLayout.addStretch()
        self.bottomLayout.addWidget(send_button)
        image = QtGui.QPixmap(f"./src/img/knapp/check.jpg")
        self.button_images.append(image)
        send_button.setIcon(QtGui.QIcon(image))
        send_button.setIconSize(QtCore.QSize(38, 30))  # Justera storleken på ikonen vid behov
        send_button.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton::icon {"
                                "    position: absolute;"
                                "    bottom: -2;"
                                "    right: -2;"
                                "    border-radius: 5px;"
                                "}"
                                "QPushButton:hover {"
                                "    border: 2px ridge #756d5b;"
                                "    border-radius: 5px;"
                                "}")     

        back_button.clicked.connect(self.return_to_dialog)

    def return_to_dialog(self):
        self.close()
        self.returnToDialog.emit()
       
    def get_button_by_value(self, value):
        for button in self.buttonsLeft + self.buttonsRight:
            if button.property("value") == value:
                return button
        return None

    def button_click(self, button, value):
        if button.isChecked():
            if button in self.buttonsLeft:
                button.setStyleSheet("border: 6px ridge yellow; border-radius: 5px;")
                self.selected_buttons_left.append(int(value))
            elif button in self.buttonsRight:
                prev_button_value = self.selected_buttons_right[0] if self.selected_buttons_right else None
                if prev_button_value and prev_button_value != int(value):
                    prev_button_button = self.get_button_by_value(prev_button_value)
                    if prev_button_button:
                        prev_button_button.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}")

                button.setStyleSheet("border: 6px ridge yellow; border-radius: 5px;")
                self.selected_buttons_right = [int(value)]  # Spara värdet
        else:
            button.setStyleSheet("")
            if button in self.buttonsLeft:
                self.selected_buttons_left.remove(int(value))
            elif button in self.buttonsRight:
                self.selected_buttons_right = []  # Reset

        self.selected_buttons = self.selected_buttons_left + self.selected_buttons_right
        print("Markerade knappar:", self.selected_buttons)

        if button in self.buttonsRight:
            self.update_json()  # Updatera json

    def update_json(self):
        json_data = {
            "geologer": self.selected_buttons_left,
            "resurs": self.selected_buttons_right
        }
        with open("./src/nummer.json", "w") as json_file:
            json.dump(json_data, json_file)

    def clear_button_click(self):
        self.selected_buttons_left = []  # Återställ markerade knappar i vänster box
        self.selected_buttons_right = []  # Återställ markerade knappar i höger box
        for btn in self.buttonsLeft:
            btn.setChecked(False)
            btn.setStyleSheet("")
        for btn in self.buttonsRight:
            btn.setChecked(False)
            btn.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}")

    def send_button_click(self):
        if not self.selected_buttons_left or not self.selected_buttons_right:
            QMessageBox.warning(self, "Gör alla val först", "Vänligen välj både en geolog och en resurs innan du klickar på Check.")
            return
    
        resurs_value = 100
        custom_order = [18, 16, 21, 12, 20, 25, 24, 17, 13, 11, 23, 22, 14, 19, 15, 10]
        geologer_sorted = self.selected_buttons_left[:]
        geologer_sorted = sorted(geologer_sorted, key=lambda x: custom_order.index(x) if x in custom_order else float('inf'))
        if self.selected_buttons_right:
            resurs_str = str(self.selected_buttons_right[0])
            if resurs_str.isdigit():
                resurs_value = int(resurs_str)

        data = {
            "geologer": list(geologer_sorted),
            "resurs": resurs_value
        }

        with open("./src/nummer.json", "w") as json_file:
            json.dump(data, json_file)



        print("Skicka-knappen klickad")
        self.close()
        subprocess.Popen([sys.executable, "./src/running.py"])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = GeoWindow()
    window.show()
    sys.exit(app.exec_())
    