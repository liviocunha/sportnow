# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('allauth.urls')),
    url(r'^dashboard/(\d+)/$', 'core.views.logado', name='logado'),
    url(r'^termos$', 'core.views.termos', name='termos'),
    url(r'^futebol/', include('futebol.urls')),
    url(r'^modalidade/(?P<modalidade_id>\d+)/$', 'modalidade', name='modalidade'),
    url(r'^modalidade/', include('modalidade.urls')),
    url(r'^$', 'core.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_URL)


