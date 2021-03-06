from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^articles/', include('staticpages.urls')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^guestbook/', include('guestbook.urls', namespace='guestbook')),
    url(r'^hack/', include('hack.urls', namespace='hack')),
    url(r'^market/', include('market.urls', namespace='market')),
    url(r'^news/', include('news.urls')),
    url(r'^redactor/', include('redactor.urls')),
    url(r'^register/', include('register.urls', namespace='register')),
    url(r'^roles/', include('roles.urls', namespace='roles')),
    url(r'^science/', include('science.urls', namespace='science')),
    url(r'^space/', include('space.urls', namespace='space')),
    url(r'^ulogin/', include('django_ulogin.urls')),
    url(r'^users/', include('users.urls', namespace='users')),

    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
