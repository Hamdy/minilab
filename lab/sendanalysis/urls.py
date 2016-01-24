from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^show_analysises', 'sendanalysis.views.show_analysises', name='show_analysises'),
    url(r'^send_analysis', 'sendanalysis.views.send', name='send_analysis'),
    url(r'^report/sent', 'sendanalysis.views.report', name='send_analysis_report'),
    url(r'^confirm_send_analysis', 'sendanalysis.views.confirm_send', name='confirm_send_analysis'),

)
