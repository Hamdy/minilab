from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^register/$', 'account.views.register', name='register'),
    url(r'^message/$', 'account.views.message', name='message'),
    url(r'^activate/(?P<token>\w+)/$', 'account.views.activate', name='activate'),
    url(r'^resend_activation/$', 'account.views.resend_activation', name='resend_activation'),
    
    
)
