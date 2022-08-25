from django.contrib import admin

# Register your models here.
from .models import *

from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp
admin.site.unregister(SocialToken)
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)

class VoterAdmin(admin.ModelAdmin):
    list_display = ('md5_signature', 'serial_number', 'voter_id', 'full_name', 'age', 'gender',
        'father_name', 'husband_name', 'house_number', 'caste', 'category', 'data_eng', 'data_hin')
    list_filter = ('gender', 'caste', 'category')
    search_fields = ['voter_id', 'full_name', 'serial_number', 'md5_signature']


admin.site.register(Voter, VoterAdmin)

class PollingBoothAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'images_created', 'is_processed', 'has_errors')
    list_filter = ('is_processed','has_errors')
    search_fields = ['name', 'number']

admin.site.register(PollingBooth, PollingBoothAdmin)

class CasteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'related_surnames')
admin.site.register(Caste, CasteAdmin)

admin.site.register(AgentType)

class PollingAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'mobile', 'agent_type', 'caste', 'category', 'polling_booth', 'points')
    list_filter = ('agent_type', 'category')
    search_fields = ['user__username', 'full_name', 'mobile']
admin.site.register(PollingAgent, PollingAgentAdmin)


class PollingStationImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image', 'boxed_image_url', 'is_previewd', 'is_processed', 'has_errors'
    )
    list_filter = ('is_processed', 'has_errors')
admin.site.register(PollingStationImage, PollingStationImageAdmin)


class VoterImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image_url', 'station_image', 'is_voter_id_captured', 'is_details_captured', 'is_processed', 'has_errors'
    )
    list_filter = ('is_processed', 'has_errors', 'is_voter_id_captured', 'is_details_captured')
admin.site.register(VoterImage, VoterImageAdmin)
