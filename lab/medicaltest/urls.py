from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^tests/$', 'medicaltest.views.tests', name='list_tests'),
    url(r'^tests/(?P<param>\w+)/$', 'medicaltest.views.tests', name='list_tests'),
    url(r'^add', 'medicaltest.views.add', name='add_test'),
    url(r'^delete/(?P<id>\d+)/$', 'medicaltest.views.delete', name='delete_test'),
    url(r'^delete_confirm/(?P<id>\d+)/$', 'medicaltest.views.confirm_delete', name='confirm_delete_test'),
    url(r'^edit/(?P<id>\d+)/$', 'medicaltest.views.edit', name='edit_test'),

)
