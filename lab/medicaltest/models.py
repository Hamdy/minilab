# -*- coding: utf-8 -*-

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django import forms

class Unit(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False, unique=True)

    def __unicode__(self):
        return self.name

class Range(models.Model):
    SEX_CHOICES = (('male', 'male'), ('female', 'female'))
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=False, blank=False)
    age_from = models.IntegerField(validators=[MinValueValidator(0)])
    AGE_CHOICES = (('day', 'day'), ('month', 'month'), ('year', 'year'))
    age_from_choice =  models.CharField(max_length=5, choices=AGE_CHOICES, null=False, blank=False)
    age_to = models.IntegerField(validators=[MaxValueValidator(120)])
    age_to_choice =  models.CharField(max_length=5, choices=AGE_CHOICES, null=False, blank=False)
    TYPE_CHOICES = (('range', 'range'), ('upto', 'upto'))
    type = models.CharField(max_length=6, choices=TYPE_CHOICES)
    range_from = models.FloatField(validators=[MinValueValidator(0)], default=0)
    range_to = models.FloatField()
    
    def get_age_range_in_days(self):
        min = 0
        max = 0
        
        if self.age_from_choice == 'day':
            min = self.age_from
        elif self.age_from_choice == 'month':
            min = self.age_from * 30
        else:
            min = self.age_from * 365
        
        if self.age_to_choice == 'day':
            max = self.age_to
        elif self.age_to_choice == 'month':
            max = self.age_to * 30
        else:
            max = self.age_to * 365
        
        return (min, max)

    def __repr__(self):
        return "%s : %s %s - %s %s " % (self.sex,
            self.age_from,
            self.age_from_choice,
            self.age_to,
            self.age_to_choice)
    
    def __unicode__(self):
        ret = "%s : %s %s - %s %s " % (self.sex,
                                      self.age_from,
                                      self.age_from_choice,
                                      self.age_to,
                                      self.age_to_choice)
        
        if self.type == "upto":
            ret += "upto %s %s" % (self.range_to, self.unit or '')
        elif self.type == "range":
            ret += "from %s to %s" % (self.range_from, self.range_to)
        
        return ret

class OtherLabs(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False, unique=True)
    
    def __unicode__(self):
        return self.name

class SendingPrice(models.Model):
    price = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    lab = models.ForeignKey(OtherLabs)

    def __unicode__(self):
        return "%s labs - %s" % (self.lab.name, self.price)

class TestGroup(models.Model):
    name = models.CharField("name", max_length=70, unique=True)

    def __unicode__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False, unique=True)
    group = models.ForeignKey(TestGroup, related_name="tests")
    price = models.FloatField(blank=False, null=False, validators=[MinValueValidator(0.0)])
    receiving_price = models.FloatField(verbose_name="سعر الاستقبال من معامل أخرى", blank=False, null=False, validators=[MinValueValidator(0.0)])
    sending_prices = models.ManyToManyField(SendingPrice)
    ranges = models.ManyToManyField(Range, verbose_name="ranges")
    unit = models.ForeignKey(Unit)
    
    def __unicode__(self):
        return self.name