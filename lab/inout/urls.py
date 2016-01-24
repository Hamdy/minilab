from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^inout', 'inout.views.inout', name='inout'),
    
)
