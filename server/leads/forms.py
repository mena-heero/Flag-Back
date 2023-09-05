from django import forms
from .models import LeadF

class LeadForm(forms.ModelForm):
  class Meta:
    model = LeadF
    fields = ['name', 'email', 'phone']