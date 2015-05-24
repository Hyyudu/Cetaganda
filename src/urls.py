from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^roles/', include('roles.urls')),
    url(r'^ulogin/', include('django_ulogin.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
