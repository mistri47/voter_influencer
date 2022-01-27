import os
import cv2
import numpy as np
import pytesseract
import pandas as pd
from googletrans import Translator
from textblob import TextBlob

from .models import *
from django.conf import settings


def sort_contours(cnts, method="left-to-right"):
    # initialize the reverse flag and sort index
    reverse = False
    i = 0

    # handle if we need to sort in reverse
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True

    # handle if we are sorting against the y-coordinate rather than
    # the x-coordinate of the bounding box
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1

    # construct the list of bounding boxes and sort them from top to
    # bottom
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))

    # return the list of sorted contours and bounding boxes
    return (cnts, boundingBoxes)


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


#Functon for extracting the box
def box_extraction(polling_stations_image):

    print("Reading image..")
    img = cv2.imread(polling_stations_image.image.path, 0)  # Read the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image

    if img_bin.any():
        img_bin = 255 - img_bin  # Invert the image

        # print("Storing binary image to Images/Image_bin.jpg..")
        # cv2.imwrite("Images/Image_bin.jpg",img_bin)

        # print("Applying Morphological Operations..")
        # Defining a kernel length
        kernel_length = np.array(img).shape[1]//40
        
        # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
        verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
        # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
        hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
        # A kernel of (3 X 3) ones.
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        # Morphological operation to detect verticle lines from an image
        img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
        verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
        # cv2.imwrite("Images/verticle_lines.jpg",verticle_lines_img)

        # Morphological operation to detect horizontal lines from an image
        img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
        horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
        # cv2.imwrite("Images/horizontal_lines.jpg",horizontal_lines_img)

        # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
        alpha = 0.5
        beta = 1.0 - alpha
        # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
        img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
        img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
        (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # For Debugging
        # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
        # print("Binary image which only contains boxes: Images/img_final_bin.jpg")
        # cv2.imwrite("Images/img_final_bin.jpg",img_final_bin)
        # Find contours for image, which will detect all the boxes
        contours, hierarchy = cv2.findContours(
            img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Sort all the contours by top to bottom.
        (contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")

        print("Output stored in Output directiory!")
        image_dir = settings.MEDIA_ROOT + '/booth/images/'+ str(polling_stations_image.station.id) + "/" + str(polling_stations_image.id) + "/cropped/"

        try:
            os.stat(image_dir)
        except:
            os.makedirs(image_dir)
            
        idx = 0
        VoterImage.objects.filter(station_image=polling_stations_image).delete()

        for c in contours:
            # Returns the location and width,height for every contour
            x, y, w, h = cv2.boundingRect(c)

            # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
            if (w > 1240 and h > 470 and w < 1300 and h < 500):
                print(c)
                idx += 1
                new_img = img[y:y+h, x:x+w]
                image_path = image_dir + str(idx) + '.png'
                image_url = 'booth/images/'+ str(polling_stations_image.station.id) + "/" + str(polling_stations_image.id) + "/cropped/" + str(idx) + '.png'

                cv2.imwrite(image_path, new_img)
                voter_image = VoterImage(station_image=polling_stations_image, image=image_url)
                voter_image.save()
            else:
                print("ERROR: Image not in desired sizee")
                print("x %s, y %s, w %s, h %s " % (x,y,w,h))

        # For Debugging
        # Enable this line to see all contours.
        # cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
        # cv2.imwrite("./Temp/img_contour.jpg", img)
    else:
        print("ERROR: Image not extracted correctly")

def process_voter_list_page():

    # list of non-processed booths
    print("Processing Images to extract details. First we delete all old voters and then extract each page images.")

    booths = PollingBooth.objects.filter(
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
            
            box_extraction(polling_stations_image)
            polling_stations_image.is_processed = True
            polling_stations_image.save()





def process_voter_detail_image():

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

        #id_cropped = crop_img[0:0+27, 350:350+140]  # Cropping Voter ID
        id_cropped = crop_img[10:85, 800:1230]  # Cropping Voter ID
        voter_id = read_voter_id(id_cropped)
        print(voter_id)

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
            try:
                existing_voter = Voter.objects.get(voter_id=voter_id)
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
