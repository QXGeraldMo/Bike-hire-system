from django.contrib import admin
from .models import vehicle_list, destination_location, Order

admin.site.register(vehicle_list)
admin.site.register(destination_location)
admin.site.register(Order)




