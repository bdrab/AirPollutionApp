from django.shortcuts import render
from django.http.response import HttpResponse
# Create your views here.
from website.models import Sensor, Data, Favorite
from django.http import JsonResponse


def home_page(request):
    return HttpResponse("AirPollutionApp by Bartosz Drab")


def return_data(request):
    pk = int(request.GET.get('q'))

    try:
        sensor = Sensor.objects.get(pk=pk)
    except Sensor.DoesNotExist:
        data_to_send = {
            "sensor": "sensor_not_found",
            "data": "sensor_not_found",
        }
        return JsonResponse(data_to_send)

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
        "sensor": pk,
        "data": data_dict,
    }

    return JsonResponse(data_to_send)