from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class destination_location(models.Model):
    street_id = models.IntegerField(primary_key=True)
    street_name = models.CharField(max_length=20, default="")
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    def __str__(self):
        return str(self.street_name)


class vehicle_list(models.Model):
    id = models.IntegerField(primary_key=True)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    location = models.ForeignKey(destination_location, on_delete=models.CASCADE, related_name='vehicle_list')
    battery = models.IntegerField(default=100)
    status = models.BooleanField(default=False)
    repair = models.BooleanField(default=False)
    v_type = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    duration = models.CharField(max_length=40)
    departure = models.CharField(max_length=40)
    destination = models.CharField(max_length=40)
    customer = models.CharField(max_length=10, default="")
    v_id = models.ForeignKey(vehicle_list, on_delete=models.CASCADE)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        verbose_name_plural = "Order"
