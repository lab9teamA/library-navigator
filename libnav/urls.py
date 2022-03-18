from django.urls import path
from libnav import views

app_name = 'libnav'

urlpatterns = [
    path('', views.home, name='home'),
    path('map/<floor_number>/', views.map, name='map'),
    path('about/', views.about, name= 'about'),
    path('profile/<username>/', views.profile, name = 'profile'),
    path('book/<isbn>/', views.book, name ='book'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('put/', views.put, name='put'),
    path('test/', views.testPage, name='test'),
    path('send_friend_request/<username>/', views.send_friend_request, name = 'send friend request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name = 'accept friend request'),
    path('delete_friend_request/<int:requestID>/', views.delete_friend_request, name = 'delete friend request'),
]