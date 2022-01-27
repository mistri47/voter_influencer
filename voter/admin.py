from django.contrib import admin

# Register your models here.
from .models import *


class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'serial_number', 'full_name', 'age', 'gender',
        'father_name', 'husband_name', 'house_number', 'data_eng', 'data_hin')
    list_filter = ('gender',)
    search_fields = ['voter_id', 'full_name', 'serial_number']


admin.site.register(Voter, VoterAdmin)

admin.site.register(PollingBooth)
admin.site.register(PollingAgent)
admin.site.register(PollingStationImage)


class VoterImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image', 'station_image', 'is_processed', 'has_errors'
    )
    list_filter = ('is_processed', 'has_errors')
admin.site.register(VoterImage, VoterImageAdmin)
