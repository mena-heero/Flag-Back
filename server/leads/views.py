from django.shortcuts import redirect
from django.shortcuts import render
from .forms import LeadForm




def thankyou(request):
  return render(request, 'leads/thankyou.html')