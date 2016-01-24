# -*- coding: utf-8 -*-
from django import forms
from models import Patient

class AddPatientForm(forms.ModelForm):
    def clean_pregnant(self):
        if self.cleaned_data['pregnant'] and self.cleaned_data['sex'] != 'female':
            raise forms.ValidationError("هذا الحقل للإناث فقط")
        return self.cleaned_data['pregnant']
    
    def clean_national_ID(self):
        nid = self.cleaned_data.get('national_ID')
        if nid:
            patient = Patient.objects.filter(national_ID=nid)
            if patient.count() > 0 and patient[0].national_ID != self.instance.national_ID:
                raise forms.ValidationError("مسجل من قبل")
        return nid
    class Meta:
        model = Patient
