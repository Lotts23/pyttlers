import pyautogui


def berakna_starmenu(bild_sokvag):   # Definierar starmenu_area för att söka på begränsad yta 
    global starmenu_area

    hittad_position = pyautogui.locateOnScreen(bild_sokvag)

    if hittad_position is not None: # Om stjärnan hittas
        x, y, bredd, hojd = hittad_position
        starmenu_bredd = bredd * 10
        starmenu_höjd = hojd * 8.8

        #Beräkna det begränsade området
        starmenu_x = x - int(starmenu_bredd / 2)
        starmenu_y = y
        starmenu_area = (starmenu_x, starmenu_y, round(starmenu_bredd), round(starmenu_höjd))    
        return starmenu_area, starmenu_bredd, starmenu_höjd
        
starmenu_area = berakna_starmenu("img/02_image.bmp")

import pyautogui

def berakna_starmenu(bild_sokvag):
    global starmenu_area

    hittad_position = pyautogui.locateOnScreen(bild_sokvag)

    if hittad_position is not None:
        pyautogui.moveTo(hittad_position)
        x, y, bredd, hojd = hittad_position
        starmenu_bredd = bredd * 10
        starmenu_höjd = hojd * 8.8

        starmenu_x = x - int(starmenu_bredd / 2)
        starmenu_y = y
        starmenu_area = (starmenu_x, starmenu_y, round(starmenu_bredd), round(starmenu_höjd))    
        return starmenu_area, starmenu_bredd, starmenu_höjd

starmenu_area = berakna_starmenu("img/02_image.bmp")

def draw_area(starmenu_area):
    x, y, bredd, hojd = starmenu_area

    pyautogui.moveTo(x, y)
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    pyautogui.mouseDown()
    pyautogui.moveRel(bredd, 0, duration=0.5)  # Flytta till höger
    pyautogui.moveRel(0, hojd, duration=0.5)   # Flytta nedåt
    pyautogui.moveRel(-bredd, 0, duration=0.5) # Flytta till vänster
    pyautogui.moveRel(0, -hojd, duration=0.5)  # Flytta uppåt
    pyautogui.mouseUp()

draw_area(starmenu_area)

    
"""
            x, y, width, height = hittad_position
            #area_width, area_height = starmenu_area[2], starmenu_area[3]
            print(x, starmenu_area[0], y, starmenu_area[1])
            # Om den hittar en geolog längst bort på en rad, scrolla åt det hållet
            if x <= starmenu_area[0] and y <= starmenu_area[1]:"""