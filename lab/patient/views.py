from django.shortcuts import render, get_object_or_404
from forms import AddPatientForm
from models import Patient
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test, login_required

@login_required
def add(request, bid):
    if request.method not in ['GET', 'POST']:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    
    if request.method == 'GET':
        form = AddPatientForm()
    else:
        form = AddPatientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_patients'))
    return render(request, 'add_patient.html', {'form':form})

@login_required
def patients(request, param=''):
    if request.method == "POST":
        param = request.POST.get("param")
    
    if not param or param == "newest":
        patients = Patient.objects.all()
    elif param == "oldest":
        patients = Patient.objects.all().order_by('date_added')
    elif param == "alphabet":
        patients = Patient.objects.all().order_by('name')
    elif param.isdigit():
        if len(param) > 10:
            patients = Patient.objects.filter(national_ID=param)
        else:
            patients =Patient.objects.filter(id=int(param))
    elif isinstance(param, basestring):
        patients = Patient.objects.filter(name__contains=param).order_by('-date_added')
    return render(request, 'patients.html', {'patients':patients})

@user_passes_test(lambda u: u.is_superuser)
def confirm_delete(request, id=0):
    patient = get_object_or_404(Patient, pk=id)
    patient.delete()
    return HttpResponseRedirect(reverse('list_patients'))

@user_passes_test(lambda u: u.is_superuser)
def delete(request, id=0):
    patient = get_object_or_404(Patient, pk=id)
    return render(request, 'delete_patient.html', {'patient':patient})

@login_required
def edit(request, id=0):
    patient = get_object_or_404(Patient, pk=id)
    if request.method == 'GET':
        form = AddPatientForm(instance=patient)
    else:
        form = AddPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_patients'))
    return render(request, 'edit_patient.html', {'form':form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def patient_reports(request, id=0):
    patient = get_object_or_404(Patient, pk=id)
    return render(request, 'patient_reports.html', {})
