from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from enum import Enum

from voter_influencer.users.models import User
# Create your models here.


class PollingBooth(models.Model):
    name = models.CharField(max_length=100)
    number = models.SmallIntegerField()
    address = models.TextField(null=True, blank=True)
    voter_list = models.FileField(null=True, blank=True)
    images_created = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class VoterListPageTypes(Enum):
    VOTER_LIST = 'VOTER_LIST'
    SUMMARY = 'SUMMARY'
    MAP = 'MAP'


class PollingStationImage(models.Model):
    station = models.ForeignKey(PollingBooth, related_name='images', on_delete=CASCADE)
    type = models.CharField(max_length=20, default=VoterListPageTypes.VOTER_LIST.name)
    image = models.FileField(null=True, blank=True)
    page_number = models.SmallIntegerField()
    is_processed = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)
    md5_signature = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.image.url



class VoterImage(models.Model):
    station_image = models.ForeignKey(PollingStationImage, related_name='voter_images', on_delete=CASCADE)
    image = models.FileField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.image.url



GENDERS = (
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('OTHER', 'OTHER')
)

CATEGORIES = (
    ('GENERAL', 'GENERAL'),
    ('OBC', 'OBC'),
    ('SC', 'SC'),
    ('ST', 'ST')
)


class PollingAgent(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    polling_booth = models.ForeignKey(PollingBooth, related_name='agents', on_delete=CASCADE)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    points = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username


class Voter(models.Model):
    voter_id = models.CharField(max_length=20, primary_key=True)  # Primary Key, Unique
    serial_number = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    husband_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDERS, null=True, blank=True)
    house_number = models.CharField(max_length=20, null=True, blank=True)

    category = models.CharField(max_length=20, choices=CATEGORIES, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    data_eng = models.TextField(null=True, blank=True)
    data_hin = models.TextField(null=True, blank=True)

    polling_booth = models.ForeignKey(PollingBooth, related_name='voters', on_delete=CASCADE)
    polling_station_image = models.ForeignKey(
        PollingStationImage, related_name='voters', on_delete=CASCADE, null=True, blank=True)
    voter_image = models.ForeignKey(
    VoterImage, related_name='voters', on_delete=CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.voter_id
