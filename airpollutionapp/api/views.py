from website.models import Sensor, Favorite, User, Data
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def home_page(request):
    return HttpResponse("AirPollutionApp by Bartosz Drab")


@csrf_exempt
def add_data(request):
    response = {
        "result": "data sent successfully",
    }
    data = json.loads(request.body)["data"]
    sensor = data['sensor']
    pm1 = data['pm1']
    pm25 = data['pm25']
    pm10 = data['pm10']
    temperature = data['temperature']
    pressure = data['pressure']

    try:
        Data.objects.create(sensor=Sensor.objects.get(pk=sensor),
                            pm1=pm1, pm25=pm25, pm10=pm10,
                            temperature=temperature, pressure=pressure)
    except:
        response["result"] = "data sending failed"
        return JsonResponse(response)

    return JsonResponse(response)


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
