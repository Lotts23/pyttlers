"""
Image Utils is a module designed for handling image operations
such as opening, converting, scaling, and writing data for images.
Primarily aimed at game automations.
"""

import json
import os
import time

import numpy as np
import pyautogui
from PIL import Image


def find_image(image_path, **kwargs):
    """
    Find an image on the screen using template matching.

    Args:
        image_path (str): Path to the image file to be searched for on the screen.
        **kwargs: Optional keyword arguments for the function.

    Keyword Args:
        scale_factor (float, optional): Scale factor to resize
        the image for matching (default is 0.5).
        confidence (float, optional): Confidence threshold
        for the match (between 0 and 1) (default is 0.8).
        grayscale (bool, optional): If True, perform grayscale matching (default is False).
        search_region (tuple, optional): A tuple (left, top, width, height)
        representing the region where the image will be searched for
        on the screen (default is None).
        sleep_time (float, optional): Time to sleep after the
        function call (default is 0.1 seconds).

    Returns:
        tuple or None: Position of the found image as a tuple (left, top, width, height),
                       or None if the image is not found.
    """
    scale_factor = kwargs.get("scale_factor", 0.5)
    confidence = kwargs.get("confidence", 0.8)
    grayscale = kwargs.get("grayscale", True)
    search_region = kwargs.get("search_region", None)
    sleep_time = kwargs.get("sleep_time", 0.1)

    for _ in range(2): # Loop 2 times unless found
        found_position = None
        image = Image.open(image_path)
        scaled_image = image.resize(
                                    (int(image.width * scale_factor),
                                     int(image.height * scale_factor))
                                    )
        image_array = np.array(scaled_image)

        found_position = pyautogui.locateOnScreen(
            image_array,
            confidence=confidence,
            grayscale=grayscale,
            region=search_region
            )
        if found_position is not None:
            return found_position

    time.sleep(sleep_time)
    return None

def click_center(image_position, **kwargs):

    """
    Click on the center of the specified image position.

    Args:
        image_position (tuple): Position of the image as a tuple (left, top, width, height).
        sleep_time (float, optional): Time to sleep after the click (default is 0.1 seconds).

    Returns:
        None
    """
    button = kwargs.get("button", "left")
    sleep_time = kwargs.get("sleep_time", 0.1)

    if image_position is not None:
        center = pyautogui.center(image_position)
        pyautogui.moveTo(center)
        pyautogui.mouseDown(center, button=button)
        pyautogui.mouseUp()
        time.sleep(sleep_time)

def json_handler(
    data,
    data_type,
    app_data_path,
    json_folder,
    mode="read"
):
    """
    Read or write data to a JSON file.

    Parameters:
        data (dict): The data to be written to or read from the JSON file.
        data_type (str): The type of data being stored in the JSON file.
        app_data_path (str): The path to the application's data directory.
        json_folder (str): The name of the subdirectory where JSON files are stored.
        mode (str, optional): The file operation mode, either "write" (default) or "read".

    Example:
        # Writing data to JSON file
        json_handler(data={"scale": 0.75, "resolution": "1080p"}, data_type="scale_data",
                     app_data_path="/path/to/your/app_data_directory",
                     json_folder="json_files", mode="write")

        # Reading data from JSON file
        data = json_handler(data_type="scale_data",
        app_data_path="/path/to/your/app_data_directory",
                            json_folder="json_files")
    """
    json_file_path = os.path.join(app_data_path, json_folder, f"{data_type}.json")
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

    if mode == "write":
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file)
    elif mode == "read":
        with open(json_file_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
