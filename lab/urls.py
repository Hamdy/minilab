from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('attendance.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('django.contrib.auth.urls')),
    url(r'', include('home.urls')),
    url(r'^physician/', include('physician.urls')),
    url(r'^patient/', include('patient.urls')),
    url(r'^test/', include('medicaltest.urls')),
    url(r'^analysis/', include('analysis.urls')),
    url(r'^', include('inout.urls')),
    url(r'^', include('sendanalysis.urls')),
    url(r'^', include('account.urls')),
    url(r'^lab/', include('medicallab.urls', namespace='lab')),

)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += staticfiles_urlpatterns(settings.MEDIA_URL)