from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^attend/$', 'attendance.views.attend', name='attend'),
    url(r'^depart/$', 'attendance.views.depart', name='depart')
    
)
