import re
from .models import *


def update_gender():

    # Extract Gender
    no_gender_voters = Voter.objects.filter(
        gender=None
    )

    for voter in no_gender_voters:
        try:
            gender = re.findall(r'Gender: (\w+)', voter.data_eng)[0].upper()
            if gender == 'WOMEN':
                gender = 'FEMALE'
            voter.gender = gender
            voter.save()
        except Exception as e:
            print(e)
            print("Gender not parsed.")

    update_husband_name()


def update_age():
    # Extract AGE
    no_age_voters = Voter.objects.filter(
        age=None
    )

    for voter in no_age_voters:
        try:
            age = int(re.findall(r'[Age][Sex]: (\w+)', voter.data_eng)[0])
            if age < 100:
                voter.age = age
                voter.save()
        except Exception as e:
            try:
                age = int(re.findall(r'Sex: (\w+)', voter.data_eng)[0])
                if age < 100:
                    voter.age = age
                    voter.save()
            except:
                print(e)
                print("Age not parsed.")


def update_house_number():
    # Extract House Number
    no_hn_voters = Voter.objects.filter(
        house_number=None
    )

    for voter in no_hn_voters:
        try:
            house_number = int(re.findall(r'Home Number: (\w+)', voter.data_eng)[0])
            voter.house_number = house_number
            voter.save()
        except Exception as e:
            print(e)
            print("House_number not parsed.")


def update_name():
    # Extract Name
    no_fn_voters = Voter.objects.filter(
        full_name=None
    )

    for voter in no_fn_voters:
        try:
            full_name = re.findall(r'Name of Elector: (\w+)', voter.data_eng)[0]
            voter.full_name = full_name
            voter.save()
        except Exception as e:
            print(e)
            print("full_name not parsed.")


def update_father_name():
    # Extract Father Name
    no_father_n_voters = Voter.objects.filter(
        father_name=None,
        husband_name=None
    )

    for voter in no_father_n_voters:
        try:
            father_name = re.findall(r'Father\'s name: (\w+)', voter.data_eng)[0]
            voter.father_name = father_name
            voter.save()
        except Exception as e:
            print(e)
            print("father_name not parsed.")


def update_husband_name():
    # Extract Husband name
    no_husband_n_voters = Voter.objects.filter(
        husband_name=None,
        gender='FEMALE'
    )

    for voter in no_husband_n_voters:
        try:
            husband_name = re.findall(r'Husband\'s name : (\w+)', voter.data_eng)[0]
            voter.husband_name = husband_name
            voter.save()
        except Exception as e:
            print(e)
            print("husband_name not parsed.")
