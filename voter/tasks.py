import re
from .models import *
from config.celery_app import app
from .tasks_voter_info import update_husband_name, update_father_name, update_name, update_house_number, update_age, update_gender
from .tasks_image_creator import pdf_to_images
from .tasks_image_processing import process_voter_list_page


@app.task(bind=True)
def voter_info_update(self):
    update_gender()
    update_age()
    update_house_number()
    update_name()
    update_father_name()
    # update_husband_name() - Husband name called from inside of gender


@app.task(bind=True)
def pdf_to_images_task(self):
    pdf_to_images()


@app.task(bind=True)
def process_voter_list_page_task(self):
    process_voter_list_page()
