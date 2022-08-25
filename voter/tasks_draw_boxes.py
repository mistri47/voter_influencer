import os
from enum import unique
import cv2
from .utils import box_extraction
import hashlib
from .models import PollingStationImage, VoterImage
from django.conf import settings

def draw_boxes_around_voter_details():
    print("Drawing boxes around voter details")

    voting_list_pages = PollingStationImage.objects.filter(is_previewd=False)[:10]
    
    for voting_list_page in voting_list_pages:
        image_path = voting_list_page.image.path
        contours = box_extraction(image_path)
        if contours:
            boxed_img = cv2.imread(image_path)  # Read the image
                
            for c in contours:

                # Returns the location and width,height for every contour
                x, y, w, h = cv2.boundingRect(c)

                rectangle_dia = f"w: {w}, h: {h}"
                if (w > 1150 and w < 1300 and h > 450 and h < 500):
                    print(rectangle_dia)
                    boxed_img = cv2.rectangle(boxed_img, (x, y), (x + w, y + h), (12,255,36), 2)
                    # cv2.putText(
                    #     boxed_img,
                    #     rectangle_dia, 
                    #     (x, y-10), 
                    #     cv2.FONT_HERSHEY_SIMPLEX,
                    #     2, 
                    #     (12,255,36),
                    #     2
                    # )
                    cropped_dir = settings.MEDIA_ROOT + f"/booth/images/{voting_list_page.station.id}/{voting_list_page.id}/cropped/"
                    try:
                        os.stat(cropped_dir)
                    except Exception as e:
                        os.makedirs(cropped_dir)

                    image_url = f"/booth/images/{voting_list_page.station.id}/{voting_list_page.id}/cropped/"
                    voter_image_path = cropped_dir + f"/{x}_{y}_{w}_{h}.png"
                    unique_hash=hashlib.md5(str(voter_image_path).encode('utf-8')).hexdigest()

                    try:
                        voter_image = VoterImage(
                            md5_signature=unique_hash,
                            station_image=voting_list_page,
                            image=voter_image_path,
                            image_url=image_url+f"/{x}_{y}_{w}_{h}.png",
                            x=x,
                            y=y,
                            w=w,
                            h=h
                        )
                        voter_image.save()
                    except Exception as e:
                        pass # Here need the logic to update info for voter image.

            boxed_image_url = f"/booth/images/{voting_list_page.station.id}/page_{voting_list_page.page_number}_boxed_{voting_list_page.id}"
            squre_image_path = settings.MEDIA_ROOT + f"{boxed_image_url}.png"
            cv2.imwrite(squre_image_path, boxed_img)
            voting_list_page.boxed_image=squre_image_path
            voting_list_page.boxed_image_url=boxed_image_url+".png"
            
        voting_list_page.is_previewd = True
        voting_list_page.save()


def crop_voter_details_images():
    voter_list_images = PollingStationImage.objects.filter(is_previewd=True, is_processed=False)[:10]

    for voter_list_image in voter_list_images:
        org_img = cv2.imread(voter_list_image.image.path)  # Read the image
            
        for voter_image in voter_list_image.voter_images.all():     
            print(voter_image.image.path)       
            voter_image_data = org_img[voter_image.y:voter_image.y+voter_image.h, voter_image.x:voter_image.x+voter_image.w]
            cv2.imwrite(voter_image.image.path, voter_image_data)
            voter_image.is_cropped = True
            voter_image.save()

        voter_list_image.is_processed = True
        voter_list_image.save()            
