from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.


def home_page(request):
    context = {}
    return render(request, 'website/index.html', context)


def login_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            return render(request, 'website/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'website/login.html')


def register_page(request):

    if request.user.is_authenticated:
        return redirect('home')

    form = UserCreationForm()
    context = {"form": form}

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print("not")
    return render(request, 'website/register.html', context)


def map_page(request):
    marker = {'lat': 50.054045434391156, 'lon': 19.935247879895858, 'popup': "PM1: 10 ,PM2.5: 23, PM10: 45"}
    context = {"marker": marker,
               "dane": 123}
    return render(request, 'website/map.html', context)


def user_logout(request):
    logout(request)
    return redirect('home')