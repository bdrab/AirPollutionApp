from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="home"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('map/', views.map_page, name="map"),
    path('logout/', views.user_logout, name="logout")
]
