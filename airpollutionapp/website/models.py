from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Sensor(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    serial = models.CharField(max_length=200)
    lat = models.DecimalField(decimal_places=15, max_digits=20, default=0)
    lon = models.DecimalField(decimal_places=15, max_digits=20, default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.serial


class Data(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    pm1 = models.IntegerField()
    pm25 = models.IntegerField()
    pm10 = models.IntegerField()
    temperature = models.FloatField()
    pressure = models.FloatField()

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return str(self.sensor) + str(self.created)


class Favorite(models.Model):
    user = models.ForeignKey(User, related_name='favorites', on_delete=models.SET_NULL, null=True)
    sensor = models.ForeignKey(Sensor, related_name='favorites', on_delete=models.CASCADE, null=True)
