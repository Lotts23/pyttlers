import json
import os
import sys
import threading
import time

import cv2
import numpy as np
import pyautogui
from PIL import Image
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QEvent, QRect, Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QDialog, QLabel,
                             QMainWindow, QMessageBox, QPushButton,
                             QStackedWidget, QVBoxLayout, qApp)

import image_utils

typ = 100
tid = 1000
faktor = None
explorer = None
resting_place = 200, 200 # Bara för att alltid iallf ha nån giltlig resting_place - alltså där inga inforutor stör sökningen
command_area = 0
starmenu_area = 0
noscroll = False

class ProgressDialog(QtWidgets.QDialog):
    startProgressDialog = QtCore.pyqtSignal()
    returnToDialog = QtCore.pyqtSignal()

    def __init__(self, app_data_path):
        super(ProgressDialog, self).__init__()
        self.app_data_path = app_data_path
        self.initUI()
        self.setWindowTitle("Pågår...")

        self.setFixedSize(350, 220)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Fönstret alltid överst

        self.setStyleSheet(open("./data/stil.css").read())  # Länk till stil.css

        desktop = QApplication.desktop()
        screen_rect = desktop.availableGeometry()
        self.setGeometry(QRect(screen_rect.width() - self.width(), 0, self.width(), self.height()))

    typ = 100
    tid = 1000
    faktor = None
    explorer = None
    resting_place = 200, 200 # Bara för att alltid iallf ha nån giltlig resting_place - alltså där inga inforutor stör sökningen
    command_area = 0
    starmenu_area = 0
    noscroll = False

    def hitta_skalfaktor(self, skalbild_sokvag):# Här kollar vi skalan och ser till att stjärn-fönstret är öppen och i rätt tab.
        tillatna_varden = [1, 0.75, 0.625, 0.55, 0.5, 0.45, 0.375, 0.25]
        global faktor
        faktor = faktor
        for faktor in tillatna_varden:
            #print(faktor * 2 * 100, "%")
            skalbild = Image.open(skalbild_sokvag)
            skalad_bild = skalbild.resize((int(skalbild.width * faktor), int(skalbild.height * faktor)))
            skalbild_array = np.array(skalad_bild)
            hittad_skalfaktor = pyautogui.locateOnScreen(skalbild_array, confidence=0.63, grayscale=True)
            if hittad_skalfaktor is not None:
                data = {"faktor": faktor}
                with open(f"{self.app_data_path}/scale_data.json", "w") as json_file:
                    json.dump(data, json_file)
                return faktor
            time.sleep(0.01)
        ### Skriv en felhantering för när skalan inte hittas
        return

    def testa_skalfaktor(self, skalbild_sokvag, faktor):
        testbild = Image.open(skalbild_sokvag)
        testad_bild = testbild.resize((int(testbild.width * faktor), int(testbild.height * faktor)))
        testbild_array = np.array(testad_bild)
        hittad_testbild = pyautogui.locateOnScreen(testbild_array, confidence=0.8, grayscale=True)

        if hittad_testbild is not None:
            return faktor
        else:
            self.hitta_skalfaktor("./data/img/01_image.bmp")
            return faktor

    def oppna_stjarna(self, bild_sokvag, faktor):
        hittad = None
        hittad_position = image_utils.find_image(bild_sokvag, confidence=0.8, scale_factor=faktor)
        time_limit = 0
        meny_bild_sokvag = "./data/img/02_image.bmp"
        meny_opened = None
        if hittad_position is not None: #klicka
            hittad = pyautogui.center(hittad_position)
            pyautogui.moveTo(hittad)
            pyautogui.mouseDown(hittad)
            pyautogui.mouseUp()
            time.sleep(0.1)  # minskar fel
            return hittad
        while meny_opened is None:
            meny_opened = image_utils.find_image(meny_bild_sokvag, confidence=0.75, scale_factor=faktor)
            time_limit = time_limit + 1
            if meny_opened is not None:
                break
            if time_limit >= 20:
                break

    def hitta_bild_stjarna(self, bild_sokvag, faktor):    # kolla om stjärnmeny Else öppna stjärna
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=True)
        if hittad_position is not None:
            pass
        else:
            self.oppna_stjarna("./data/img/03_image.bmp", faktor) # Här öppnas stjärnan om stjärnmenyn inte hittats.

    def tab_stjarna(self, bild_sokvag, faktor):
        hittad = None
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=True) #, region=starmenu_area)
        if hittad_position is not None:
            hittad = pyautogui.center(hittad_position)
            time.sleep(0.1)  # minskar fel
            pyautogui.moveTo(hittad)
            pyautogui.mouseDown(hittad)
            pyautogui.mouseUp()

    def check_if_scrollbar(self, bild_sokvag, faktor):
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=True) #, region=starmenu_area)
        if hittad_position is not None:
            return True
        return False

    def sortera_klick(self, bild_sokvag, faktor, hittad_position):
        reset_point = hittad_position
        for _ in range(3):  # Loopa 3 gånger
            check_box = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=True)
            if check_box is not None:
                x, y, width, height = check_box
                check_box = x + width - (width // 7), y + (height // 2)
                pyautogui.moveTo(check_box)
                time.sleep(0.1)
                pyautogui.mouseDown(check_box)
                pyautogui.mouseUp()
                return True
            time.sleep(0.1)
        pyautogui.mouseDown(reset_point)
        pyautogui.mouseUp()

    def sortera(self, bild_sokvag, faktor):
        for _ in range(1):
            bild = Image.open(bild_sokvag)
            skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
            bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
            hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.85, grayscale=False)
            if hittad_position is not None:
                pyautogui.mouseDown(hittad_position)
                pyautogui.mouseUp()
                time.sleep(0.1)
                self.sortera_klick("./data/img/06_image.bmp", faktor, hittad_position)
        return False

    def berakna_starmenu(self, bild_sokvag, faktor):   # Definierar starmenu_area för att söka på begränsad yta
        global starmenu_area
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.7, grayscale=True)

        if hittad_position is not None: # Om stjärnan hittas
            x, y, width, height = hittad_position
            starmenu_width = width * 10.1
            starmenu_height = height * 8

            #Beräkna det begränsade området
            starmenu_x = x - int(starmenu_width / 2.1)
            starmenu_y = y + int(y / 8)
            starmenu_area = (starmenu_x, starmenu_y, round(starmenu_width), round(starmenu_height))
            return starmenu_area

    def find_resting_place(self, bild_sokvag, faktor):
        found_starmenu = None
        global resting_place
        time.sleep(0.1)
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=False)
        if hittad_position is not None:
            found_starmenu = pyautogui.center(hittad_position)
            x, y, width, height = starmenu_area
            resting_place = (x + width, y + (height / 3))
            pyautogui.mouseDown(found_starmenu)
            pyautogui.mouseUp()
            pyautogui.moveTo(resting_place)
            time.sleep(0.1)
            return resting_place
        else:
            time.sleep(0.1)
            return None

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        try:
            with open(f"{self.app_data_path}/scale_data.json", "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                faktor = data["faktor"]
        except FileNotFoundError:
            faktor = 0.5

        with open(f"{self.app_data_path}/expl_nummer.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            explorers = data["explorers"]
            typ = data["typ"]
            tid = data["tid"]

        with open("./data/expl_namn.json", "r", encoding="utf-8") as expl_file:
            expl_data = json.load(expl_file)
            expl_dict = expl_data

        with open("./data/typ_namn.json", "r", encoding="utf-8") as typ_file:
            typ_data = json.load(typ_file)
            typ_dict = typ_data

        with open("./data/tid_namn.json", "r", encoding="utf-8") as tid_file:
            tid_data = json.load(tid_file)
            tid_dict = tid_data

        explorers_namn = [expl_dict[str(num)] for num in explorers]
        typ_namn = typ_dict[str(typ)]
        tid_namn = tid_dict[str(tid)]

        self.label = QLabel(self)
        explorers_str = ", ".join(explorers_namn)
        self.label.setText(f"Process pågår...\n\nSöker {explorers_str} som ska leta efter {typ_namn} under {tid_namn} tid.\n\nNödstopp genom att flytta musen till skärmens hörn.")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.restart_button = QPushButton("Upprepa", self)
        layout.addWidget(self.restart_button)
        self.restart_button.clicked.connect(self.start_process_again)
        self.restart_button.setVisible(False)

        self.start_button = QtWidgets.QPushButton("Nytt val", self)
        layout.addWidget(self.start_button)
        self.start_button.clicked.connect(self.on_returnToDialog)
        self.start_button.setVisible(False)

        self.stop_action = QAction("Avsluta (q)", self)
        self.stop_action.setShortcut(QKeySequence("q"))
        self.stop_action.triggered.connect(self.stop_process)
        self.addAction(self.stop_action)

        self.stop_button = QPushButton("Avsluta", self)
        layout.addWidget(self.stop_button)
        self.stop_button.clicked.connect(self.stop_process)
        self.stop_button.setVisible(False)

        self.handbrake_button = QPushButton("Nödstopp", self)
        layout.addWidget(self.handbrake_button)
        self.handbrake_button.clicked.connect(self.handbrake)
        self.handbrake_button.setVisible(True)

    def on_returnToDialog(self):
        self.returnToDialog.emit()
        self.close()

    def stop_process(self):
        self.close()  # Stäng minifönstret och avbryt processen
        qApp.quit()  # Avsluta programmet

    def handbrake(self):
        #print("handbrake(self)"),
        self.close()  # Stäng minifönstret och avbryt processen
        os._exit(0)
    def start_process(self):
        QApplication.processEvents()
        self.show()
        self.prepare()
        QApplication.processEvents()
        self.leta_skatt()  # Starta leta_skatt-funktionen
        self.process_completed()

    def start_process_again(self):
        with open("./data/expl_namn.json", "r", encoding="utf-8") as expl_file:
            expl_data = json.load(expl_file)
            expl_dict = expl_data

        with open("./data/typ_namn.json", "r", encoding="utf-8") as typ_file:
            typ_data = json.load(typ_file)
            typ_dict = typ_data

        with open("./data/tid_namn.json", "r", encoding="utf-8") as tid_file:
            tid_data = json.load(tid_file)
            tid_dict = tid_data
        explorers_namn = [expl_dict[str(num)] for num in explorers]
        typ_namn = typ_dict[str(typ)]
        tid_namn = tid_dict[str(tid)]

        self.label.clear()
        explorers_str = ", ".join(explorers_namn)
        self.label.setText(f"Upprepar...\n\nSöker {explorers_str} som ska leta efter {typ_namn} under {tid_namn}.\n\nNödstopp genom att flytta musen till skärmens hörn.")
        self.label.setWordWrap(True)
        self.restart_button.setVisible(False)
        self.start_button.setVisible(False)
        self.stop_button.setVisible(False)
        self.handbrake_button.setVisible(True)
        QApplication.processEvents()  # Uppdatera GUI-tråden
        self.leta_skatt()
        self.process_completed()

    def process_completed(self, *args):
        QApplication.processEvents()
        self.label.setText("Processen är klar.\nAlla möjliga klick är genomförda.")
        self.restart_button.setVisible(True)
        self.start_button.setVisible(True)
        self.stop_button.setVisible(True)
        self.handbrake_button.setVisible(False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.handbrake()
        else:
            super().keyPressEvent(event)

    def prepare(self):
        json_fil = f"{self.app_data_path}/scale_data.json"
        global faktor
        global noscroll
        global resting_place
        global starmenu_area
        noscroll = False
        faktor = None
        if os.path.isfile(json_fil):  # Om det finns en fil
            with open(json_fil, "r") as json_file:  # öppna den
                json_data = json.load(json_file)  # och läs datan
                faktor = json_data.get("faktor")  # Hämta tidigare faktor
            if faktor is not None: # Om faktor-värdet inte är tomt, testa det
                self.testa_skalfaktor("./data/img/01_image.bmp", faktor) # Testar om gamla faktorn funkar
                if faktor is None:
                    self.hitta_skalfaktor("./data/img/01_image.bmp")
        else:
            faktor = self.hitta_skalfaktor("./data/img/01_image.bmp")
        with open(f"{self.app_data_path}/scale_data.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            faktor = data["faktor"]
        self.hitta_bild_stjarna("./data/img/02_image.bmp", faktor) # Kör hitta om stjärnmenyn är öppen, else kör öppna stjärnan.
        self.tab_stjarna("./data/img/04_image.bmp", faktor) # Gå till rätt tab så blir det inte så mycket scroll
        starmenu_area = self.berakna_starmenu("./data/img/02_image.bmp", faktor)
        self.sortera("./data/img/07_image.bmp", faktor)
        scrollbar = self.check_if_scrollbar("./data/img/08_image.bmp", faktor)
        if scrollbar is False:
            scrollbar = self.check_if_scrollbar("./data/img/09_image.bmp", faktor)
            if scrollbar is False:
                noscroll = True
        with open(f"{self.app_data_path}/expl_nummer.json", "r", encoding="utf-8") as json_file:
            global explorers
            global typ
            global tid
            data = json.load(json_file)
            explorers = data["explorers"]
            typ = data["typ"]
            tid = data["tid"]
        resting_place = self.find_resting_place("./data/img/02_image.bmp", faktor)
        return resting_place, starmenu_area, explorers, typ, tid, faktor, noscroll

#
#   Nu börjar sökningen på riktigt
#

    def hitta_scroll(self, bild_sokvag, faktor):
        hittad_position = None
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=True)
        if hittad_position is None:
            time.sleep(0.01)
            return False # inte hittad
        else:
            return True # hittad

    def scroll(self, explorer):
        vimpel = False
        riktning = -2
        counting = 0
        been = None
        position_top = False
        position_bottom = False
        safestop = 0
        while vimpel is False and explorer is not None: # När en viss explorer saknas
            individ = explorer
            position_top = self.hitta_scroll("./data/img/top.bmp", faktor)
            position_bottom = self.hitta_scroll("./data/img/bottom.bmp", faktor)
            hittad_explorer = self.hitta_scroll(f"./data/img/expl_{individ}.bmp", faktor)
            safestop += 1
            if hittad_explorer or noscroll is True:
                vimpel = True
                return vimpel
            pyautogui.moveTo(resting_place)
            pyautogui.mouseDown(resting_place)
            pyautogui.mouseUp()
            pyautogui.scroll(clicks=riktning)
            if position_bottom is True:
                riktning = 2 # Om vi är längst ner börja skrolla upp
                counting += 1
                if been is None:
                    been = "bottom"
            if position_top is True:
                riktning = -2
                counting += 1
                if been is None:
                    been = "top"
            if counting >= 2 and position_top is True and been == "bottom":
                vimpel = False
                return None
            if counting >= 2 and position_bottom is True and been == "top":
                vimpel = False
                return None
            # Håll reda på hur många scroll-sök så det inte spårar ut
            if counting >= 3 or safestop == 30:
                return None

    def berakna_command(self, bild_sokvag, faktor): # Hitta sökområdet för typer och check. # Behöver finslipas
        global command_area
        hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.8, grayscale=True)
        if hittad_position is not None:
            x, y, width, height = hittad_position
            command_width = width * 5
            command_height = height * 15
            #Beräkna det begränsade området
            command_x = x + int(width / 2) - int(command_width / 2)
            command_y = y
            command_area = (command_x, command_y, round(command_width), round(command_height))
            return command_area

    def hitta_typ(self, bild_sokvag, faktor):
        for _ in range(3):  # Loopa 3 gånger för varje försök
            hittad_position = image_utils.find_image(bild_sokvag, scale_factor=faktor, confidence=0.85, grayscale=True)#, region=command_area)
            if hittad_position is not None:
                x, y, width, height = hittad_position  # Klickar i högra hörnet för att kunna ha med texten brevid knappen
                knappens_plats = x + width - (width // 5), y + (height // 2)
                pyautogui.moveTo(knappens_plats)
                pyautogui.mouseDown(knappens_plats)
                pyautogui.mouseUp()
                pyautogui.moveTo(resting_place)
                return True
            time.sleep(0.1)
        return False

    def hitta_tid(self, bild_sokvag, faktor):
        #for _ in range(3):  # Loopa 3 gånger
        #global command_area
        #command_area = berakna_command("./data/img/05_image.bmp", faktor)
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        for _ in range(3):  # Loopa 3 gånger för varje försök
            hittad_position = pyautogui.locateOnScreen(bild_array, confidence=0.83, grayscale=True)#, region=command_area)
            if hittad_position is not None:
                x, y, width, height = hittad_position  # Klickar i högra hörnet för att kunna ha med texten brevid knappen
                knappens_plats = x + width - (width // 6), y + (height // 2)
                pyautogui.moveTo(knappens_plats)
                pyautogui.mouseDown(knappens_plats)
                pyautogui.mouseUp()
                pyautogui.moveTo(resting_place)
                return True
            time.sleep(0.1)
        return False#, command_area

    def hitta_check(self, bild_sokvag, faktor):
        for _ in range(3): # Loopa 3ggr
            hittad_position = image_utils.find_image(bild_sokvag, confidence=0.8, grayscale=False, region=command_area, scale_factor=faktor, sleep_time=0.1)
            if hittad_position is not None:
                hittad_check = pyautogui.center(hittad_position)
                pyautogui.moveTo(hittad_check)
                pyautogui.mouseDown(hittad_check)
                pyautogui.mouseUp()
                pyautogui.moveTo(resting_place)
                pyautogui.mouseDown(resting_place)
                pyautogui.mouseUp()
                time.sleep(0.5)  # minskar fel
                break
        time.sleep(0.1)

    def error_bild(self, bild_sokvag, faktor):
        bild = Image.open(bild_sokvag)
        skalad_bild = bild.resize((int(bild.width * faktor), int(bild.height * faktor)))
        bild_array = np.array(skalad_bild)  # Konvertera PIL-bilden till en array
        bild_array = cv2.cvtColor(bild_array, cv2.COLOR_RGB2BGR)
        error_found = pyautogui.locateOnScreen(bild_array, confidence=0.8, grayscale=False)
        if error_found is not None:
            self.popup_flagga.set()
            pyautogui.mouseDown(error_found)
            pyautogui.mouseUp()
            pyautogui.press('esc')
            time.sleep(0.1)
            self.hitta_bild_stjarna("./data/img/02_image.bmp", faktor)

    def hantera_popup(self):
        while not self.popup_flagga.is_set():
            time.sleep(2)
            self.error_bild("./data/img/error.bmp", faktor)

    popup_flagga = threading.Event()

    def hitta_explorer(self, bild_sokvag, faktor, search_area):
        global flagga
        flagga = True
        hittad = None
        global sort
        if typ == 100:
            sort = "t"
        else:
            sort = "a"
        pyautogui.moveTo(resting_place)
        hittad_position = None
        window_open = False
        hittad = None
        for _ in range(3): # Loopa 3ggr om den INTE hittar

            hittad_position = image_utils.find_image(bild_sokvag, confidence=0.77, grayscale=True, region=search_area)
            self.popup_flagga.clear()
            if hittad_position is not None:
                hittad = pyautogui.center(hittad_position)
                self.popup_flagga.clear()
                popup_trad = threading.Thread(target=self.hantera_popup)
                popup_trad.start()
                #pyautogui.moveTo(hittad)
                pyautogui.mouseDown(hittad)
                pyautogui.mouseUp()
                pyautogui.moveTo(resting_place) # För att bli av med popup-bubblan
                time.sleep(0.1)
                window_open = self.hitta_typ(f"./data/img/typ_{typ}.bmp", faktor)
                self.popup_flagga.set()
                if window_open is False:
                    continue
                self.hitta_tid(f"./data/img/tid_{sort}_{tid}.bmp", faktor)
                self.hitta_check("./data/img/check.bmp", faktor)
                # Hämtar alla värden för hittad_position och starmenu_area så att vi kan scrolla senare
                found_x, found_y, found_width, found_height = hittad_position
                lower_corner_x, lower_corner_y = int(found_x + (found_width * faktor)), found_y + found_height # Av den hittade bilden
                upper_corner_x, upper_corner_y = found_x, found_y
                x, y, width, height = starmenu_area
                right_limit = starmenu_area[0] + starmenu_area[2] - (found_width / 2)
                left_limit = starmenu_area[0]
                #pyautogui.moveTo(hittad)
                # Jämför hittad position + X med starmenu_area så att denna aldrig är större
                next_x = min(hittad_position[0] + (found_width * faktor * 0.3), right_limit)
                next_x = max(next_x, left_limit)
                # Om den hittar en explorer längst bort på en rad, scrolla åt det hållet
                if lower_corner_x <= (x + (found_width * 1.9)) and lower_corner_y <= (y + (found_height * 1.9)) and noscroll is False:
                    pyautogui.moveTo(resting_place)
                    pyautogui.mouseDown(resting_place)
                    pyautogui.mouseUp()
                    pyautogui.scroll(clicks=2)
                    time.sleep(0.1)
                    search_area = starmenu_area
                if upper_corner_x >= (x + width - (found_width * 1.9)) and upper_corner_y >= (y + height - (found_height * 1.9)) and noscroll is False:
                    pyautogui.moveTo(resting_place)
                    pyautogui.mouseDown(resting_place)
                    pyautogui.mouseUp()
                    pyautogui.scroll(clicks=-2)
                    time.sleep(0.1)
                    search_area = starmenu_area
                flagga = True # Vi har hittat den
                if found_x + found_width >= x + width - found_width:
                    # If we find it furthest to the right, start to the very left again
                    search_area = starmenu_area
                    time.sleep(0.1)
                else:
                    # When an image have been found we move the search to the right of that
                    search_area = (int(next_x), int(starmenu_area[1]), int(starmenu_area[2] - found_width), int(starmenu_area[3]))
                return hittad, search_area # Om den hittas lämnar vi loopen, itereringen sköts i leta_sten
            else:
                time.sleep(0.1)
                search_area = starmenu_area
                self.popup_flagga.clear()
        return hittad, search_area # Om den inte hittats har hittad inget värde

    def leta_skatt(self):
        with open(f"{self.app_data_path}/scale_data.json", "r") as json_file:
            data = json.load(json_file)
            faktor = data["faktor"]
            self.faktor = data["faktor"]
        global flagga
        global explorer
        global resting_place
        hitta = None
        for explorer in explorers:
            flagga_funnen = False
            search_area = starmenu_area
            flagga = True
            pyautogui.moveTo(resting_place)
            while flagga:
                hittad_explorer, search_area = self.hitta_explorer(f"./data/img/expl_{explorer}.bmp", faktor, search_area) # Returnerar hittad/none
                if hittad_explorer is not None:
                    flagga_funnen = True
                    flagga = True
                elif hittad_explorer is None and flagga_funnen is False and noscroll is False: # En tidigare hittad explorer behöver inte sökas efter utöver när-scrollet i hitta_explorer
                    hitta = self.scroll(explorer)
                    if hitta is not None:
                        flagga = True # Upprepa hitta_explorer
                    else:
                        flagga = False # Avbryt och börja leta efter nästa explorer.
                elif hittad_explorer is None and flagga_funnen is False and noscroll is True:
                    flagga = False
                elif hittad_explorer is None and flagga_funnen is True:
                    flagga = False # Avbryt direkt och gå vidare i listan.
