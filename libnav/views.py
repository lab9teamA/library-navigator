from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from libnav.models import Book, Bookcase, Floor, Subject, UserProfile
from libnav.forms import UserForm, UserProfileForm
# from libnav.forms import
from django.shortcuts import redirect
from django.http import HttpResponse

from django.http.response import JsonResponse


def put(request):
    if request.method == 'GET':
        return JsonResponse({"key": "value"})
    else:
        return HttpResponse()

def testPage(request):
    return render(request, "libnav/test.html")


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

def profile(request, username):
    context_dict = {}
    current_user = request.user
    try:
        user = User.objects.get(username = username)
        userProfile = UserProfile.objects.get(user = user)
        context_dict["user"]= user
        context_dict["userProfile"] = userProfile
    except User.DoesNotExist:
        context_dict["user"]= None
        context_dict["userProfile"] = None
    if current_user.is_authenticated and user == current_user:
        try:
            friends = userProfile.friends.all()
            context_dict["friends"] = friends
        except:
            context_dict["friends"] = None
        response = render(request, 'libnav/my_profile.html', context= context_dict)

    else:
        try:
            recommended = userProfile.recommends.all()
            context_dict["recommended"] = recommended
            reading = userProfile.isReading.all()
            context_dict["reading"] = reading
        except:

            context_dict["recommended"] = None
            context_dict["reading"] = None
        response = render(request, 'libnav/profile.html', context= context_dict)
    #if logged in return myprofile.html
    return response

def map(request, floor_number):
    context_dict ={}
    try:
        floor = Floor.objects.get(number = floor_number)
        context_dict['floor'] = floor
        books = Book.objects.order_by('-likes')
        context_dict['books'] = books
    except Floor.DoesNotExist:
        context_dict['floor'] = None
        context_dict['books'] = None
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
    if request.user.is_authenticated:
        return redirect(reverse('libnav:profile', kwargs={'username': request.user.username}))
    
    if request.method == 'POST':
        # login form 
        if request.POST.get('submit') == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username= username, password = password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('libnav:home'))
                else:
                    return HttpResponse("Your LIBNAV account is disabled.")
            else:
                print(f"Invalid login details: {username}, {password}")
                return HttpResponse("Invalid login details supplied.")
        # register form 
        elif request.POST.get('submit') == 'register':
            user_form = UserForm(request.POST)
            profile_form = UserProfileForm(request.POST)
            
            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user 
                
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']
                    
                profile.save()
                
                login(request, user)
                return redirect(reverse('libnav:profile', kwargs={'username': user.username}))
            else:
                print(user_form.errors, profile_form.errors)
    # not post          
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    return render(request,
        'libnav/login.html',
        context = {
            'user_form': user_form,
            'profile_form': profile_form,})

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('libnav:home'))
        