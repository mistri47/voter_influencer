import re
from .models import *
from config.celery_app import app
from .tasks_voter_info import update_husband_name, update_father_husband_name, update_name, update_house_number, update_age, update_gender, update_english_data
from .tasks_image_creator import pdf_to_images
from .tasks_image_processing import process_voter_list_page, process_voter_detail_image


# This task reads additional information from the voter image and updates.
@app.task(bind=True)
def voter_info_update(self):
    update_english_data()

@app.task(bind=True)
def update_gender_task(self):
    update_gender()


@app.task(bind=True)
def update_age_task(self):
    update_age()

@app.task(bind=True)
def update_house_number_task(self):
    update_house_number()

@app.task(bind=True)
def update_name_task(self):
    update_name()

@app.task(bind=True)
def update_father_husband_name_task(self):
    update_father_husband_name()


# This task will create images for each page from the PDF file.
@app.task(bind=True)
def pdf_to_images_task(self):
    pdf_to_images()


# This task will process each page image and break it into each voter image.
@app.task(bind=True)
def process_voter_list_page_task(self):
    process_voter_list_page()


# This task reads each voter detail image and extracts voter information.
@app.task(bind=True)
def process_voter_detail_image_task(self):
    process_voter_detail_image()
