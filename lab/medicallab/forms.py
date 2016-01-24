from django import forms
from models import Lab
from models import Branch


class MedicalLabForm(forms.ModelForm):
    class Meta:
        model = Lab
        exclude = ['is_verified']
        
class MedicalLabBranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        exclude = ['lab', 'is_main']
        