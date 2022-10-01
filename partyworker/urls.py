from django.urls import include, path


from .views import *

urlpatterns = [
    path("",                    list_items,         name="list_workers"),
    path("add/",                add_item,           name="add_worker"),
    path("update/<int:id>/",    update_item,        name="update_worker"),

]