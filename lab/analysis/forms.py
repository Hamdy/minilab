# -*- coding: utf-8 -*-
from django import forms
from models import Analysis, AnalysisTestInfo
from physician.models import Physician
from medicaltest.models import TestGroup, Test
from django.forms.models import BaseInlineFormSet
from django.contrib.admin.widgets import FilteredSelectMultiple
         
class AddAnalysisTestInfoForm(forms.ModelForm):
    class Meta:
        model = AnalysisTestInfo
     
    def clean(self):
        analysis = self.cleaned_data.get('analysis')
        test= self.cleaned_data.get('test')
        if analysis and test and test not in analysis.tests.all():
            raise forms.ValidationError("هذا التحليل غير موجود بالفحص")
        return self.cleaned_data
 
class CategoriesField(forms.ModelMultipleChoiceField):
    def __init__(self, queryset, **kwargs):
        super(forms.ModelMultipleChoiceField, self).__init__(queryset, **kwargs)
        self.queryset = queryset.select_related()
        self.to_field_name=None

        group = None
        list = []
        self.choices = []

        for category in queryset:
            if not group:
                group = category.group

            if group != category.group:
                self.choices.append((group.name, list))
                group = category.group
                list = [(category.id, category.name)]
            else:
                list.append((category.id, category.name))
        try:
            self.choices.append((group.name, tuple(list)))
        except:
            pass
        self.choices = tuple(self.choices)
class AddAnalysisForm(forms.ModelForm):
    tests = forms.CharField(widget=forms.HiddenInput)
    labs = forms.CharField(widget=forms.HiddenInput)
    
    def clean_tests(self):
        tests = self.cleaned_data.get('tests').split(',')[:-1]
        return tests
    
    def clean_labs(self):
        labs = self.cleaned_data.get('labs').split(',')[:-1]
        return labs

    class Meta:
        model = Analysis
        exclude = ('delivered',)
