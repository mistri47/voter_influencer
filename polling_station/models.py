from django.db import models
from django.db.models.deletion import RESTRICT
from enum import Enum

# Create your models here.

class VoterListPageTypes(Enum):
    VOTER_LIST = 'VOTER_LIST'
    SUMMARY = 'SUMMARY'
    MAP = 'MAP'

    
class PollingStation(models.Model):
    name = models.CharField(max_length=100)
    number = models.SmallIntegerField()
    address = models.TextField(null=True, blank=True)
    voter_list = models.FileField(null=True, blank=True)
    images_created = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)

    total_voters = models.SmallIntegerField(default=0)
    male_voters = models.SmallIntegerField(default=0)
    female_voters = models.SmallIntegerField(default=0)
    other_voters = models.SmallIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.number) + "-"+ self.name
    
    class Meta:
        ordering = ['number']


class PollingStationImage(models.Model):
    station = models.ForeignKey(PollingStation, related_name='images', on_delete=RESTRICT)
    type = models.CharField(max_length=20, default=VoterListPageTypes.VOTER_LIST.name)
    image = models.FileField(null=True, blank=True)
    boxed_image = models.FileField(null=True, blank=True)
    boxed_image_url = models.FileField(null=True, blank=True)
    page_number = models.SmallIntegerField()
    is_previewd = models.BooleanField(default=False)
    is_processed = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)
    md5_signature = models.CharField(max_length=1000, unique=True)

    def __str__(self) -> str:
        return self.image.url

