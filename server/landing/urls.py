from django.urls import path , include
from .views import LandingPageView, CreateLeadApi , ThankYouView
from rest_framework import routers



app_name = 'landing'
# Create a router for your API views
router = routers.DefaultRouter()
router.register(r'api/leads', CreateLeadApi)

urlpatterns = [
    # URL for your LandingPageView, allowing for a dynamic template name
    path('<str:template_name>/', LandingPageView.as_view(), name='landing-page'),
    path('thankyou/', ThankYouView.as_view(), name='thank-you'),
    # Include API URLs from the router
    path('', include(router.urls)),
]
