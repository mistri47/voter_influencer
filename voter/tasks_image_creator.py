import os
import re
from .models import *
from pdf2image import convert_from_path
from django.conf import settings
import hashlib

def pdf_to_images():
    print("Creating images from voter list pdf.")
    image_dir = settings.MEDIA_ROOT + '/booth/images'
    try:
        os.stat(image_dir)
    except:
        os.makedirs(image_dir)

    booths = PollingBooth.objects.filter(images_created=False, voter_list__isnull=False)

    for booth in booths:

        PollingStationImage.objects.filter(station=booth).delete()
        image_file_dir = image_dir + "/" + str(booth.id)
        try:
            os.stat(image_file_dir)
        except:
            os.makedirs(image_file_dir)

        try:
            pages = convert_from_path(booth.voter_list.path, 500)


            for index, page in enumerate(pages):
                file_path = image_file_dir +"/page_%s.jpg" % (index)
                page.save(file_path, 'JPEG')
                print("Saved File: %s" % file_path)

                file_url = "booth/images/%s/page_%s.jpg" % (booth.id, index)
                print(file_url)

                page_type = VoterListPageTypes.VOTER_LIST.name
                if index == 1:
                    page_type = VoterListPageTypes.SUMMARY.name
                if index == 2:
                    page_type = VoterListPageTypes.MAP.name

                obj = PollingStationImage(
                    md5_signature=hashlib.md5(str(file_url).encode('utf-8')).hexdigest(),
                    station=booth,
                    type=page_type,
                    page_number=index,
                    image=file_url
                )
                obj.save()

            booth.images_created = True
            booth.save()
        except Exception as e:
            print(e)
