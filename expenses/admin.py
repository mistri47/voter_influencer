from statistics import mode
from django.contrib import admin

# Register your models here.

from .models import *


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vikaskhand', 'panchayat', 'village_name', 'workd_details', 'amount', 'department', 'financial_year')
    list_filter = ('financial_year', 'vikaskhand')

admin.site.register(Expense, ExpenseAdmin)
