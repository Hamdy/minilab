# -*- coding: utf-8 -*-
from django.db import models
from medicaltest.models import Test, OtherLabs
from django.core.validators import MaxValueValidator, MinValueValidator
from physician.models import Physician
from patient.models import Patient
from django import forms

class AnalysisTestInfo(models.Model):
    analysis = models.ForeignKey('Analysis', related_name='tests')
    test = models.ForeignKey(Test)
    result = models.FloatField(null=True, blank=True)
    from_lab = models.BooleanField(default=False)
    to_lab = models.BooleanField(default=False)
    lab = models.ForeignKey(OtherLabs, null=True, blank=True)

    def is_from_lab(self):
        return self.from_lab and self.lab
    
    def is_to_lab(self):
        return self.to_lab and self.lab
    
    def cost(self):
        if self.is_from_lab():
            return self.test.receiving_price
        return self.test.price
    
    def sending_cost(self):
        if not self.is_to_lab():
            return 0.0
        return self.test.sending_prices.filter(lab=self.lab)[0].price

    def send_to_lab(self, lab):
        self.lab = lab
        self.to_lab = True
        self.from_lab = False
        self.save()
        return self.sending_cost()
        

    def save(self, *args, **kwargs):
        if not self.result:
            super(AnalysisTestInfo, self).save(*args, **kwargs)
            return
        patient = self.analysis.patient
        sex = patient.sex
        age = patient.get_age_in_days()
        for range in self.test.ranges.all():
            if not range.sex == sex:
                continue
            min_age, max_age = range.get_age_range_in_days()
            if (min_age <= age <= max_age) and (range.range_from <= self.result <= range.range_to):
                super(AnalysisTestInfo, self).save(*args, **kwargs)
                break
        else:
            raise forms.ValidationError("Invalid range")

        def __unicode__(self):
            return self.test.name
    
class Analysis(models.Model):
        physician = models.ForeignKey(Physician, null=True, blank=True)
        patient = models.ForeignKey(Patient, related_name="analysis")
        fast_hours_count = models.IntegerField(default=0, null=False, blank=False, validators=[MinValueValidator(0), MaxValueValidator(24)])
        x_ray_dye = models.BooleanField(default=False)
        delivered = models.BooleanField(default=False)
        date_created = models.DateField(auto_now_add=True)
        
        def cost(self):
            cost = 0.0
            for test in self.tests:
                cost += test.cost()
            return cost

        def __unicode__(self):
            return "%s" % self.patient.name
