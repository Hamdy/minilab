# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

def _nameValidator(value):
    value =  value.strip()
    if value in ['normal', 'vip', 'newest', 'oldest', 'alphabet'] or value.isdigit():
        raise ValidationError(u'%s is not a valid name' % value)
    
class Physician(models.Model):
    name = models.CharField(max_length=40,
        null=False, blank=False, unique=True,
        validators=[_nameValidator],
        error_messages={'unique':"موجود مسبقا"})
    address = models.CharField(max_length=70, null=True, blank=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    cell = models.CharField(max_length=15, blank=True, null=True)
    is_vip = models.BooleanField(default=True)
    
    class Meta:
        ordering=['-is_vip', 'name']
    def __unicode__(self):
        return self.name

