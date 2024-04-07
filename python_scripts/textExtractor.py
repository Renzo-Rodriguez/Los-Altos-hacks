import cv2
import numpy as np
import easyocr
import pyautogui
import time

reader = easyocr.Reader(['en'])
final_extracted_text = None
final_extracted_text_x_coords = None
final_extracted_text_y_coords = None


def extract_text(image):

    averageX = [];
    averageY = [];

    results = reader.readtext(image)

    extracted_text = [result[1] for result in results]
    extracted_text_box_coords = [result[0] for result in results]
    extracted_text_coords_1 = [coord[1] for coord in extracted_text_box_coords]
    extracted_text_coords_2 = [coord[3] for coord in extracted_text_box_coords]
    extra_extracted_text_coords_1 = [coord[0] for coord in extracted_text_coords_1]
    extra_extracted_text_coords_2 = [coord[1] for coord in extracted_text_coords_1]
    extra_extracted_text_coords_3 = [coord[0] for coord in extracted_text_coords_2]
    extra_extracted_text_coords_4 = [coord[1] for coord in extracted_text_coords_2]

    for i in range(len(extra_extracted_text_coords_1)):
        avg = (extra_extracted_text_coords_1[i] + extra_extracted_text_coords_3[i]) / 2
        averageX.append(avg)
        
    for i in range(len(extra_extracted_text_coords_2)):
        avg = (extra_extracted_text_coords_2[i] + extra_extracted_text_coords_4[i]) / 2
        averageY.append(avg)
    
    final_extracted_text = extracted_text
    final_extracted_text_x_coords = averageX
    final_extracted_text_y_coords = averageY


    # averageXButInAStringIGuess = [str(x) for x in averageX]
    # averageYButInAStringIGuess = [str(y) for y in averageY]

    # returnThis = ' '.join(extracted_text)

    # print(returnThis)
    # print(" ".join(averageXButInAStringIGuess))
    # print(" ".join(averageYButInAStringIGuess))

last_screenshot_time = 0
screenshot_interval = 5  # seconds

while True:
    current_time = time.time()
    if current_time - last_screenshot_time >= screenshot_interval:
        screenshot = pyautogui.screenshot(region=(200,200, 1720, 880))

        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        extract_text(frame)

        last_screenshot_time = current_time

    time.sleep(1)