from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('add-sensor/', views.add_sensor, name="add-sensor"),
    path('return-data/', views.return_data, name="return-data"),
    path('map/', views.maps, name="maps")
]

