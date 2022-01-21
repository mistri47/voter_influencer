import os
import cv2
import numpy as np
import pytesseract
import pandas as pd
import googletrans
from googletrans import Translator

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
def image_to_text_hindi(img):
    try:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        custom_config = r'-l hin --psm 6'
        txt = pytesseract.image_to_string(rgb, config=custom_config)
        return format_txt(txt)
    except Exception as e:
        print(e)
        return None


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
        image_dir = settings.MEDIA_ROOT + '/booth/images/'+ str(polling_stations_image.station.id) + "/cropped/"

        try:
            os.stat(image_dir)
        except:
            os.makedirs(image_dir)
            
        idx = 0
        for c in contours:
            #print(c)
            # Returns the location and width,height for every contour
            x, y, w, h = cv2.boundingRect(c)

            # If the box height is greater then 20, widht is >80, then only save it as a box in "cropped/" folder.
            if (w > 1000 and h > 300 and w < 2000 and h < 1000):
                idx += 1
                new_img = img[y:y+h, x:x+w]
                image_path = image_dir + str(idx) + '.png'

                cv2.imwrite(image_path, new_img)
                voter_image = VoterImage(station_image=polling_stations_image, image=image_path)
                voter_image.save()
            else:
                pass
                # print("x %s, y %s, w %s, h %s " % (x,y,w,h))

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

            for voter_image in VoterImage.objects.filter(station_image=polling_stations_image):
                #
                # Below we are cropping and extracting from single voter detail image.
                #

                crop_img = cv2.imread(voter_image.image.path)

                if crop_img:

                    serial_cropped = crop_img[10:70, 30:260]  # Cropping Serial ID
                    serial_id = image_to_text_english(serial_cropped)

                    id_cropped = crop_img[10:85, 800:1230]  # Cropping Voter ID
                    voter_id = image_to_text_english(id_cropped)

                    # photo_cropped = crop_img[100:485, 900:1250]  # Cropping Photo
                    # image_to_text(photo_cropped)

                    data_cropped = crop_img[82:480, 10:900]  # Cropping Photo
                    data_hindi = image_to_text_hindi(data_cropped)
                    data_english = image_to_text_english(data_cropped)

                    try:
                        # write_to_csv([serial_id, voter_id, data_english, data_hindi])
                        try:
                            existing_voter = Voter.objects.get(voter_id=voter_id)
                            existing_voter.serial_number = serial_id
                            existing_voter.data_eng = data_english
                            existing_voter.data_hin = data_hindi
                            existing_voter.polling_station_image = polling_stations_image
                            existing_voter.save()
                        except Exception as e:
                            print(e)
                            try:
                                voter = Voter(
                                    voter_id=voter_id,
                                    serial_number=serial_id,
                                    data_eng=data_english,
                                    data_hin=data_hindi,
                                    polling_booth=booth,
                                    polling_station_image=polling_stations_image
                                )
                                voter.save()
                            except Exception as e:
                                print(e)

                    except Exception as e:
                        print(e)
                        print("Error in saving record")
                        print(voter_id)
                        print(data_english)

            polling_stations_image.is_processed = True
            polling_stations_image.save()





        # for image in images:
        #     Voter.objects.filter(polling_station_image=image).delete()
        #     img = cv2.imread(image.image.path)
        #     x = 170
        #     y = 282

        #     w = 1260
        #     h = 488

        #     for j in range(0, 10):
        #         for i in range(1, 4):
        #             # print("Coordinates: %s:%sx%s:%s" % (x, y, x+w, y+h))
        #             crop_img = img[y:y+h, x:x+w]
        #             x = x+w

        #             serial_cropped = crop_img[10:70, 30:260]  # Cropping Serial ID
        #             serial_id = image_to_text_english(serial_cropped)

        #             id_cropped = crop_img[10:85, 800:1230]  # Cropping Voter ID
        #             voter_id = image_to_text_english(id_cropped)

        #             # photo_cropped = crop_img[100:485, 900:1250]  # Cropping Photo
        #             # image_to_text(photo_cropped)

        #             data_cropped = crop_img[82:480, 10:900]  # Cropping Photo
        #             data_hindi = image_to_text_hindi(data_cropped)
        #             data_english = image_to_text_english(data_cropped)

        #             try:
        #                 # write_to_csv([serial_id, voter_id, data_english, data_hindi])
        #                 try:
        #                     existing_voter = Voter.objects.get(voter_id=voter_id)
        #                     existing_voter.serial_number = serial_id
        #                     existing_voter.data_eng = data_english
        #                     existing_voter.data_hin = data_hindi
        #                     existing_voter.polling_station_image = image
        #                     existing_voter.save()
        #                 except Exception as e:
        #                     print(e)
        #                     try:
        #                         voter = Voter(
        #                             voter_id=voter_id,
        #                             serial_number=serial_id,
        #                             data_eng=data_english,
        #                             data_hin=data_hindi,
        #                             polling_booth=booth,
        #                             polling_station_image=image
        #                         )
        #                         voter.save()
        #                     except Exception as e:
        #                         print(e)

        #             except Exception as e:
        #                 print(e)
        #                 print("Error in saving record")
        #                 print(voter_id)
        #                 print(data_english)

        #         y = y+h
        #         x = 170
        #     image.is_processed = True
        #     image.save()

#header = ['serial_id', 'voter_id', 'data_english', 'data_hindi']

# cv2.imshow("cropped", img)

# ! Coordinates for ID: 10:70, 30:270
# ! Coordinates for VoterID: 10:85, 800:1250
# ! Coordinates for Photo: 100:485, 900:1250
