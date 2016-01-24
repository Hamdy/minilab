# -*- coding: utf-8 -*-
from django import forms
from models import Test

class AddTestForm(forms.ModelForm):
    class Meta:
        model = Test
        
    def clean_sending_prices(self):
        lab_name_count = {}
        
        sending_prices = self.cleaned_data.get('sending_prices', [])
        for record in sending_prices:
            lab_name_count[record.lab.name] = lab_name_count.get(record.lab.name, 0) + 1
        for v in lab_name_count.values():
            if v > 1:
                raise forms.ValidationError("لا يمكن وضع أكثر من سعر لنفس المعمل")
        return sending_prices
    
    def clean_ranges(self):
        ranges_counts = {}
        ranges = self.cleaned_data.get('ranges', [])
        for range in ranges:
            ranges_counts[repr(range)] = ranges_counts.get(repr(range), 0) + 1
        for e in ranges_counts.values():
            if e > 1:
                raise forms.ValidationError("لا يمكن وضع أكثر من مدى لنفس الفئة العمرية لنفس النوع")
        return ranges
    