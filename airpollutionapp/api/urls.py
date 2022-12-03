from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name="api-home"),
    path('return-data/', views.return_data, name="return-data"),
    path('modify-favourite/<str:operation>/<int:favouriteid>', views.modify_favourite, name="modify-favourite"),
    path('add-data/', views.add_data, name="add-data")
]
