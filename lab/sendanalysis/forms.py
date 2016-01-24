# -*- coding: utf-8 -*-
from django import forms
class ShowAnalysisesForm(forms.Form):
    TYPE_CHOICES = (('today', 'اليوم'),
                    ('yesterday', 'الأمس'),
                    ('last_week', 'الاسبوع المنصرم'))
    
    type = forms.CharField(max_length=10, widget=forms.RadioSelect(choices=TYPE_CHOICES), initial='today')
    