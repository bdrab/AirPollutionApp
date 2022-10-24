from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Sensor, Data
from .forms import SensorForm
# Create your views here.
from django.forms.models import model_to_dict


def index(request):
    q = request.GET.get('q', None)
    sensors = Sensor.objects.all()
    markers = [{'lat': sensor.lat,
                'lon': sensor.lon,
                'popup': sensor.description,
                'id': sensor.id
                } for sensor in sensors]

    context = {"markers": markers}
    return render(request, 'website/map.html', context)


def login_page(request):

    if request.user.is_authenticated:
        return redirect('index')

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
            return redirect('index')

    return render(request, 'website/login.html')


def register_page(request):

    if request.user.is_authenticated:
        return redirect('index')

    form = UserCreationForm()
    context = {"form": form}

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    return render(request, 'website/register.html', context)


def user_logout(request):
    logout(request)
    return redirect('index')


def add_sensor(request):
    return redirect('index')


def return_data(request):
    pk = int(request.GET.get('q'))
    sensor = Sensor.objects.get(pk=pk)

    data = list(sensor.data_set.all())
    data_dict = list(map(model_to_dict, data))

    data_to_send = {
        "sensor":  pk,
        "data":  data_dict,
    }
    print(data_to_send)
    return JsonResponse(data_to_send)


def add_sensor(request):
    form = SensorForm()
    if request.method == "POST":
        form = SensorForm(request.POST)
        if form.is_valid():
            sensor = form.save(commit=False)
            sensor.owner = request.user
            sensor.save()
            return redirect('home')
    context = {"form": form}
    return render(request, 'website/add_sensor.html', context)


def settings(request):
    return redirect('index')
