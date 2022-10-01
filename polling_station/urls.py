from django.urls import include, path


from .views import *

urlpatterns = [

    path("",                    list_items, name="list_polling_stations"),
    path("add/",                add,        name="add_polling_station"),
    path("<int:id>/",           details,    name="details_polling_station"),
    path("update/<int:id>/",    update,     name="udpate_polling_station"),
    path("delete/<int:id>/",    delete,     name="delete_polling_station"),



    path("create_images_from_pdf/<int:booth_id>/", create_images_from_pdf, name="create_images_from_pdf"),
    path("draw_boxes_around_voter_details/<int:booth_id>/", draw_boxes_around_voter_details, name="draw_boxes_around_voter_details"),
    path("crop_voter_details_images/<int:booth_id>/", crop_voter_details_images, name="crop_voter_details_images"),
    path("read_voter_id/<int:booth_id>/", read_voter_id, name="read_voter_id"),
    path("capture_details/<int:booth_id>/", capture_details, name="capture_details"),


]
