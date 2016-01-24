from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^create/$', 'medicallab.views.update_create', name='create'),
    url(r'^update/(?P<id>\d+)/$', 'medicallab.views.update_create', name='update'),
    url(r'^profile/(?P<id>\d+)/$', 'medicallab.views.profile', name='profile'),

)
