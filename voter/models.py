from django.db import models
from django.db.models.deletion import RESTRICT
from django.db.models.fields import CharField
from enum import Enum
from django.conf import settings

from voter_influencer.users.models import User
# Create your models here.
from polling_station.models import PollingStationImage, PollingStation



class VoterImage(models.Model):
    polling_station = models.ForeignKey(PollingStation, related_name='voter_images', on_delete=RESTRICT)
    station_image = models.ForeignKey(PollingStationImage, related_name='voter_images', on_delete=RESTRICT)
    image = models.FileField(null=True, blank=True)
    image_url = models.FileField(null=True, blank=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    is_cropped = models.BooleanField(default=False)
    is_voter_id_captured = models.BooleanField(default=False)
    is_photo_captured = models.BooleanField(default=False)
    is_serial_captured = models.BooleanField(default=False)
    is_details_captured = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)
    md5_signature = models.CharField(max_length=1000, unique=True)
    
    def __str__(self) -> str:
        return self.image.url



class Caste(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=settings.CATEGORIES)
    related_surnames = models.TextField()

    def __str__(self) -> str:
        return self.title + " - " + self.category




class Voter(models.Model):
    md5_signature = models.CharField(max_length=1000, unique=True)
    voter_id = models.CharField(max_length=20, null=True, blank=True)  # Primary Key, Unique
    serial_number = models.IntegerField(null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    father_name = models.CharField(max_length=100, null=True, blank=True)
    husband_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.SmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=settings.GENDERS, null=True, blank=True)
    house_number = models.CharField(max_length=20, null=True, blank=True)
    caste = models.ForeignKey(Caste, related_name='voters', on_delete=RESTRICT, null=True, blank=True)
    category = models.CharField(max_length=20, choices=settings.CATEGORIES, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)

    data_eng = models.TextField(null=True, blank=True)
    data_hin = models.TextField(null=True, blank=True)

    polling_booth = models.ForeignKey(PollingStation, related_name='voters', on_delete=RESTRICT)
    polling_station_image = models.ForeignKey(
        PollingStationImage, related_name='voters', on_delete=RESTRICT)
    voter_image = models.ForeignKey(VoterImage, related_name='voters', on_delete=RESTRICT)

    class Meta:
        ordering = ('polling_booth', 'house_number',)

    def __str__(self) -> str:
        return self.md5_signature
