from django.shortcuts import render
from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    template_name = 'landing/lp1.html'  # Default template

    def get_template_names(self):
        # Get the template_name parameter from the URL
        template_name = self.kwargs.get('template_name', 'lp1')
        return ['landing/{}.html'.format(template_name)]

