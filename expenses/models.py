from unicodedata import name
from django.db import models

# Create your models here.

class Expense(models.Model):
    vikaskhand = models.CharField(max_length=100)
    panchayat = models.CharField(max_length=100)
    village_name = models.CharField(max_length=100)
    workd_details = models.TextField()
    amount = models.BigIntegerField(default=0)
    department = models.CharField(max_length=100)
    financial_year = models.SmallIntegerField(default=2000)

    def __str__(self) -> str:
        return f"{self.vikaskhand} : {self.panchayat} : {self.workd_details}"

    class Meta:
        ordering = ('vikaskhand', 'panchayat', 'financial_year')