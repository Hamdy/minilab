from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseNotFound
from forms import RegistrationForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from consts import *
from account.forms import ResendActTokenForm
from account.signals import actvation_token_reset

def register(request):
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
            user.is_active = False
            user.reset_activation_token()
            user.generate_verification_token()
            user.save()
            
            return redirect("%s?message=%s" %
                (reverse('message'), REG_SUCCESSFUL))
    else:
        return HttpResponseNotAllowed(permitted_methods=['POST', 'GET'])
    return render(request, 'registration/register.html', {'form':form})

def message(request):
    if not request.method == 'GET':
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    
    message = request.GET.get('message')
    
    if message not in ['reg_successful']:
        return HttpResponseForbidden()
    
    data = {}
    if message == REG_SUCCESSFUL:
        data['message'] = REG_SUCCESSFUL_MESSAGE
            
    return render(request, 'message.html', data)

def activate(request, token=''):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=['GET'])
    
    if request.user.is_authenticated():
        return HttpResponseForbidden()

    User = get_user_model()
    users = User.objects.filter(activation_token=token)
    
    if not users:
        return HttpResponseNotFound()
    
    user = users[0]
    if user.is_active:
        return HttpResponseNotFound()
    data = {}
    
    if user.token_expired:
        data['message'] = ACT_TOKEN_EXPIRED
    else:
        user.activate()
        data['message'] = ACT_SUCCESSFUL
    return render(request, 'message.html', data)

def resend_activation(request):
    if request.user.is_authenticated():
        return HttpResponseForbidden()
    
    if request.method == "GET":
        form = ResendActTokenForm()
    elif request.method == "POST":
        form = ResendActTokenForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            User = get_user_model()
            user = User.objects.filter(email=email)[0]
            user.reset_activation_token()
            user.save()
            actvation_token_reset.send(sender=get_user_model(), token=user.activation_token)
            return render(request, 'message.html', {'message':ACT_TOKEN_RESENT})
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET'])

    return render(request, 'registration/resend_act_token.html', {'form':form})

def verify_account(request):
    pass

def profile(request):
    pass
