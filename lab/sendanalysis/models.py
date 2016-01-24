from django.db import models
from analysis.models import AnalysisTestInfo
from medicaltest.models import OtherLabs

class LabTests(models.Model):
    tests = models.ManyToManyField(AnalysisTestInfo)
    lab = models.ForeignKey(OtherLabs)
    report = models.ForeignKey('Report', related_name='labs_tests')

class Report(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)
    