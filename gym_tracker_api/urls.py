"""
URL configuration for gym_tracker_api project.
"""
from django.urls import include, path

urlpatterns = [
    path("api/", include("api.urls")),
]
