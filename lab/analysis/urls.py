from django.conf.urls import patterns, url
# 
urlpatterns = patterns('',
    url(r'^add/(?P<patient_id>\d+)/$', 'analysis.views.add', name='add_analysis'),
    url(r'^group/tests/(?P<group_id>\w+)/$', 'analysis.views.get_testgroup_tests', name='get_group_tests'),
    url(r'^analysis/tests/get_cost/$', 'analysis.views.get_tests_cost', name='get_tests_cost'),
 
    url(r'^delete/(?P<id>\d+)/$', 'analysis.views.delete', name='delete_analysis'),
    url(r'^delete_confirm/(?P<id>\d+)/$', 'analysis.views.confirm_delete', name='confirm_delete_analysis'),
 
    url(r'^edit/(?P<id>\d+)/$', 'analysis.views.edit', name='edit_analysis'),
    url(r'^analysis/$', 'analysis.views.analysis', name='list_analysis'),
    url(r'^analysis/(?P<patient_id>\d+)/$', 'analysis.views.analysis', name='list_analysis'),
    url(r'^analysis/(?P<patient_name>\w+)/$', 'analysis.views.analysis', name='list_analysis'),
    url(r'^analysis/(?P<patient_id>\d+)/(?P<status>\w+)/$', 'analysis.views.analysis', name='list_analysis'),
    url(r'^result/add/(?P<analysis_id>\d+)/$', 'analysis.views.add_result', name='add_result'),
 
#     url(r'^reports/(?P<id>\d+)/$', 'analysis.views.analysis_reports', name='panalysis_reports'),
)
