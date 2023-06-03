from django import forms
from django.forms import ModelForm
from django.forms.utils import ErrorList

from customers.models import Order
from manager.models import query


class EnterTimeForm(ModelForm):
    class Meta:
        model = query
        fields = ['start', 'end']



