# -*- coding: utf-8 -*- 
from django.contrib.auth import views as auth_views, get_user_model
from django.http import Http404
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import json
from auth.forms import RegistrationForm, ResendActTokenForm
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponseNotAllowed, HttpResponseForbidden,\
    HttpResponseNotFound
from Cheetah.Django import render
from django.shortcuts import redirect
from signals import actvation_token_reset 
from consts import REG_SUCCESSFUL
from auth.consts import ACT_TOKEN_EXPIRED, ACT_SUCCESSFUL, ACT_TOKEN_RESENT,\
    REG_SUCCESSFUL_MESSAGE

def login(request,
          template_name='registration/login.html',
          extra_context=None):
     
    response = auth_views.login(request,
        template_name)
     
    if request.POST.has_key('remember_me'):   
        request.session.set_expiry(1209600) # 2 weeks
    else:
        request.session.set_expiry(0)

    return response

def password_reset(request):
    if not request.is_ajax() or not request.method == 'POST':
        raise Http404()
    
    email = request.POST.get('email')
    try:
        validate_email(email)
        auth_views.password_reset(request)
    except ValidationError:
        pass

    return HttpResponse(json.dumps({}),
        content_type="application/json")
    

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
