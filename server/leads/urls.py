from django.urls import path
from .views import  thankyou
from . import views

urlpatterns = [
    
    path('thank-you/', thankyou, name='thankyou'), 
]