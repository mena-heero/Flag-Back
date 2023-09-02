from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "home"

public_router = DefaultRouter()
public_router.register(r"companies", CompanyDetailApiViewset, "companies_api")
public_router.register(r"company-finder-rating",
                       CompanyFinderRatingApiViewset, "company_finder_rating_api")


urlpatterns = [
    path("public/", include(public_router.urls)),
]
