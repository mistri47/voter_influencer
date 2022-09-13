from django.contrib import admin

# Register your models here.
from .models import PollingStation, PollingStationImage

class PollingStationAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'images_created', 'is_processed', 'has_errors', 'total_voters', 'male_voters', 'female_voters', 'other_voters')
    list_filter = ('is_processed','has_errors')
    search_fields = ['name', 'number']

admin.site.register(PollingStation, PollingStationAdmin)




class PollingStationImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'image', 'boxed_image_url', 'is_previewd', 'is_processed', 'has_errors'
    )
    list_filter = ('is_processed', 'has_errors')
admin.site.register(PollingStationImage, PollingStationImageAdmin)
