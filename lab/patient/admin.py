from django.contrib import admin
from models import Patient
from patient.forms import AddPatientForm

class PatientAdmin(admin.ModelAdmin):
    model = Patient
    form = AddPatientForm
    
admin.site.register(Patient, PatientAdmin)