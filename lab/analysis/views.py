# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from models import Analysis
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from forms import AddAnalysisForm
from patient.models import Patient
from medicaltest.models import TestGroup, OtherLabs
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound
import json
from medicaltest.models import Test 
from analysis.models import AnalysisTestInfo
from inout.models import Income
import datetime
from django.db import transaction
# 
@login_required
def get_tests_cost(request):
     
    if not request.method == 'POST':
        return HttpResponseNotFound()
     
    tests = request.POST.get("tests").strip().split(",")
    type = request.POST.get("type").strip()
    paid = 0.0
    try:
        paid = int(request.POST.get("paid").strip())
    except:
        pass
     
    if not type in ["standalone", "from_physician", "from_lab"]:
        return HttpResponseNotFound()
         
    tests_ids = []
    for test in tests:
        if test.isdigit():
            tests_ids.append(test)
    res = Test.objects.filter(id__in=tests_ids)
    cost = 0.0
    for test in res:
        if type == "from_lab":
            cost += test.receiving_price
        else:
            cost += test.price
    return HttpResponse(json.dumps({'cost':cost, 'remaining':cost-paid}), mimetype='application/json')
 
@login_required
def get_testgroup_tests(request, TestGroup_id='all'):
    tests = {}
    if TestGroup_id == 'all':
        for test in Test.objects.all():
            tests[test.name] = test.id
    elif not TestGroup_id.isdigit():
        return HttpResponseForbidden()
    else:
        TestGroup = get_object_or_404(TestGroup, pk=TestGroup_id)
     
        for test in TestGroup.tests.all():
            tests[test.name] = test.id
    return HttpResponse(json.dumps(tests), mimetype='application/json')
 
 
@login_required
def add(request, patient_id):
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method == 'GET':
        form = AddAnalysisForm()
    else:
        post_data = request.POST.copy()
        post_data['patient'] = patient.id
        form = AddAnalysisForm(post_data)
        if form.is_valid():
            with transaction.commit_on_success():
                tests = Test.objects.filter(id__in=form.cleaned_data['tests'])
                labs = form.cleaned_data['labs']
                analysis = form.save()
                patient.analysis.add(analysis)
                infos =[]
                for i, test in enumerate(tests):
                    info = AnalysisTestInfo()
                    info.analysis = analysis
                    info.test = test
                    if labs[i]  != '0':
                        info.lab = OtherLabs.objects.get(pk=labs[i])
                        info.from_lab = True
                    infos.append(info)
                AnalysisTestInfo.objects.bulk_create(infos)
                Income.objects.create(analysis=analysis)

            return HttpResponseRedirect(reverse('list_analysis'))
    return render(request, 'add_edit_analysis.html', {'form':form,
        'patient_name':patient.name, 'tests':Test.objects.all(), 'labs':OtherLabs.objects.all()})
 
@login_required
def analysis(request, patient_id=0, patient_name='', status=''):
    if request.method == 'POST' and request.POST.get('patient_name'):
        patient_name = request.POST.get('patient_name')
    if patient_id:
        analysis = Analysis.objects.filter(patient__id=patient_id).order_by('-date_created')
        if status and status == 'all':
            analysis = Analysis.objects.filter(patient__id=patient_id).order_by('delivered')
        elif status and status == 'delivered':
            analysis = analysis.filter(delivered=True)
        else:
            return HttpResponseNotFound()
    elif patient_name:
        analysis = Analysis.objects.filter(patient__name__contains=patient_name).order_by('-date_created')
         
    else:
        analysis = Analysis.objects.order_by('-date_created')
    return render(request, 'list_analysis.html', {'analysis':analysis})
 
@user_passes_test(lambda u: u.is_superuser)
def confirm_delete(request, id=0):
    analysis = get_object_or_404(Analysis, pk=id)
    analysis.delete()
    return HttpResponseRedirect(reverse('list_analysis'))
 
@user_passes_test(lambda u: u.is_superuser)
def delete(request, id=0):
    analysis = get_object_or_404(Analysis, pk=id)
    return render(request, 'delete_analysis.html', {'analysis':analysis})
 
@login_required
def edit(request, id=0):
    analysis = get_object_or_404(Analysis, pk=id)
    if request.method == 'GET':
        form = AddAnalysisForm(instance=analysis)
    else:
        old_cost = analysis.paid
        post_data = request.POST.copy()
        post_data['patient'] = analysis.patient.id
        form = AddAnalysisForm(post_data, instance=analysis)
        if form.is_valid():
            new_cost = post_data.get('paid')
            Income.objects.get(date=datetime.date.today()).update(income=new_cost-old_cost)
            form.save()
             
            return HttpResponseRedirect(reverse('list_analysis'))
    return render(request, 'add_edit_analysis.html', {'form':form, 'patient_name':analysis.patient.name})
 
def add_result(request, analysis_id):
    analysis = get_object_or_404(Analysis, pk=analysis_id)
    tests = analysis.tests.all()
    errors = {}
    if request.method == "GET":
        return render(request, 'add_result.html', {'tests':tests, 'patient': analysis.patient, 'erros':errors})
    else:
         
        for test in tests:
            value = request.POST.get(test.name, '0')
            test.value = value if value else '0'
            try:
                int(value)
                value = float(value)
            except ValueError:
                errors[test.name] = "من فضلك ادخل ارقام"
                break
            try:
                AnalysisTestInfo.objects.create(test=test, analysis=analysis, result=value)
            except:
                errors[test.name] = "من فضلك ادخل قيمة صحيحة لهذا التحليل"
                break
                       
        else:
            return HttpResponseRedirect(reverse('home'))
        return render(request, 'add_result.html', {'tests':tests, 'patient': analysis.patient, 'errors':errors})
 
@login_required
@user_passes_test(lambda u: u.is_superuser)
def Analysis_reports(request, id=0):
    Analysis = get_object_or_404(Analysis, pk=id)
    return render(request, 'Analysis_reports.html', {})
