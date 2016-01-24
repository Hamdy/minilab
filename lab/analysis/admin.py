from django.contrib import admin
from models import Analysis
from models import AnalysisTestInfo

class AnalysisTestInfoAdmin(admin.ModelAdmin):
    model = AnalysisTestInfo
    
class AnalysisAdmin(admin.ModelAdmin):
    model = Analysis

admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(AnalysisTestInfo, AnalysisTestInfoAdmin)