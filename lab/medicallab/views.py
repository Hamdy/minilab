# generate verification UUID.
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotAllowed, HttpResponseForbidden
from forms import MedicalLabForm
from django.shortcuts import render, get_object_or_404, redirect
from models import Lab
from django.db import transaction
from models import Branch
from medicallab.forms import MedicalLabBranchForm
from account.forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from account.consts import REG_SUCCESSFUL

@login_required
def update_create(request, id=0):
    if request.method not in ['GET', 'POST']:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    instance = None
    if id:
        instance = get_object_or_404(Lab, pk=id)
    if request.method == 'GET':
        form = MedicalLabForm(instance)
    elif request.method == 'POST':
        form = MedicalLabForm(request.POST, instance=instance)
        if form.is_valid():
            with transaction.commit_on_success():
                lab = form.save()
                # Only add lab, main branch in new lab creation
                if not instance:
                    request.user.lab = lab
                    request.user.save()
                    Branch.create_main_branch(lab)
    return render(request, 'add_update.html', {'form':form})


#job offers, #patients, #votes up/down
def profile(request, id):
    lab = get_object_or_404(Lab, pk=id)
    return render(request, 'profile.html', {'lab':lab})

def create_update_branch(request, id):
    if request.method not in ['GET', 'POST']:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
    
    instance = None
    if id:
        instance = get_object_or_404(Branch, pk=id)
        if instance.lab != request.user.lab:
            return HttpResponseForbidden()

    if request.method == 'GET':
        form = MedicalLabBranchForm(instance)
    elif request.method == 'POST':
        form = MedicalLabBranchForm(request.POST, instance=instance)
        if form.is_valid():
            form['lab'] = request.user.lab
            form.save()
        # redirect or something
    
    return render(request, 'add_update_branch.html', {'form':form})

# users/admins (invite via email - or add-user / new user Must change his pass)
def add_user(request, bid):
    if request.method not in ['GET', 'POST']:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'GET'])
    
    branch = get_object_or_404(Branch, pk=bid)
    
    if request.method == 'GET':
        form = RegistrationForm()
    elif request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = get_user_model()
            user = user()
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.password = make_password(form.cleaned_data.get('password'))
            user.branch = branch
            user.activate()
            
            #redirect somewhere
        
    return render(request, 'registration/register.html', {'form':form})


def verify(request):
    pass

def settings(request):
    pass

def frienf(request):
    pass

def unfriend(request):
    pass

