import importlib
import json
import os
import subprocess
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QRect, Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QLabel,
                             QMessageBox, QPushButton, QStackedWidget,
                             QVBoxLayout, qApp)

from running2 import ProgressDialog

app_data_dir = os.path.join(os.getenv('APPDATA'), 'Pyttlers') if os.name == 'nt' else os.path.expanduser("~/.config/Pyttlers")

app_data_path = os.path.join(app_data_dir, 'Pyttlers')
os.makedirs(app_data_path, exist_ok=True)    

class ExplWindow(QtWidgets.QMainWindow):
    returnToDialog = QtCore.pyqtSignal()
    startProgressDialog = QtCore.pyqtSignal()

    def __init__(self):
        super(ExplWindow, self).__init__()
        self.app_data_path = app_data_path
        self.setWindowTitle("Välj explorers att sända")
        self.setGeometry(500, 100, 640, 790)

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

        # Skapa en box för den övre layouten (explorer och sökmål)
        self.upperBox = QtWidgets.QGroupBox()
        self.upperLayout = QtWidgets.QHBoxLayout(self.upperBox)
        self.upperBox.setStyleSheet("border: none; padding: 5px;")

        # Skapa en box för vänsterinnehållet (explorerknapparna)
        self.leftBox = QtWidgets.QGroupBox("    Explorers")
        self.leftLayout = QtWidgets.QGridLayout(self.leftBox)  
        self.leftBox.setStyleSheet("QGroupBox {border-top: 1px solid rgb(230, 153, 10); border-bottom: 1px solid rgb(230, 153, 10); padding: 5px;}")

        # Skapa en box för högerinnehållet (typ)
        self.rightBox = QtWidgets.QGroupBox("   Söktyp")
        self.rightLayout = QtWidgets.QGridLayout(self.rightBox)  
        self.rightBox.setStyleSheet("QGroupBox {border-top: 1px solid rgb(230, 153, 10); border-bottom: 1px solid rgb(230, 153, 10); padding: 5px;}")

        # Skapa en box för höger-höger-innehållet (längden)
        self.rightestBox = QtWidgets.QGroupBox("   Längd")
        self.rightestLayout = QtWidgets.QGridLayout(self.rightestBox) 
        self.rightestBox.setStyleSheet("QGroupBox {border-top: 1px solid rgb(230, 153, 10); border-bottom: 1px solid rgb(230, 153, 10); padding: 5px;}")

        # Skapa en box för bottom-innehållet (check-knappen och de två knapparna)
        self.bottomBox = QtWidgets.QGroupBox()
        self.bottomLayout = QtWidgets.QHBoxLayout(self.bottomBox)
        self.bottomBox.setStyleSheet("border: 0px; padding: 5px;")

        # Skapa en box för höger och högerhöger-innehållet
        self.rightareaBox = QtWidgets.QGroupBox()
        self.rightareaLayout = QtWidgets.QVBoxLayout(self.rightareaBox)

        # Lägg till vänster- och högerarea i den övre layouten
        self.upperLayout.addWidget(self.leftBox)
        self.upperLayout.addWidget(self.rightareaBox)
        
        # Lägg till höger och högerhöger i högerareaboxen        
        self.rightareaLayout.addStretch()
        self.rightareaLayout.addWidget(self.rightBox)
        self.rightBox.setFixedHeight(88)
        self.rightareaLayout.addWidget(self.rightestBox)
                
        # Skapa textrutan för infotexten
        self.infoText = QtWidgets.QLabel()
        self.infoText.setFixedHeight(88)  # Höjden på textrutan
        self.infoText.setFixedWidth(540)
        self.infoText.setText("När du klickar på check så kommer programmet ta kontroll över musen och genomföra alla klick för sökningen. \nDra musen till skärmens hörn i några sekunder för att avbryta akut.\n\nEndast den sist klickade söktyp/längd kommer sökas, grafikfel.")
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
        self.rightestBox.setObjectName("rightestBox")

        # Skapa scrollområdet för explorerknapparna
        self.scrollArea = QtWidgets.QScrollArea(self.leftBox)
        self.scrollArea.setWidgetResizable(True)
        self.leftLayout.addWidget(self.scrollArea)

        self.scrollContent = QtWidgets.QWidget(self.scrollArea)
        self.scrollArea.setWidget(self.scrollContent)

        self.gridLayout = QtWidgets.QGridLayout(self.scrollContent)

        self.selected_buttons_left = []  # Lista för markerade knappar i vänster box
        self.selected_buttons_right = []  # Lista för markerade knappar i höger box
        self.selected_buttons_rightest = []  # Lista för markerade knappar i höger-höger box

        self.button_images = []
        self.selected_buttons = []
        self.buttonsLeft = []  # Lista för knapparna i vänster box
        self.buttonsRight = []  # Lista för knapparna i höger box
        self.buttonsRightest = []  # Lista för knapparna i högerhöger box

        # Skapa knapparna för explorerna
        for i in range(10, 33):
            value = str(i)  

            button = QtWidgets.QPushButton(self.scrollContent)
            button.setFixedSize(57, 68)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayout.addWidget(button, (i-10) // 4, (i-10) % 4)
            self.buttonsLeft.append(button)

            image = QtGui.QPixmap(f"./src/img/knapp/eknapp_{value}.png")
            self.button_images.append(image)
            button.setIcon(QtGui.QIcon(image))
            button.setIconSize(image.rect().size())
            button.setIconSize(QtCore.QSize(57, 68))
            button.setStyleSheet("QPushButton::icon {"
                                "    position: absolute;"
                                "    bottom: 0;"
                                "    right: 0;"
                                "    border-radius: 5px;"
                                "}")            

        # Skapa scrollområdet för typ-knappar
        self.scrollAreaRight = QtWidgets.QScrollArea(self.rightBox)
        self.scrollAreaRight.setWidgetResizable(True)
        self.rightLayout.addWidget(self.scrollAreaRight)

        self.scrollContentRight = QtWidgets.QWidget(self.scrollAreaRight)
        self.scrollAreaRight.setWidget(self.scrollContentRight)

        self.gridLayoutRight = QtWidgets.QGridLayout(self.scrollContentRight)

        # Skapa knapparna för typen
        for i in range(100, 102):
            value = str(i)

            button = QtWidgets.QPushButton(self.scrollContentRight)
            button.setFixedSize(42, 30)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayoutRight.addWidget(button, (i-100) // 2, (i-100) % 2)
            self.buttonsRight.append(button)  # Uppdaterad namn på listan

            image = QtGui.QPixmap(f"./src/img/knapp/treasure_{value}.bmp")
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

        # Skapa scrollområdet för sökLÄNGDS-knappar
        self.scrollAreaRightest = QtWidgets.QScrollArea(self.rightestBox)
        self.scrollAreaRightest.setWidgetResizable(True)
        self.rightestLayout.addWidget(self.scrollAreaRightest)

        self.scrollContentRightest = QtWidgets.QWidget(self.scrollAreaRightest)
        self.scrollAreaRightest.setWidget(self.scrollContentRightest)

        self.gridLayoutRightest = QtWidgets.QGridLayout(self.scrollContentRightest)

        # Skapa knapparna för söklängd ### Lägg till 4, 5, 6 OM treasure är valt
        for i in range(1000, 1007):
            value = str(i)
            button = QtWidgets.QPushButton(self.scrollContentRightest)
            button.setFixedSize(42, 30)
            button.setCheckable(True)
            button.clicked.connect(lambda _, b=button, v=value: self.button_click(b, v))
            self.gridLayoutRightest.addWidget(button, (i-1000) // 2, (i-1000) % 2)
            self.buttonsRightest.append(button)  # Uppdaterad namn på listan

            image = QtGui.QPixmap(f"./src/img/knapp/time_{value}.bmp")
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


        # Endast en knapp åt gången kan väljas i den högrahögra boxen
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

        back_button.clicked.connect(self.on_returnToDialog)

    def choose_treasure(self):
        self.mode = True
        self.update_length_buttons()

    def choose_adventure(self):
        self.mode = False
        self.update_length_buttons()

    def update_length_buttons(self):
        for button in self.buttonsRightest:
            button.setEnabled(self.mode)

    def on_returnToDialog(self):
        self.close()
        self.returnToDialog.emit()

    def get_button_by_value(self, value):
        for button in self.buttonsLeft + self.buttonsRight + self.buttonsRightest:
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
            elif button in self.buttonsRightest:
                prevrightest_button_value = self.selected_buttons_rightest[0] if self.selected_buttons_rightest else None
                if prevrightest_button_value and prevrightest_button_value != int(value):
                    prevrightest_button_button = self.get_button_by_value(prevrightest_button_value)
                    if prevrightest_button_button:
                        prevrightest_button_button.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}")

                button.setStyleSheet("border: 6px ridge yellow; border-radius: 5px;")
                self.selected_buttons_rightest = [int(value)]  # Spara värdet
        else:
            button.setStyleSheet("")
            if button in self.buttonsLeft:
                self.selected_buttons_left.remove(int(value))
            elif button in self.buttonsRight:
                self.selected_buttons_right = []  # Reset
            elif button in self.buttonsRightest:
                self.selected_buttons_rightest = []  # Reset

        self.selected_buttons = self.selected_buttons_left + self.selected_buttons_right + self.selected_buttons_rightest

        if button in self.buttonsRight:
            self.update_json()  # Updatera json

        if button in self.buttonsRightest:
            self.update_json()  # Updatera json

    def update_json(self):
        json_data = {
            "explorers": self.selected_buttons_left,
            "typ": self.selected_buttons_right,
            "tid": self.selected_buttons_rightest
        }
        with open(f"{app_data_path}/Expl_nummer.json", "w") as json_file:
            json.dump(json_data, json_file)

    def clear_button_click(self):
        self.selected_buttons_left = []  # Återställ markerade knappar i vänster box
        self.selected_buttons_right = []  # Återställ markerade knappar i höger box
        self.selected_buttons_rightest = []  # Återställ markerade knappar i högerhöger box
        for btn in self.buttonsLeft:
            btn.setChecked(False)
            btn.setStyleSheet("")
        for btn in self.buttonsRight:
            btn.setChecked(False)
            btn.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}")
        for btn in self.buttonsRightest:
            btn.setChecked(False)
            btn.setStyleSheet("QPushButton {"
                                "    border: 4px ridge #a49777;"
                                "    border-radius: 5px;"
                                "}")

    def open_miniprogram(self):
        # Close the ExplWindow and open the ProgressDialog
        self.close()
        self.miniprogram = ProgressDialog()
        self.miniprogram.returnToDialog.connect(self.show)  # Show ExplWindow again after ProgressDialog closes
        self.miniprogram.show()     
        self.miniprogram.startProgressDialog.emit()

    def start_process(self):
        self.update_json()  # Update the JSON data before starting the process
        self.open_miniprogram()  # Open the ProgressDialog

    def send_button_click(self):
        if not self.selected_buttons_left or not self.selected_buttons_right:
            QMessageBox.warning(self, "Gör alla val först", "Vänligen välj en explorer, en söktyp och en längd innan du klickar på Check.")
            return
        custom_order = [19, 29, 21, 24, 16, 15, 20, 12, 32, 22, 14, 23, 17, 13, 28, 31, 18, 27, 30, 11, 25, 26, 10]
        explorers_sorted = self.selected_buttons_left[:]
        explorers_sorted = sorted(explorers_sorted, key=lambda x: custom_order.index(x) if x in custom_order else float('inf'))
        typ_value = 100
        if self.selected_buttons_right:
            typ_str = str(self.selected_buttons_right[0])
            if typ_str.isdigit():
                typ_value = int(typ_str)
        tid_value = 1000
        if self.selected_buttons_rightest:
            tid_str = str(self.selected_buttons_rightest[0])
            if tid_str.isdigit():
                tid_value = int(tid_str)

        data = {
            "explorers": list(self.selected_buttons_left),
            "typ": typ_value,
            "tid": tid_value
        }

        with open(f"{app_data_path}/Expl_nummer.json", "w") as json_file:
            json.dump(data, json_file)

        self.close()
        self.miniprogram = ProgressDialog(self.app_data_path)
        self.miniprogram.startProgressDialog.connect(self.start_process)  # Connect the signal to start the process
        self.miniprogram.show()
        self.miniprogram.start_process() # Här startar vi processen i running
        self.miniprogram.returnToDialog.connect(self.show)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ExplWindow()
    app.exec_()