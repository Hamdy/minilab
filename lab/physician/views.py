from django.shortcuts import render, get_object_or_404
from forms import AddPhysicianForm
from models import Physician
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def add(request):
    if request.method == 'GET':
        form = AddPhysicianForm()
    else:
        form = AddPhysicianForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_physician'))
    return render(request, 'add_physician.html', {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def physician(request, param=''):
    if request.method == "POST":
        param = request.POST.get("param")
    
    if not param:
        physicians = Physician.objects.all()
    elif param == "vip":
        physicians = Physician.objects.filter(is_vip=True).order_by('name')
    elif param == "normal":
        physicians = Physician.objects.filter(is_vip=False).order_by('name')
    else:
        physicians = Physician.objects.filter(name__contains=param.strip()).order_by('name')
    return render(request, 'physicians.html', {'physicians':physicians})

@user_passes_test(lambda u: u.is_superuser)
def confirm_delete(request, id=0):
    physician = get_object_or_404(Physician, pk=id)
    physician.delete()
    return HttpResponseRedirect(reverse('list_physician'))

@user_passes_test(lambda u: u.is_superuser)
def delete(request, id=0):
    physician = get_object_or_404(Physician, pk=id)
    return render(request, 'delete_physician.html', {'physician':physician})

@user_passes_test(lambda u: u.is_superuser)
def edit(request, id=0):
    physician = get_object_or_404(Physician, pk=id)
    if request.method == 'GET':
        form = AddPhysicianForm(instance=physician)
    else:
        form = AddPhysicianForm(request.POST, instance=physician)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('list_physician'))
    return render(request, 'edit_physician.html', {'form':form})

@user_passes_test(lambda u: u.is_superuser)
def physician_reports(request, id=0):
    physician = get_object_or_404(Physician, pk=id)
    return render(request, 'physician_reports.html', {})

