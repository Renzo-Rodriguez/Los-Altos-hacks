import cv2
import numpy as np
import easyocr
import pyautogui
import time
import json
import requests

api_key = "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"
reader = easyocr.Reader(['en'])
final_extracted_text = None
final_extracted_text_x_coords = None
final_extracted_text_y_coords = None
final_response_text = []
flag = True

def extract_text(image):

    flag = False
    averageX = [];
    averageY = [];

    results = reader.readtext(image)

    extracted_text = [result[1] for result in results if result[2] >= 0.9]
    extracted_text_box_coords = [result[0] for result in results if result[2] >= 0.9]
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
        
    for i in range(len(extracted_text)):    
        headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
        
        payload = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "With the context that you are an AI assistant viewing portions of text from a viewers screen, please provide any advice you have about this portion of text, or reply with nothing if it is too concise or if there is nothing of value you can provide. THIS IS VERY IMPORTANT: IF THERE IS NOT ENOUGH INFORMATION TO GIVE ANY ADVICE, PLEASE DO NOT REPLY AND INSTEAD REPLY WITH A BLANK. The text will now be provided: " + extracted_text[i]
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        print('sent request')
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        if response.json() is not None:
            final_response_text.append(response.json()["choices"][0]["message"]["content"])
        else:
            final_response_text.append(" ")
    
    print('dumping')
    with open('text.json', 'w') as f:
        json.dump(final_response_text, f)
    with open('xCoord.json', 'w') as f:
        json.dump(averageX, f)
    with open('yCoord.json', 'w') as f:
        json.dump(averageY, f)

    flag = True
    # averageXButInAStringIGuess = [str(x) for x in averageX]
    # averageYButInAStringIGuess = [str(y) for y in averageY]

    # returnThis = ' '.join(extracted_text)

    # print(returnThis)
    # print(" ".join(averageXButInAStringIGuess))
    # print(" ".join(averageYButInAStringIGuess))

# last_screenshot_time = 0
# screenshot_interval = 10  # seconds

while True:
    # current_time = time.time()
    if flag:
        screenshot = pyautogui.screenshot(region=(400,400, 1520, 680))

        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        extract_text(frame)

        # last_screenshot_time = current_time

    time.sleep(1)