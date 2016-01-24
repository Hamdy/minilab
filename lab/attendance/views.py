# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance.models import Attendance
from datetime import datetime
from django.http.response import HttpResponse, HttpResponseRedirect


def _attended(user):
    records = Attendance.objects.filter(user__username=user.username)
    if records:
        last_record = records[0]
        today = datetime.today().date()
        if today == last_record.attendance.date():
            return True
    return False

def _departed(user):
    records = Attendance.objects.filter(user__username=user.username)
    if records:
        last_record = records[0]
        today = datetime.today().date()
        if last_record.departure and today == last_record.departure.date():
            return True
    return False

@login_required
def attend(request):
    if request.method != 'POST' or _attended(request.user):
        return HttpResponse(status=204)
    attendance = Attendance(user=request.user)
    attendance.attendance = datetime.now()
    attendance.save()
    return HttpResponseRedirect('/')

@login_required
def depart(request):
    if request.method != 'POST' or _departed(request.user) or not _attended(request.user):
        return HttpResponse(status=204)
    
    record = Attendance.objects.filter(user__username=request.user.username)[0]
    record.departure = datetime.now()
    record.save()
    return HttpResponseRedirect('/')

@login_required
def add_patient(request):
    pass
