import re
from .models import *

from googletrans import Translator
from textblob import TextBlob


def get_local_translation(txt):
    replace_dict = {
        "निर्वाचक का नाम":"Voter Name",
        "पिता का नाम":"Father Name",
        "पति का नाम":"Husband Name",
        "गृह संख्या":"House Number",
        "आयु":"Age",
        "लिंग":"\nGender",
        "पुरुष":"MALE",
        "महिला":"FEMALE",
    }

    for key,value in replace_dict.items():
        txt = txt.replace(key, value, 1)
    
    return txt


def update_english_data():
    no_english_data_voters = Voter.objects.filter(
        data_eng=None
    )[:100]

    for voter in no_english_data_voters:
        txt = voter.data_hin
        eng_txt = get_local_translation(txt)
                     
        voter.data_eng = eng_txt
        
        txt_array = eng_txt.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))

            if index==0: # Voter name line
                value = line.split(":")[1].strip()
                print("Voter Name: %s" % value)
                voter.full_name = value  

            if index==1: # Father/Husband name line
                if line.startswith("Husband"):
                    value = line.split(":")[1].strip()
                    print("Husband: %s" % value)
                    voter.husband_name = value
                else:
                    value = line.split(":")[1].strip()
                    print("Father: %s" % value)
                    voter.father_name = value

            if index==2: # House Number line
                value = line.split(":")[1].strip()
                print("House: %s" % str(value))
                voter.house_number = value

            if index==3: # Age name line
                try:
                    value = line.split(":")[1].strip()
                    print("Age: %s" % int(value))
                    voter.age = value
                except:
                    voter.age = -1
                    print(voter)
                    voter.has_errors = True


            if index==4: # Gender name line
                value = line.split(":")[1].strip()
                print("Gender Name: %s" % value)
                voter.gender = value

        voter.save()



def update_gender():

    # Extract Gender
    no_gender_voters = Voter.objects.filter(
        gender=None,
        data_eng__isnull=False
    )[:10]

    for voter in no_gender_voters:
                     
        txt_array = voter.data_eng.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))

            if index==4: # Gender name line
                value = line.split(":")[1].strip()
                print("Gender Name: %s" % value)
                voter.gender = value

        voter.save()

    update_husband_name()


def update_age():
    # Extract AGE
    no_age_voters = Voter.objects.filter(
        age=None,
        data_eng__isnull=False
    )[:100]

    for voter in no_age_voters:
        txt_array = voter.data_eng.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))
            if index==3: # Age name line
                try:
                    value = line.split(":")[1].strip()
                    print("Age: %s" % int(value))
                    voter.age = value
                except:
                    voter.age = -1
                    print(voter)
                    voter.has_errors = True


        voter.save()



def update_house_number():
    # Extract House Number
    no_hn_voters = Voter.objects.filter(
        house_number=None,
        data_eng__isnull=False
    )[:100]

    for voter in no_hn_voters:
        txt_array = voter.data_eng.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))
            if index==2: # House Number line
                value = line.split(":")[1].strip()
                print("House: %s" % value)
                voter.house_number = value

        voter.save()



def update_name():
    # Extract Name
    no_fn_voters = Voter.objects.filter(
        full_name=None,
        data_eng__isnull=False
    )[:100]

    for voter in no_fn_voters:
        txt_array = voter.data_eng.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))
            if index==0: # Voter name line
                try:
                    value = line.split(":")[1].strip()
                    print("Voter Name: %s" % value)
                    voter.full_name = value  
                except:
                    print(voter)
                    voter.has_errors = True
                    

        voter.save()



def update_father_husband_name():
    # Extract Father Name
    no_father_n_voters = Voter.objects.filter(
        father_name=None,
        husband_name=None,
        data_eng__isnull=False
    )[:100]

    for voter in no_father_n_voters:
        txt_array = voter.data_eng.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))

            if index==1: # Father/Husband name line
                if line.startswith("Husband"):
                    value = line.split(":")[1].strip()
                    print("Husband: %s" % value)
                    voter.husband_name = value
                else:
                    value = line.split(":")[1].strip()
                    print("Father: %s" % value)
                    voter.father_name = value

        voter.save()



def update_husband_name():
    # Extract Husband name
    no_husband_n_voters = Voter.objects.filter(
        husband_name=None,
        gender='FEMALE',
        data_eng__isnull=False
    )[:100]

    for voter in no_husband_n_voters:
        txt_array = voter.data_eng.strip().split("\n")

        for index,line in enumerate(txt_array):
            line = line.strip()
            # print("Line %s : %s " % (index, line))
            if index==1: # Father/Husband name line
                if line.startswith("Husband"):
                    value = line.split(":")[1].strip()
                    print("Husband: %s" % value)
                    voter.husband_name = value
                else:
                    pass

        voter.save()

