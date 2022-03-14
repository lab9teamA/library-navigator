from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from numpy import number
from libnav.models import Book, Bookcase, Floor, Subject
# from libnav.forms import
from django.shortcuts import redirect
from django.http import HttpResponse


def home(request):
    popular_list = Book.objects.order_by('-likes')[:5]

    context_dict = {
        'popular': popular_list,
    }
    response = render(request, 'libnav/home.html', context= context_dict)

    return response
def about(request):
    response = render(request, 'libnav/about.html')
    return response

def profile(request):
    response = render(request, 'libnav/profile.html')
    return response

def map(request, floor_number):
    context_dict ={}
    try:
        floor = Floor.objects.get(number = floor_number)
        context_dict['floor'] = floor
    except Floor.DoesNotExist:
        context_dict['floor'] = None
    response = render(request, 'libnav/map.html', context = context_dict)
    return response

def book(request, isbn):
    context_dict ={}
    try:
        book = Book.objects.get(ISBN = isbn)
        location = Bookcase.objects.get(id = book.bookcase.id)
        context_dict['book'] = book
        context_dict['bookcase'] = location
    except Book.DoesNotExist:
        context_dict['book'] = None
    response = render(request, 'libnav/book.html', context=context_dict)
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

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
