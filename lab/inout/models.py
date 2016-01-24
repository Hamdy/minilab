from django.db import models
from analysis.models import Analysis, AnalysisTestInfo

class Expenses(models.Model):
    date = models.DateField()
    test_info = models.ForeignKey(AnalysisTestInfo)
    
    @property
    def expenses(self):
        return self.test_info.sending_cost()
    
    def __unicode__(self):
        return str(self.date)

class Income(models.Model):
    analysis = models.ForeignKey(Analysis)
    date = models.DateField(auto_now_add=True)
    
    @property
    def income(self):
        return self.analysis.cost()    
    
    def __unicode__(self):
        return str(self.date)