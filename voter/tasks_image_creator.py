import os
import re
from .models import *
from pdf2image import convert_from_path
from django.conf import settings


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

        pages = convert_from_path(booth.voter_list.path)

        # convert_from_path(
        #     pdf_path,
        #     dpi=200,
        #     output_folder=None,
        #     first_page=None,
        #     last_page=None,
        #     fmt="ppm",
        #     jpegopt=None,
        #     thread_count=1,
        #     userpw=None,
        #     use_cropbox=False,
        #     strict=False,
        #     transparent=False,
        #     single_file=False,
        #     output_file=uuid_generator(),
        #     poppler_path=None,
        #     grayscale=False,
        #     size=None,
        #     paths_only=False,
        #     hide_annotations=False,
        # )



        for index, page in enumerate(pages):
            file_path = image_file_dir + "/out%s.jpg" % index
            page.save(file_path, 'JPEG')
            print("Saved File: %s" % file_path)

            file_url = 'booth/images' + "/out%s.jpg" % index

            page_type = VoterListPageTypes.VOTER_LIST.name
            if index == 1:
                page_type = VoterListPageTypes.SUMMARY.name
            if index == 2:
                page_type = VoterListPageTypes.MAP.name

            obj = PollingStationImage(station=booth, type=page_type, page_number=index,
                                      image=file_url)
            obj.save()

        booth.images_created = True
        booth.save()
