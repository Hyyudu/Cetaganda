from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^ulogin/', include('django_ulogin.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^redactor/', include('redactor.urls')),

    url(r'^', include('roles.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
