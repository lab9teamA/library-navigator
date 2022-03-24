import json
from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from libnav.models import Book, Bookcase, Floor, Subject, UserProfile, FriendRequest
from libnav.forms import UserForm, UserProfileForm
from django.shortcuts import redirect
from library_navigator.settings import MEDIA_URL
from django.http import HttpResponse, JsonResponse

from libnav.miscs.locations_keeper import locations,location

from django.http.response import JsonResponse


def put(request):
    if request.method == 'GET':
        return JsonResponse({"key": "value"})
    else:
        return HttpResponse()

def testPage(request):
    return render(request, "libnav/test.html")


def home(request):
    people_like_list = Book.objects.order_by('-likes')[:4]
    popular_list = Book.objects.order_by('-numCheckedOut')[:4]


    context_dict = {
        'people_like': people_like_list,
        'popular': popular_list
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
            friend_requests = FriendRequest.objects.filter(to_user = current_user)
            context_dict["requests"] = friend_requests
        except:
            context_dict["friends"] = None
            context_dict['requests'] = None
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
        if current_user.is_authenticated:
            if userProfile.friends.filter(username = current_user).exists():
                context_dict['notFriends'] = False
            else:
                context_dict['notFriends'] = True

        response = render(request, 'libnav/profile.html', context= context_dict)
    #if logged in return myprofile.html
    return response

@login_required
def edit_profile(request):
    if request.method == 'POST':
        current_user = request.user
        profile = UserProfile.objects.get(user = current_user)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            print(profile_form.cleaned_data)
            data = profile_form.cleaned_data
            if data['website']:
                profile.website = data['website']
            if data['description']:
                profile.description = data['description']
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            return redirect(reverse('libnav:profile', kwargs={'username': current_user.username}))
        else:
            print(profile_form.errors)
    else:
        context_dict = {'profile_form': UserProfileForm()}
        return render(request, 'libnav/edit_profile.html', context=context_dict)


current_floor = 1

def map(request, floor_number):
    context_dict ={}
    try:
        floor = Floor.objects.get(number = floor_number)
        context_dict['floor'] = floor
        books = Book.objects.filter(bookcase__in=Bookcase.objects.filter(floor=Floor.objects.get(number=floor_number))).order_by('-likes')
        context_dict['books'] = books
    except Floor.DoesNotExist or Bookcase.DoesNotExist:
        context_dict['floor'] = None
        context_dict['books'] = None
    response = render(request, 'libnav/map.html', context = context_dict)
    global current_floor
    current_floor = floor_number
    return response

def updateMap(request, floor_number):
    floor = Floor.objects.get(number=floor_number)
    response = HttpResponse(json.dumps({"mapName": floor.mapName, "number": floor.number, "mediaUrl": MEDIA_URL}))
    response["Access-Control-Allow-Origin"] = "*"
    return response

def getCurrentFloor(request):
    response = HttpResponse(json.dumps({"floor_number": current_floor}))
    response["Access-Control-Allow-Origin"] = "*"
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
        if request.POST.get('submit') == 'Login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username= username, password = password)

            if user:
                if user.is_active:
                    login(request, user)
                    user_id=UserProfile.objects.get(user=User.objects.get(username=username)).user_id
                    print(user_id)
                    request.session['user_id'] = UserProfile.objects.get(user=User.objects.get(username=username)).user_id
                    print(request.session['user_id'])
                    return redirect(reverse('libnav:home'))
                else:
                    return HttpResponse("Your LIBNAV account is disabled.")
            else:
                print(f"Invalid login details: {username}, {password}")
                return HttpResponse("Invalid login details supplied.")
        # register form
        elif request.POST.get('submit') == 'Register':
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
                request.session['user_id'] = profile.user_id
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
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect(reverse('libnav:home'))

@login_required
def api_get_loc(request):
    username = request.user.id

    user = User.objects.get(id=request.user.id)
    userProfile = UserProfile.objects.get(user=user)

    a = list()
    a.append(user)
    user_loc = locations.get_all_by_users(a)

    friends = [x.id for x in userProfile.friends.all()]
    friends_locations = locations.get_all_by_users(friends)

    public_loc = [x for x in locations.get_all_public_locations() if x not in friends_locations]
    if user_loc in public_loc:
        public_loc.remove(user_loc)

    response = JsonResponse({"user_loc" : user_loc, "friends" : friends_locations,"others" : public_loc})
    response["Access-Control-Allow-Origin"] = "*"
    return response

@login_required
def api_set_loc(request):
    l = location(user =  request.user.id,
             x = request.POST["x"],
             y = request.POST["y"],
             floor = request.POST["floor"],
             private = request.POST["private"])
    locations.add(l)

    return HttpResponse()
  
def send_friend_request(request, username):
    from_user = request.user
    to_user = User.objects.get(username = username)
    friend_request, created = FriendRequest.objects.get_or_create(from_user = from_user, to_user = to_user)
    if created:
        messages.info(request, 'friend request sent successfully!')
    else:
        messages.info(request, 'friend request was already sent')
    return redirect(reverse('libnav:profile',kwargs={'username':username}))

@login_required
def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id = requestID)
    from_user = UserProfile.objects.get(user = friend_request.from_user)
    to_user = UserProfile.objects.get(user = friend_request.to_user)
    if friend_request.to_user == request.user:
        to_user.friends.add(friend_request.from_user)
        from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        messages.info(request, 'friend request accepted')
    else:
        messages.info(request, 'friend request not accepted')
    return redirect(reverse('libnav:profile',kwargs={'username':to_user.user.username}))
        
@login_required
def delete_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id = requestID)
    if friend_request.to_user == request.user:
        friend_request.delete()
        messages.info(request, 'friend request deleted')
    else:
        messages.info(request, 'friend request not deleted')
    return redirect(reverse('libnav:profile',kwargs={'username':friend_request.to_user.username}))

@login_required
def delete_friend(request, username):
    current_user = request.user
    deleted = User.objects.get(username = username)
    UserProfile.objects.get(user = current_user).friends.remove(deleted)
    UserProfile.objects.get(user = deleted).friends.remove(current_user)
    messages.info(request, 'friend deleted')
    return redirect(reverse('libnav:profile',kwargs={'username':username}))

def search(request):
    term = request.GET['search']
    
    context_dict ={'term':term,
        'books': Book.objects.filter(title__contains = term),
        'users': User.objects.filter(username__contains = term),

        }
    return render(request, 'libnav/search.html', context=context_dict)
