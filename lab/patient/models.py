# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

def _IDValidator(value):
    if not value.isdigit() or len(value) != 14:
        raise ValidationError(u'%s قيمة خاطئة' % value)

def _nameValidator(value):
    value =  value.strip()
    if value in ['normal', 'vip', 'newest', 'oldest', 'alphabet'] or value.isdigit():
        raise ValidationError(u'%s is not a valid name' % value)
    
class Patient(models.Model):
    name = models.CharField(max_length=70,
        null=False, blank=False, unique=True,
        validators=[_nameValidator])
    
    SEX_CHOICES = (('male', 'ذكر'), ('female', 'أنثى'))
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default="male")
    age_number = models.IntegerField( validators=[MinValueValidator(1), MaxValueValidator(120)])
    AGE_CHOICES = (('day', 'يوم'), ('month', 'شهر'), ('year', 'سنة'))
    age_type = models.CharField(max_length=5, choices=AGE_CHOICES, default="year")
    telephone = models.CharField(max_length=15, blank=True, null=True)
    cell = models.CharField(max_length=14, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    national_ID = models.CharField(max_length=14, validators=[_IDValidator], null=True, blank=True)
    blood_liquidity_treatment = models.BooleanField()
    antibiotique_treatment = models.BooleanField()
    diabetic_treatment = models.BooleanField()
    virus_treatment = models.BooleanField()
    had_blood_transfer = models.BooleanField()
    gland_treatment = models.BooleanField()
    pregnant = models.BooleanField()
    smoker = models.BooleanField()
    liver_treatment = models.BooleanField()
    notes = models.TextField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_age_in_days(self):
        if self.age_type == 'day':
            return self.age_number
        elif self.age_type == 'month':
            return self.age_number * 30
        else:
            return self.age_number * 365
    
    def save(self, *args, **kwargs):
        if self.blood_liquidity_treatment is None:
            self.blood_liquidity_treatment = False
        
        if self.antibiotique_treatment is None:
            self.antibiotique_treatment = False
            
        if self.diabetic_treatment is None:
            self.diabetic_treatment = False
            
        if self.virus_treatment is None:
            self.virus_treatment = False
            
        if self.had_blood_transfer is None:
            self.had_blood_transfer = False
            
        if self.blood_liquidity_treatment is None:
            self.blood_liquidity_treatment = False
            
        if self.gland_treatment is None:
            self.gland_treatment = False
            
        if self.pregnant is None:
            self.pregnant = False
            
        if self.smoker is None:
            self.smoker = False
            
        if self.liver_treatment is None:
            self.liver_treatment = False
            
        super(Patient, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-date_added']

    def __unicode__(self):
        return self.name
    
    def fasted(self):
        return self.fast_hours_count > 0