from django import forms
from django.contrib.auth import get_user_model
from django.forms.util import ErrorList
from common.validators import non_empty

class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=2,
        max_length=40, validators=[non_empty])
    
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