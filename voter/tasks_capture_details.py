import os
import cv2
from .models import PollingStationImage, VoterImage, Voter
import numpy as np
import pytesseract
from googletrans import Translator
from textblob import TextBlob

def format_voter_details(txt):
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


def get_voter_details(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        custom_config = r'-l hin+eng --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        tb = TextBlob(txt)
        return format_voter_details(tb)
    except Exception as e:
        print(e)
        return None


def update_details():
    
    voter_images = VoterImage.objects.filter(is_voter_id_captured=True, is_details_captured=False)[:100]

    for voter_image in voter_images:
        img_rgb = cv2.imread(voter_image.image.path)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("voter_influencer/media/train_details.png")
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        w, h = template_gray.shape[::-1]

        methods = ['cv2.TM_CCOEFF_NORMED']      
        
        # for meth in methods:
        method = eval('cv2.TM_CCOEFF_NORMED')
        # Apply template Matching
        res = cv2.matchTemplate(img_gray, template_gray, method)
        threshold = 1
        loc = np.where( res >= threshold)
        points = list(zip(*loc[::-1]))
        while len(points)<=0:
            threshold = threshold - 0.1
            loc = np.where( res >= threshold)
            points = list(zip(*loc[::-1]))

        # for pt in points:
        pt = points[0]
        x= pt[0]
        y= pt[1]
        new_img = img_rgb[y:y+h, x:x+w]
        data_hin = get_voter_details(new_img)

        voter = Voter.objects.get(md5_signature=voter_image.md5_signature)
        voter.data_hin = data_hin
        voter.save()
        voter_image.is_details_captured = True
        voter_image.save()
        voter.save()

        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        #cv2.imwrite(voter_image.image.parent +'/voter_id_{voter_image.id}.png',img_rgb)

