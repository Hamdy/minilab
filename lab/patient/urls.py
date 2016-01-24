from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^add', 'patient.views.add', name='add_patient'),
    url(r'^delete/(?P<id>\d+)/$', 'patient.views.delete', name='delete_patient'),
    url(r'^delete_confirm/(?P<id>\d+)/$', 'patient.views.confirm_delete', name='confirm_delete_patient'),
    url(r'^edit/(?P<id>\d+)/$', 'patient.views.edit', name='edit_patient'),
    url(r'^patients/$', 'patient.views.patients', name='list_patients'),
    url(r'^patients/(?P<param>\w+)/$', 'patient.views.patients', name='list_patients'),
    url(r'^reports/(?P<id>\d+)/$', 'patient.views.patient_reports', name='patient_reports'),
)
