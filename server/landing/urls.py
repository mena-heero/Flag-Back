from django.urls import path
from . import views

app_name = 'landing'

urlpatterns = [
    path('<str:template_name>/', views.LandingPageView.as_view(), name='landing_page'),
]
