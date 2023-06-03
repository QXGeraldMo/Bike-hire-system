from django.db import models

# Create your models here.
from django.utils import timezone

from customers.models import vehicle_list


class query(models.Model):
    start = models.DateTimeField(default="")
    end = models.DateTimeField(default="")

    def __str__(self):
        return '%s %s' % (self.start, self.end)

class temp(models.Model):
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






