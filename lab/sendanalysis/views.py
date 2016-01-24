from analysis.models import Analysis, AnalysisTestInfo
import datetime
from django.shortcuts import render, get_object_or_404
from sendanalysis.forms import ShowAnalysisesForm
from medicaltest.models import OtherLabs
from django.http import HttpResponseNotAllowed
from sendanalysis.models import Report, LabTests
def report(request):
    pass

def confirm_send(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['GET'])
    tests = request.POST.getlist('tests')
    tests = AnalysisTestInfo.objects.filter(id__in=tests)
    lab = get_object_or_404(OtherLabs, pk=request.POST.get('lab'))

    total = 0.0    
    for test in tests:
        total += test.send_to_lab(lab)
    
    import pdb;pdb.set_trace()
    if tests:
        today = datetime.date.today()
        try:
            report = Report.objects.get(date=today)
            try:
                lab_tests = report.labs_tests.get(lab=lab)
            except LabTests.DoesNotExist:
                lab_tests = LabTests.objects.create(lab=lab, report=report)
            
        except Report.DoesNotExist:
            report = Report.objects.create(date=today)
            lab_tests = LabTests.objects.create(lab=lab, report=report)
            
        lab_tests.tests.add(*tests)
    
    return render(request, 'report.html', {'tests': tests, 'total':total})
    
def send(request):
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['GET'])
    tests = request.POST.getlist('tests')
    tests = AnalysisTestInfo.objects.filter(id__in=tests)
    lab = get_object_or_404(OtherLabs, pk=request.POST.get('lab'))
    return render(request, 'confirm_send.html', {'tests': tests, 'lab':lab})
    

def show_analysises(request):
    analysises = []
    if request.method == "GET":
        form = ShowAnalysisesForm()
    else:
        form = ShowAnalysisesForm(request.POST)
        if form.is_valid():
            type = form.cleaned_data.get('type')
            if type == 'today':
                today = datetime.date.today()
                analysises = Analysis.objects.filter(date_created=today)
                   
            elif type == 'yesterday':
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
                analysises = Analysis.objects.filter(date_created=yesterday)
                
            elif type == 'last_week':
                week_ago = datetime.date.today() - datetime.timedelta(days=7)
                analysises = Analysis.objects.filter(date_created__gte=week_ago)
    labs = OtherLabs.objects.all()
    return render(request, 'show_analysises.html', {'labs':labs, 'analysises':analysises,'form':form})