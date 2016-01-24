from django import forms
from models import Physician

class AddPhysicianForm(forms.ModelForm):
    class Meta:
        model = Physician
