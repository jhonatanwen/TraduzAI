import cv2
import numpy as np
import pytesseract


def process_image(img_path):
    try:
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        config = r'--oem 3 --psm 6 -l jpn'
        text = pytesseract.image_to_string(thresh, config=config)
        return text.strip()

    except Exception as e:
        raise RuntimeError(f"Erro no OCR: {str(e)}")