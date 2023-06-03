from django import forms
from django.utils.safestring import mark_safe
from django.forms import ModelForm
from customers.models import vehicle_list, destination_location


class TrackBike(forms.Form):
    bike_id = forms.ModelChoiceField(queryset=vehicle_list.objects.all(), label=mark_safe('Choose a Vehicle  '))


class ChargeBike(forms.Form):
    bike_id_charge = forms.ModelChoiceField(queryset=vehicle_list.objects.filter(battery__lte=10),
                                            label=mark_safe('Vehicles That Needs To Be Charged  '))


class RepairBike(forms.Form):
    bike_id_repair = forms.ModelChoiceField(queryset=vehicle_list.objects.filter(repair=True),
                                            label=mark_safe('Vehicles That Needs To Be Repaired '))


class MoveBike(forms.Form):
    bike_id_move = forms.ModelChoiceField(queryset=vehicle_list.objects.filter(repair=False, status=False),
                                          label=mark_safe('Vehicle '))


class StartLocation(forms.Form):
    bike_start_location = forms.ModelChoiceField(queryset=destination_location.objects.all(),
                                                 label=mark_safe('Location '))
