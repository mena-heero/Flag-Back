from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "authentication"

public_router = DefaultRouter()
public_router.register(r"users", PublicUserApiViewset, "public_user_api")


urlpatterns = [
    path("public/", include(public_router.urls)),
]
