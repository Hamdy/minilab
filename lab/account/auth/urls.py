from django.conf.urls import patterns, url

from views import login, password_reset

urlpatterns = patterns('',
    url(r'^accounts/login/$', login, name='auth_login'),
    url(r'^accounts/password_reset/$', password_reset, name='auth_password_reset'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/signup/$', 'account.views.register', name='register'),
    url(r'^message/$', 'account.views.message', name='message'),
    url(r'^activate/(?P<token>\w+)/$', 'account.views.activate', name='activate'),
    url(r'^resend_activation/$', 'account.views.resend_activation', name='resend_activation'),

)
