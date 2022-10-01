from django.urls import include, path


from .views import *

urlpatterns = [
    path("", list_items, name="list_expenses"),
    path("add/", add, name="add_expense"),
    path("details/<int:id>", details, name="details_expense"),
    path("update/<int:id>", update, name="update_expense"),
    path("delete/<int:id>", delete, name="delete_expense"),

]