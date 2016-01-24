# -*- coding: utf-8 -*-
from django import forms
class InOutForm(forms.Form):
    TYPE_CHOICES = (('today', 'اليوم'),
                    ('yesterday', 'الأمس'),
                    ('last_week', 'الاسبوع المنصرم'),
                    ('last_month', 'الشهر المنصرم'),
                    ('last_year', 'السنة المنصرمة'),
                    ('range', 'مدى'))
    
    type = forms.CharField(max_length=10, widget=forms.RadioSelect(choices=TYPE_CHOICES), initial='today')
    start = forms.DateField(required=False)
    end = forms.DateField(required=False)
    
    def clean(self):
        cleaned = self.cleaned_data
        type = cleaned.get('type')
        start = cleaned.get('start')
        end = cleaned.get('end')
        
        if type and type == 'range':
            if not start or not end:
                raise forms.ValidationError("من فضلك قم باختيار مدى من الايام")
        return cleaned

    