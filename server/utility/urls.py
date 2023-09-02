from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "utility"

public_router = DefaultRouter()
public_router.register(r"settings", SettingsApiViewset, "public_settings_api")
public_router.register(r"stories", StoryApiViewset, "public_story_api")
public_router.register(
    r"all-country", AllCountryApiViewset, "public_all_country_api")
public_router.register(
    r"contact-us", ContactUsApiViewset, "public_contact_us_api")

urlpatterns = [
    path("public/", include(public_router.urls)),
]
