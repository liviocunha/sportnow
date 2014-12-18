# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import BuscaajaxView, BuscarajaxView, searchAJAX, Buscarcomentario

admin.autodiscover()

urlpatterns = patterns('futebol.views',

    url(r'^$', 'futebol', name='futebol'),

    url(r'^tipos/$', 'tiposFutebol', name='tiposFutebol'),
    url(r'^postar/$', 'postar', name='postar'), 
                
    #partidas    
    url(r'^partidas/iniciadas/$', 'partidasIniciadas', name='partidasIniciadas'),
    url(r'^partidas/escolhaequipes/$', 'escolhaEquipes', name='escolhaEquipes'),
    url(r'^partidas/new/$', 'newPartidas', name='newPartidas'),
    url(r'^partidas/newteste/$', 'newPartidasTESTE', name='newPartidasTESTE'),
    url(r'^partidas/teste/$', 'testePartidas', name='testePartidas'),
    url(r'^partidas/save/$', 'savePartidas', name='savePartidas'),
    url(r'^partidas/iniciar/(?P<pk>\d+)/$', 'iniciarPartida', name='iniciarPartida'),
    url(r'^partidas/comentario/(?P<pk>\d+)/(?P<par>\d+)/$', 'comentarioPartida', name='comentarioPartida'),
    url(r'^partidas/postar/$', 'postarComentarioF', name='postarComentarioF'),
    url(r'^partidas/encerrar/(?P<pk>\d+)/$', 'partidaEncerrar', name='partidaEncerrar'),

    #auxiliares       
    url(r'^buscaajax/$', BuscaajaxView.as_view()),
    url(r'^buscarajax/$', BuscarajaxView.as_view()),
    
    #ações comentarios
    url(r'^comentarios/$', 'homeComentariosCat', name='homeComentariosCat'),
    #url(r'^comentarios/home$', 'homeComentarios', name='homeComentarios'),
    #url(r'^comentarios/tipo$', 'tipoComentarios', name='tipoComentarios'),
    url(r'^comentarios/list/(?P<pk>\d+)/$', 'listComentarios', name='listComentarios'),
    url(r'^comentarios/listdetail$', 'listdetailComentarios', name='listdetailComentarios'),
    url(r'^comentarios/new$', 'newComentarios', name='newComentarios'),
    url(r'^comentarios/escolha$', 'escolhaCategoria', name='escolhaCategoria'),
    url(r'^comentarios/save$', 'saveComentarios', name='saveComentarios'),
    #url(r'^comentarios/search$', 'searchComentarios', name='searchComentarios'),
    #url(r'^comentarios/searchAJAX$', searchAJAX.as_view()),
    url(r'^buscarcomentarios/$', Buscarcomentario.as_view()),
    url(r'^comentarios/edit/(?P<pk>\d+)/$', 'editComentarios', name='editComentarios'),
    url(r'^comentarios/del/(?P<pk>\d+)/$', 'delComentarios', name='delComentarios'),

    #ações categoria comentarios
    url(r'^categorias/$', 'listCategorias', name='listCategorias'),
    url(r'^categorias/new$', 'newCategorias', name='newCategorias'),
    url(r'^categorias/save$', 'saveCategorias', name='saveCategorias'),
    url(r'^categorias/edit/(?P<pk>\d+)/$', 'editCategorias', name='editCategorias'),
    url(r'^categorias/del/(?P<pk>\d+)/$', 'delCategorias', name='delCategorias'),

    #ações equipes
    url(r'^equipes/$', 'listEquipes', name='listEquipes'),
    url(r'^equipes/new$', 'newEquipes', name='newEquipes'),
    url(r'^equipes/ajax$', 'entry_index', name='entry_index'),
    url(r'^equipes/save$', 'saveEquipes', name='saveEquipes'),
    url(r'^equipes/edit/(?P<pk>\d+)/$', 'editEquipes', name='editEquipes'),
    url(r'^equipes/del/(?P<pk>\d+)/$', 'delEquipes', name='delEquipes'),

    #ações jogadores
    url(r'^jogadores/(?P<pk>\d+)/$', 'listJogadores', name='listJogadores'),
    url(r'^jogadores/new/(?P<pk>\d+)/$', 'newJogadores', name='newJogadores'),
    url(r'^jogadores/save$', 'saveJogadores', name='saveJogadores'),
    url(r'^jogadores/edit/(?P<pk>\d+)/$', 'editJogadores', name='editJogadores'),
    url(r'^jogadores/del/(?P<pk>\d+)/$', 'delJogadores', name='delJogadores'),

)
