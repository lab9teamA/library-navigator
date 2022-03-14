from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# from libnav.models import
# from libnav.forms import
from django.shortcuts import redirect
from django.http import HttpResponse


def home(request):
    response = render(request, 'libnav/home.html')

    return response
def about(request):
    response = render(request, 'libnav/about.html')
    return response

def profile(request):
    response = render(request, 'libnav/profile.html')
    return response

def map(request):
    response = render(request, 'libnav/map.html')
    return response

def book(request):
    response = render(request, 'libnav/book.html')
    return response

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username= username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('libnav:index'))
            else:
                return HttpResponse("Your LIBNAV account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'libnav/login.html')