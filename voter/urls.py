from django.urls import include, path


from .views import *

urlpatterns = [
    path("", list_items, name="list_voters"),
]