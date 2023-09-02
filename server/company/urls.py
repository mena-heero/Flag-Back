from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "company"

public_router = DefaultRouter()
public_router.register(r"companies", CompanyApiViewset, "public_company_api")
public_router.register(r"ratings", RatingReviewApiViewset, "public_rating_api")
public_router.register(
    r"saved-topics", SavedTopicApiViewset, "public_saved_topic_api")


urlpatterns = [
    path("public/", include(public_router.urls)),
]
