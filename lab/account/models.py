from django.contrib.auth.models import AbstractUser
from django.db import models
from medicallab.models import Lab, Country, Branch
from random import choice
from string import letters, digits
from datetime import date, timedelta

class User(AbstractUser):
    country = models.ForeignKey(Country, blank=True, null=True)
    lab = models.OneToOneField(Lab, blank=True, null=True)
    branch = models.OneToOneField(Branch, blank=True, null=True)
    verification_token = models.CharField(max_length=80, blank=True, null=True)
    activation_token = models.CharField(max_length=80, blank=True, null=True)
    
    def is_employer(self):
        return bool(self.branch)
    
    def is_lab_owner(self):
        return bool(self.lab)

    def reset_activation_token(self):
        #yyyy-mm-dd
        expired_at = str(date.today() + timedelta(days=60)).replace('-', '')
        self.activation_token = expired_at + ''.join(choice(
            letters + digits) for _ in range(72))

    def generate_verification_token(self):
        self.verification_token = ''.join(choice(
            letters + digits) for _ in range(80))
    
    @property
    def token_expired(self):
        expiration_str = self.activation_token[:8]
        try:
            expiration_date = date(int(expiration_str[:4]),
                int(expiration_str[4:6]), int(expiration_str[6:8]))
        except:
            return True
        return expiration_date < date.today()

    def activate(self):
        self.is_active = True
        self.activation_token = None
        self.save()

    def verify(self):
        self.verification_token = None
        self.save()
    
    @property
    def activated(self):
        return self.is_active
    
    @property
    def verified(self):
        return bool(self.verification_token)