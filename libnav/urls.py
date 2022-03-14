from django.urls import path
from libnav import views

app_name = 'libnav'

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map, name='map'),
    path('about/', views.about, name= 'about'),
    path('profile/<user-id>/', views.profile, name = 'profile'),
    path('book/<ISBN>/', views.book, name ='book'),
    path('login/', views.user_login, name='login')
]