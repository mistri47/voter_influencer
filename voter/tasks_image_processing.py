from curses.textpad import rectangle
import os
import cv2
import numpy as np
import pytesseract
import pandas as pd
from googletrans import Translator
from textblob import TextBlob

from .models import *
from django.conf import settings



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


#
# Get text from any image and print
#

def read_voter_id(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        custom_config = r'-l eng --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        tb = TextBlob(txt)
        return format_txt(tb)
    except Exception as e:
        print(e)
        return None

def read_serial_id(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        custom_config = r'-l eng --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        tb = TextBlob(txt)
        return format_txt(tb)
    except Exception as e:
        print(e)
        return None


def image_to_text_hindi(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        custom_config = r'-l hin+eng --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        tb = TextBlob(txt)
        return format_txt(tb)
    except Exception as e:
        print(e)
        return None


def image_to_text_english(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        custom_config = r'-l eng+hin --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        # tb = TextBlob(txt)
        try:
            translator = None
            try:
                translator = Translator(service_urls=["translate.google.com", "translate.google.co.uk"])
            except Exception as e:
                translator = Translator()

            translator.raise_Exception = True
            translated = translator.translate(txt, src='hi', dest='en')
            return format_txt(translated.text)
        except Exception as e:
            print(e)
            return format_txt(txt)

        
    except Exception as e:
        print(e)
        return None





def fetch_voter_box(image_to_be_processed):
        print("Output stored in Output directiory!")
        image_dir = settings.MEDIA_ROOT + '/booth/images/'+ str(image_to_be_processed.station.id) + "/" + str(image_to_be_processed.id) + "/cropped/"

        try:
            os.stat(image_dir)
        except:
            os.makedirs(image_dir)
            
        idx = 0
        VoterImage.objects.filter(station_image=image_to_be_processed).delete()

        contours = box_extraction(image_to_be_processed.image)
        if contours:
            for c in contours:

                # Returns the location and width,height for every contour
                x, y, w, h = cv2.boundingRect(c)

                img = cv2.imread(image_to_be_processed.image.path, 0)  # Read the image
                rectangle_dia = f"w: {w}, h: {h}"
                if (w > 1150 and w < 1250 and h > 450 and h < 500):
                    with_squres_img = cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 5)
                    cv2.putText(with_squres_img, rectangle_dia, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)


                # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
                if (w > 1150 and w < 1250 and h > 450 and h < 500):
                    idx += 1
                    new_img = img[y:y+h, x:x+w]
                    image_path = image_dir + str(idx) + '.png'
                    image_url = 'booth/images/'+ str(image_to_be_processed.station.id) + "/" + str(image_to_be_processed.id) + "/cropped/" + str(idx) + '.png'

                    cv2.imwrite(image_path, new_img)

                else:
                    pass
                    # print("ERROR: Image not in desired sizee")
                    # print(rectangle_dia)
            return True
        else:
            return None


def process_voter_list_page():

    # list of non-processed booths
    print("Processing Images to extract details. First we delete all old voters and then extract each page images.")

    booths = PollingStation.objects.filter(
        images_created=True,
        is_processed=False
    )

    for booth in booths:
        polling_stations_images = PollingStationImage.objects.filter(
            station=booth,
            is_processed=False
        ).order_by('page_number')

        for polling_stations_image in polling_stations_images:
            print(polling_stations_image)
            Voter.objects.filter(polling_station_image=polling_stations_image).delete()
            #img = cv2.imread(polling_stations_image.image.path)
            
            success = fetch_voter_box(polling_stations_image)
            if success:
                polling_stations_image.is_processed = True
                polling_stations_image.save()





def process_voter_detail_image():

    # Update blank voter_id
    for voter in Voter.objects.filter(voter_id=None)[:100]:
        #id_cropped = crop_img[0:0+27, 350:350+140]  # Cropping Voter ID
        #
        # !!!! HERE WE ARE ASSUMING THAT BOXES INSIDE MAIN BOX ARE IN SAME LOCATION.
        #
        voter_image = voter.voter_image
        voter_detailed_boxes = box_extraction(voter_image.image)
        if voter_detailed_boxes:
            for box in voter_detailed_boxes:
                x, y, w, h = cv2.boundingRect(box)

                img = cv2.imread(voter_image.image.path, 0)  # Read the image
                rectangle_dia = f"w: {w}, h: {h}"
                print(">>>>>>>>>> for Voter ID: "+rectangle_dia)
                with_squres_img = cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 5)
                cv2.putText(with_squres_img, rectangle_dia, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        
            cv2.imwrite("boxed_"+voter_image.image.path, with_squres_img)

        crop_img = cv2.imread(voter_image.image.path)
        id_cropped = crop_img[x:y, x + w:y + h]  # Cropping Voter ID
        voter_id = read_voter_id(id_cropped)
        print(voter_id)
        voter.voter_id = voter_id
        voter.save()



    for voter_image in VoterImage.objects.filter(is_processed=False, has_errors=False)[:100]:
        print(voter_image)
        voter_image.voters.all().delete()
        #
        # Below we are cropping and extracting from single voter detail image.
        #

        print(voter_image.image.path)
        crop_img = cv2.imread(voter_image.image.path)

        # if crop_img:

        #serial_cropped = crop_img[0:23, 8:104]  # Cropping Serial ID
        serial_cropped = crop_img[10:70, 30:260]  # Cropping Serial ID
        serial_id = read_serial_id(serial_cropped)
        print(serial_id)


        # photo_cropped = crop_img[100:485, 900:1250]  # Cropping Photo
        # image_to_text(photo_cropped)

        #data_cropped = crop_img[28:28+150, 0:0+350]
        data_cropped = crop_img[70:480, 10:900]  # Main Details
        data_hindi = image_to_text_hindi(data_cropped)
        #data_english = image_to_text_english(data_cropped)
        #print(data_english)
        print(data_hindi)


        try:
            voter = Voter(
                md5_signature=voter_image.md5_signature,
                voter_id=voter_id,
                serial_number=serial_id,
                #data_eng=data_english,
                data_hin=data_hindi,
                polling_booth = voter_image.station_image.station,
                voter_image = voter_image
            )
            voter.save()
            voter_image.is_processed = True
            voter_image.has_errors = False
            voter_image.save()
        except Exception as e:
            print(e)
            try:
                existing_voter = Voter.objects.get(md5_signature=voter_image.md5_signature)
                existing_voter.serial_number = serial_id
                #existing_voter.data_eng = data_english
                existing_voter.data_hin = data_hindi
                existing_voter.data_eng = None
                existing_voter.voter_image = voter_image
                existing_voter.save()
                voter_image.is_processed = True
                voter_image.has_errors = False
                voter_image.save()
            except Exception as e:
                print(e)
                voter_image.is_processed = True
                voter_image.has_errors = True
                voter_image.save()
