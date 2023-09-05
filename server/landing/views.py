from django.views.generic import TemplateView 
from .models import Lead
from .serializers import LeadSerializer
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response






class LandingPageView(TemplateView):
    template_name = 'landing/lp1.html'  # Default template

    def get_template_names(self):
        # Get the template_name parameter from the URL
        template_name = self.kwargs.get('template_name', 'lp1')
        return ['landing/{}.html'.format(template_name)]



class ThankYouView(TemplateView):
    template_name = 'landing/thankyou.html'

class CreateLeadApi(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    pagination_class = None
    
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         # Save the contact form data
    #         self.perform_create(serializer)

    #         # Define the thank you page URL
    #         thank_you_url = 'landing/thankyou/'  # Replace with your actual thank you page URL

    #         return Response({'redirect_url': thank_you_url}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
