import cv2
import numpy as np
import pytesseract
import pandas as pd
from googletrans import Translator


def format_txt(txt):
    txt = str(txt).strip()

    new_txt = ""
    try:
        for sentence in txt.splitlines():
            sentence = sentence.strip()
            if(len(sentence) > 0):
                new_txt += sentence + "\n"

        new_txt = new_txt.strip()
        if(len(new_txt) > 0):
            print('-----------------------------------')
            print(new_txt)
            print('-----------------------------------')
            return new_txt
        else:
            return None

    except Exception as e:
        print(e)
        return None


def image_to_text_hindi(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        custom_config = r'-l hin --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        return format_txt(txt)
    except Exception as e:
        print(e)
        return None


def hindi_to_english(txt):
    translator = Translator()
    translator.raise_Exception = True
    translated = translator.translate(txt, src='hi', dest='en')
    return format_txt(translated.text)

def image_to_text_english(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        custom_config = r'-l eng+hin --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        try:
            translator = Translator()
            translator.raise_Exception = True
            translated = translator.translate(txt, src='hi', dest='en')
        except Exception as e:
            print(e)
            translated = txt

        return format_txt(translated.text)
    except Exception as e:
        print(e)
        return None


input_img = cv2.imread("voter_influencer/media/booth/images/1/cropped/17.png")

cropped_image = input_img[10:70, 30:260]
image_to_text_english(cropped_image)
#image_to_text_hindi(cropped_image)
# cv2.imshow("cropped", cropped_image)
# cv2.waitKey(0)

cropped_image = input_img[10:85, 800:1230]
image_to_text_english(cropped_image)
# image_to_text_hindi(cropped_image)
# cv2.imshow("cropped", cropped_image)
# cv2.waitKey(0)


cropped_image = input_img[70:480, 10:900]
image_to_text_english(cropped_image)
image_to_text_hindi(cropped_image)

cv2.imshow("cropped", cropped_image)
cv2.waitKey(0)

# ID: 1 x 8, y 0, w 96, h 23  - Serial ID
# ID: 2 x 0, y 0, w 496, h 188 
# ID: 3 x 152, y 31, w 48, h 8 
# ID: 4 x 372, y 47, w 112, h 137 
# ID: 5 x 122, y 60, w 66, h 8 
# ID: 6 x 30, y 89, w 48, h 8 
# ID: 7 x 142, y 116, w 41, h 8 ``