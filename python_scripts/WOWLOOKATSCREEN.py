import numpy as np
import cv2
from mss import mss
import pytesseract

# Path to Tesseract executable (change this based on your Tesseract installation)
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

bounding_box = {'top': 0, 'left': 0, 'width': 300, 'height': 300}

sct = mss()

# Function to extract text from a frame
def extract_text(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use OpenCV's thresholding to preprocess the frame
    _, threshold_frame = cv2.threshold(gray_frame, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Use Tesseract to extract text from the frame
    extracted_text = pytesseract.image_to_string(threshold_frame)

    return extracted_text

while True:
    sct_img = sct.grab(bounding_box)
    frame = np.array(sct_img)
    d = pytesseract.image_to_data(frame, output_type=pytesseract.Output.DICT)
    n_boxes = len(d['text'])
    
    for i in range(n_boxes):
        if int(d['conf'][i]) > 0:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Extract text from the frame
    extracted_text = extract_text(frame)

    # Display the frame with extracted text
    cv2.imshow('screen', frame)
    print("Extracted Text:")
    print(extracted_text)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
