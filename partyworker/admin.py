from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(WorkerType)


class PartyWorkerAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'mobile', 'worker_type', 'caste', 'category', 'points')
    list_filter = ('worker_type', 'category')
    search_fields = ['user__username', 'full_name', 'mobile']
admin.site.register(PartyWorker, PartyWorkerAdmin)