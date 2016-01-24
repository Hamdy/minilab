from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^add', 'physician.views.add', name='add_physician'),
    url(r'^delete/(?P<id>\d+)/$', 'physician.views.delete', name='delete_physician'),
    url(r'^delete_confirm/(?P<id>\d+)/$', 'physician.views.confirm_delete', name='confirm_delete_physician'),
    url(r'^edit/(?P<id>\d+)/$', 'physician.views.edit', name='edit_physician'),
    url(r'^physicians/$', 'physician.views.physician', name='list_physician'),
    url(r'^physicians/(?P<param>\w+)/$', 'physician.views.physician', name='list_physician'),
    url(r'^reports/(?P<id>\d+)/$', 'physician.views.physician_reports', name='physician_reports'),
)
