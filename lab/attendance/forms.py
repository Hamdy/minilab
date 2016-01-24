from django import forms
from django.forms.fields import CharField

class AttendanceForm(forms.Form):
    pass


class DepartureForm(forms.Form):
    pass

class Patient(forms.Form):
    name = forms,CharField('Name', max_length='75')