from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Sensor, Data
from .forms import SensorForm
# Create your views here.
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods


def index(request):
    q = request.GET.get('q', None)
    # print(help(type(request)))
    print(request.get_full_path_info())
    sensors = Sensor.objects.all()
    markers = [{'lat': sensor.lat,
                'lon': sensor.lon,
                'popup': sensor.description,
                'id': sensor.id
                } for sensor in sensors]

    context = {}
    if not request.user.is_authenticated:
        form_register = UserCreationForm()
        context["form_register"] = form_register
    else:
        form_sensor = SensorForm()
        context["form_sensor"] = form_sensor

    context["markers"] = markers
    context['sensors'] = sensors

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

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        return redirect('index')


def user_logout(request):
    logout(request)
    return redirect('index')


def return_data(request):
    pk = int(request.GET.get('q'))
    sensor = Sensor.objects.get(pk=pk)
    data = list(sensor.data_set.all())

    dates = list(reversed([record.created for record in data]))
    pm1 = list(reversed([record.pm1 for record in data]))
    pm25 = list(reversed([record.pm25 for record in data]))
    pm10 = list(reversed([record.pm10 for record in data]))
    temperature = list(reversed([record.temperature for record in data]))
    pressure = list(reversed([record.pressure for record in data]))

    data_dict = {
        "dates": dates,
        "pm1": pm1,
        "pm25": pm25,
        "pm10": pm10,
        "temperature": temperature,
        "pressure": pressure
    }
    data_to_send = {
        "sensor":  pk,
        "data":  data_dict,
    }

    return JsonResponse(data_to_send)


@require_http_methods(["POST"])
def add_sensor(request):
    form = SensorForm(request.POST)
    if form.is_valid():
        sensor = form.save(commit=False)
        sensor.owner = request.user
        sensor.save()
        return redirect('index')


def delete_sensor(request, sensorid):
    sensor = Sensor.objects.get(id=sensorid)
    if sensor.owner == request.user:
        sensor.delete()
    return redirect('index')



def settings(request):
    return redirect('index')
