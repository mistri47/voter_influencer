from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token


import voter.views as voter_views
import partyworker.views as party_worker_views
import polling_station.views as polling_views


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),

    path("voters/", include('voter.urls')),
    path("workers/", include('partyworker.urls')),
    path("expenses/", include('expenses.urls')),
    path("polling_stations/", include('polling_station.urls')),


    # Static Pages: Need to create apps
    # TBD #1: Create CRUD for Worker Types
    # TBD #2: Manage Casts

    path("comm/", TemplateView.as_view(template_name="communication/comm.html"), name="communication"),
    path("graphs/", TemplateView.as_view(template_name="graph/graphs.html"), name="graphs"),
    path("results/", TemplateView.as_view(template_name="result/results.html"), name="results"),

    
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("voter_influencer.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
