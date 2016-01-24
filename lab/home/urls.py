from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'home.views.home', name='home'),
    url(r'^admin_home', 'home.views.home_admin', name='admin_home'),
)
