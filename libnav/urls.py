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
    path('api/set-loc',views.api_set_loc,name="setloc"),
    path('api/get-loc',views.api_get_loc,name="getloc"),
]