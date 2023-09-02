from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

app_name = "affiliate"

public_router = DefaultRouter()
public_router.register(r"creatives", CreativeApiViewset, "public_creatives_api")
public_router.register(r"brands", BrandApiViewset, "public_brand_api")
public_router.register(r"evest", EvestApiViewset, "public_evest_api")


urlpatterns = [
    path("public/", include(public_router.urls)),
]
