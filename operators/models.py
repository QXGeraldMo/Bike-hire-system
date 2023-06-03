from django.db import models
from django.utils import timezone
# Create your models here.
class Operator(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=30)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Operators"

    def __str__(self):
        return self.name