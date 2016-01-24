from django.shortcuts import render
from datetime import datetime
from attendance.models import Attendance
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse

@login_required
def home_admin(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    
    return render(request, 'home_admin.html', {})
    
@login_required
def home(request):
    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('home.views.home_admin'))
    today = datetime.today().date()
    records = Attendance.objects.filter(user=request.user, attendance__month=today.month)
    data = {'records':records, 'attended':False, 'departed':False}
    if records:
        last_record = records[0]
        if today == last_record.attendance.date():
            data['attended'] = True
        if last_record.departure and today == last_record.departure.date():
            data['departed'] = True
    return render(request, 'home.html', data)
