import pyautogui
from PIL import Image
import time
import base64
import requests

api_key = "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"

def screenshot_area_around_mouse(width, height):
    x, y = pyautogui.position()
    left = x - width // 2
    top = y - height // 2
    right = left + width
    bottom = top + height
     screenshot = pyautogui.screenshot(region=(left, top, width, height))

    return screenshot

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

def main():
    area_width = 300
    area_height = 300
     while True:
        screenshot = screenshot_area_around_mouse(area_width, area_height)
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        base64_image = encode_image(screenshot_path)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What’s in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        print(response.json())

        time.sleep(5)

if __name__ == "__main__":
    main()
