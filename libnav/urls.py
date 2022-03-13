from django.urls import path
from libnav import views

app_name = 'libnav'

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map, name='map'),
]