from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict

from .models import Sensor, Data, Favorite
from .forms import SensorForm


def index(request):
    context = {}
    sensors = Sensor.objects.all()

    all_sensors_list = {sensor.id: {'id': sensor.id,
                                    'serial': sensor.serial,
                                    'lat': float(sensor.lat),
                                    'lon': float(sensor.lon),
                                    'description': sensor.description,
                                    'owner': sensor.owner.id}
                        for sensor in sensors}

    markers = [{'lat': sensor.lat,
                'lon': sensor.lon,
                'popup': sensor.description,
                'id': sensor.id
                } for sensor in sensors]

    if not request.user.is_authenticated:
        form_register = UserCreationForm()
        context["form_register"] = form_register
        favourite_sensors_list = {}
    else:
        form_sensor = SensorForm()
        context["form_sensor"] = form_sensor
        user = User.objects.get(id=request.user.id)
        favourite_sensors_list = {value.sensor.id: {'id': value.sensor.id,
                                                    'serial': value.sensor.serial,
                                                    'lat': float(value.sensor.lat),
                                                    'lon': float(value.sensor.lon),
                                                    'description': value.sensor.description,
                                                    'owner': value.sensor.owner.id}
                                  for value in user.favorites.all()}

    context["markers"] = markers
    context['sensors'] = sensors
    context['favouriteSensorsList'] = favourite_sensors_list
    context['allSensors'] = all_sensors_list

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


@login_required
def modify_favourite(request, operation, favouriteid):

    response = {
        "favourite":  favouriteid,
        "operation":  operation,
        "status": "failed"
    }

    if request.user.is_authenticated:
        try:
            favourite = Favorite.objects.get(sensor=Sensor.objects.get(id=favouriteid))
        except Favorite.DoesNotExist:
            Favorite.objects.create(user=User.objects.get(id=request.user.id), sensor=Sensor.objects.get(id=favouriteid))
            return JsonResponse(response)

        favourite.delete()
    response["status"] = "successful"
    return JsonResponse(response)
