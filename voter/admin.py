from django.contrib import admin

# Register your models here.
from .models import *


class VoterAdmin(admin.ModelAdmin):
    list_display = ('voter_id', 'serial_number', 'full_name', 'age', 'gender',
                    'father_name', 'husband_name', 'house_number', 'data_eng', 'data_hin')


admin.site.register(Voter, VoterAdmin)

admin.site.register(PollingBooth)
admin.site.register(PollingAgent)
admin.site.register(PollingStationImage)
admin.site.register(VoterImage)
