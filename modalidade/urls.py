# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('modalidade.views',
                       
    url(r'^(?P<modalidade_id>\d+)/$', 'modalidade', name='modalidade'),
    url(r'^create/$', 'create', name='create'),
    url(r'^save/$', 'save', name='save'),

)

