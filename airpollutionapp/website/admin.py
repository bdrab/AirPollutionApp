from django.contrib import admin
from .models import Sensor, Data

# Register your models here.

admin.site.register(Sensor)
admin.site.register(Data)
