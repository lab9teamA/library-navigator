from django.shortcuts import render
from django.urls import reverse
# from libnav.models import
# from libnav.forms import
from django.shortcuts import redirect


def home(request):
    response = render(request, 'libnav/home.html')

    return response
