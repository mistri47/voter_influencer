from django.urls import include, path


import partyworker.views as party_worker_views

urlpatterns = [
    path("workers/", party_worker_views.workers, name="workers"),
]