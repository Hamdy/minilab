# -*- coding: utf-8 -*- 
from django import forms
from auth.permissions import PERMISSIONS
from django.forms.util import ErrorList
from django.contrib.auth import get_user_model
from common.validators import non_empty_validator
    
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=2,
        max_length=40, validators=[non_empty_validator])
    
    email= forms.EmailField()
    password = forms.CharField(min_length=6, 
        widget=forms.PasswordInput())
    
    password2 = forms.CharField(min_length=6, 
        widget=forms.PasswordInput())
    
    def clean_username(self):
        username = self.cleaned_data.get('username').strip().lower()
        user = get_user_model()
        if user.objects.filter(username=username):
            self._errors['username'] = self._errors.get('username', ErrorList())
            self._errors['username'].append("Already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        user = get_user_model()
        if user.objects.filter(email=email):
            self._errors['email'] = self._errors.get('email', ErrorList())
            self._errors['email'].append("Already exists")
        return email
    
    def clean(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

                    
        if not password == password2:
            self._errors['password2'] = self._errors.get('password2', ErrorList())
            self._errors['password2'].append("Passwords don't match")
        
        # Set lower values
        self.cleaned_data['password'] = password
        self.cleaned_data['password2'] = password2
        
        return self.cleaned_data

class ResendActTokenForm(forms.Form):
    email = forms.EmailField(max_length=100)
    
    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        User = get_user_model()
        users = User.objects.filter(email=email)
        
        if not users:
            self._errors['email'] = self._errors.get('email', ErrorList())
            self._errors['email'] = 'Not Found'
            
        elif users[0].is_active:
            self._errors['email'] = self._errors.get('email', ErrorList())
            self._errors['email'] = 'Already active'
        return email
        
class PermissionForm(forms.Form):
    """
    Django makes permissions automatically
    for every model, i.e add_contract,
    change_contract, delete_contract
    We make use of those.
    """
    TYPES = (
        ('employee','employee'),
        ('category','category'),)
    
    PERMISSION_CHOICES=tuple([(y, y) for x in PERMISSIONS for y in x[1]])
    
    def __init__(self, employees, company, *args, **kwargs):
        super(PermissionForm, self).__init__(*args, **kwargs)
        
        self.fields['employee'] = forms.ModelChoiceField(
            queryset=employees,
            required=False,
            widget=forms.Select(
                attrs={'class':'form-control'}))
        
        self.fields['category'] = forms.ModelChoiceField(
            queryset=company.job_categories.all(),
            required=False,
            widget=forms.Select(
                attrs={'class':'form-control'}))
        
    
    type = forms.ChoiceField(choices=TYPES)

    permissions = forms.MultipleChoiceField(
        choices=PERMISSION_CHOICES,
        required=False,
        widget=forms.SelectMultiple(
            attrs={'class':'form-control'}))
    
    def clean(self):
        type = self.cleaned_data.get('type')
        category = self.cleaned_data.get('category')
        employee = self.cleaned_data.get('employee')
        
        if type == "employee" and not employee:
            error = self._errors.get('employee',  ErrorList())
            error.append("هذا الحقل مطلوب .")
            self._errors['employee'] = error
        elif type == "category" and not category:
            error = self._errors.get('category',  ErrorList())
            error.append("هذا الحقل مطلوب .")
            self._errors['category'] = error
        
        
        return self.cleaned_data
    
