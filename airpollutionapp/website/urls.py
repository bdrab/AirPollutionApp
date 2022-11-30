from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('register/', views.register_page, name="register"),
    path('logout/', views.user_logout, name="logout"),
    path('add-sensor/', views.add_sensor, name="add-sensor"),
    path('delete-sensor/<int:sensorid>', views.delete_sensor, name="delete-sensor"),
    path('modify-favourite/<str:operation>/<int:favouriteid>', views.modify_favourite, name="modify-favourite")
]

