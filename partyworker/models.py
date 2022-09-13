from voter_influencer.users.models import User
from django.db import models
from django.db.models.deletion import RESTRICT
from enum import Enum

from voter.models import Caste
from django.conf import settings

# Create your models here.

class WorkerType(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.title

class PartyWorker(models.Model):
    user = models.OneToOneField(User, on_delete=RESTRICT)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=settings.GENDERS, null=True, blank=True)
    worker_type = models.ForeignKey(WorkerType, related_name='workers', on_delete=RESTRICT)
    caste = models.ForeignKey(Caste, related_name='workers', on_delete=RESTRICT)
    category = models.CharField(max_length=20, choices=settings.CATEGORIES, null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    photo = models.FileField(null=True, blank=True)
    points = models.IntegerField(default=0)
    address = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username