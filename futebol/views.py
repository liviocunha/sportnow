# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken, SocialAccount
from futebol.models import *
from core.models import *
from futebol.forms import *
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.utils import timezone
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Q #Queries complexas
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from endless_pagination.decorators import page_template
import facebook
from authomatic import Authomatic

from core.config import CONFIG
authomatic = Authomatic(CONFIG, 'a super secret random string')

def tiposFutebol(request):    
    return render(request, 'futebol/tipos.html')

@login_required
def postar(request):
    facebook = 0    
    twitter = 1    
    inicio = request.POST['id']
    comentario = request.POST['comentario']
    
    user_validar = SocialAccount.objects.get(user_id=request.user.id)
    user_validar_id = (user_validar.id)
    #print user_validar_id
    #print "user, OK"
    user_social = SocialToken.objects.get(pk=user_validar_id)
    
    #print user_social
    #print "provider"        


    if facebook == 1:
        a = SocialAccount.objects.get(user_id=request.user.id)
        b = (a.id)
        teste = SocialToken.objects.get(pk=b)
        mensagem = comentario
        graph = facebook.GraphAPI(teste.token)
        graph.put_object('me', 'feed', message=mensagem)
        #success = "success: FB"
        #print mensagem+success

    if twitter == 1:
        mensagem = comentario
        a = SocialAccount.objects.get(user_id=request.user.id)
        b = (a.id)
        teste = SocialToken.objects.get(pk=b)
        serialized_credentials = '1%0A1-5%0A' + teste.token + '%0A' + teste.token_secret
        response = authomatic.access(serialized_credentials,
                                         url='https://api.twitter.com/1.1/statuses/update.json',
                                         params=dict(status=mensagem),
                                         method='POST')
        #success = "success: TW"
        #print mensagem+success


    return HttpResponseRedirect('/futebol/partidas/iniciar/'+str(inicio))

@login_required
def futebol(request):
    return render(request, 'futebol/futebol.html')

################################## PARTIDAS #################################################
@login_required
def testePartidas(request):
    form = PartidasForm()
    context = {'form': form}
    return render(request, 'futebol/testeFormPartidas.html', context)

@login_required
def partidaEncerrar(request, pk=0):
    partida = Partidas.objects.get(pk=pk)

    partida.status = '0'
    partida.save()

    return HttpResponseRedirect('/futebol/partidas/iniciadas')

@login_required
def partidasIniciadas(request):
    partidas = Partidas.objects.filter(user__id=request.user.id).order_by('status')
    partidas_iniciadas = partidas.filter(status=1).order_by('data')

    context = {'partidas_iniciadas': partidas_iniciadas}
    return render(request, 'futebol/partidas-iniciadas.html', context)

@login_required
def escolhaEquipes(request):
    equipes = Equipes.objects.filter(user__id=request.user.id)
    if equipes:
        context = {'equipes':equipes}
    else:
        msg = "Não há equipes."
        context = {'msg':msg}
    
    return render(request, 'futebol/partida-equipes.html', context)

@login_required
def newPartidas(request):
    casa = request.POST['casa']
    casa = Equipes.objects.get(pk=casa)
    visitante = request.POST['visitante']
    visitante = Equipes.objects.get(pk=visitante)

    form = PartidasForm()
    context = {'form': form, 'casa':casa, 'visitante':visitante}
    return render(request, 'futebol/formPartidas.html', context)

@login_required
def newPartidasTESTE(request):

    form = PartidasForm()
    context = {'form': form}
    return render(request, 'futebol/formPartidas2.html', context)

@login_required
def iniciarPartida(request, pk=0):
    partida = Partidas.objects.get(pk=pk)
    casa = Equipes.objects.get(pk=partida.id_casa)
    visitante = Equipes.objects.get(pk=partida.id_visitante)
    categorias = CategoriaComentarios.objects.filter(user=request.user.id)
    context = {'partida': partida, 'casa':casa, 'visitante':visitante, 'categorias':categorias}

    return render(request, 'futebol/dashboardPartida.html', context)


@login_required
def savePartidas(request, pk=0):
    if request.method == 'POST':
        try:
            partida = Partidas.objects.get(pk=request.POST.get('id','0'))
            form = PartidasForm(request.POST, instance=partida)
        except:
            form = PartidasForm(request.POST)
            id_casa = request.POST['id_casa']
            casa = Equipes.objects.get(pk=id_casa)
            id_visitante = request.POST['id_visitante']
            visitante = Equipes.objects.get(pk=id_visitante)

        if form.is_valid():
            partida = form.save()
            inicio = partida.pk
            return HttpResponseRedirect('/futebol/partidas/iniciar/'+str(inicio))
        else:
            context = {'form': form, 'casa':casa, 'visitante':visitante}
            return render(request, 'futebol/formPartidas.html', context)
    else:
        return HttpResponseRedirect('/futebol/')

@login_required
def comentarioPartida(request, pk=0, par=0):
    comentario = Comentarios.objects.get(pk=pk)
    partida = Partidas.objects.get(pk=par)
    casa = Equipes.objects.get(pk=partida.id_casa)
    #print partida.id_casa
    visitante = Equipes.objects.get(pk=partida.id_visitante)
    jogadorescasa = Jogadores.objects.filter(equipe__id=casa.pk)
    jogadoresvisitante = Jogadores.objects.filter(equipe__id=visitante.pk)
    inicio = partida.pk
    #print jogadorescasa

    if comentario.tipo == 'SC':
        tipo = "SC"
        context = {'comentario':comentario, 'tipo':tipo, 'partida':partida }

    elif comentario.tipo == 'SE':
        tipo = comentario.tipo 
        context = {'comentario':comentario, 'tipo':tipo, 'partida':partida, 'casa':casa, 'visitante':visitante }

    elif comentario.tipo == 'EE':
        tipo = comentario.tipo 
        context = {'comentario':comentario, 'tipo':tipo, 'partida':partida, 'casa':casa, 'visitante':visitante }

    elif comentario.tipo == 'EJ':
        tipo = comentario.tipo 
        context = {'comentario':comentario, 'tipo':tipo, 'partida':partida, 'casa':casa, 'visitante':visitante, 'jogadorescasa':jogadorescasa, 'jogadoresvisitante':jogadoresvisitante}

    elif comentario.tipo == 'SJ':
        tipo = comentario.tipo 
        context = {'comentario':comentario, 'tipo':tipo, 'partida':partida, 'casa':casa, 'visitante':visitante,'jogadorescasa':jogadorescasa, 'jogadoresvisitante':jogadoresvisitante}

    elif comentario.tipo == 'JJ':
        tipo = comentario.tipo 
        context = {'comentario':comentario, 'tipo':tipo, 'partida':partida, 'casa':casa, 'visitante':visitante, 'jogadorescasa':jogadorescasa, 'jogadoresvisitante':jogadoresvisitante}


    return render(request, 'futebol/formComentarioPartida.html', context)


@login_required
def postarComentarioF(request):

    partida_id = request.POST['partida_id']
    partida = Partidas.objects.get(pk=partida_id)


    comentario_id = request.POST['comentario_id']
    comentario = Comentarios.objects.get(pk=comentario_id)
    tempo = request.POST['tempo-choice']
    minuto = request.POST['minuto']
    desc = request.POST['desc']
    momento =  minuto+"'- "+tempo+" |"
    #print momento

    if comentario.tipo == 'SC':
        comentario_pronto = momento+desc
        #print comentario_pronto
        context = {'comentario_pronto':comentario_pronto, 'partida':partida}

    elif comentario.tipo == 'SE':
        equipe01 = request.POST['radio-SE']
        equipe = Equipes.objects.get(pk=equipe01)
        display = equipe.display
        print display
        desc = desc.split()      

        #altera {Equipe01} para equipe1
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Equipe01}":
                desc.pop(i)
                desc.insert(i, display)
                break

        #momento = "03' 2º T | "
        str = " "
        str1 = str.join(desc)
        comentario_pronto = momento+str1
        #print comentario_pronto        
        context = {'comentario_pronto':comentario_pronto, 'partida':partida}

    elif comentario.tipo == 'EE':
        equipe01 = request.POST['radio-EE-E1']
        equipecasa = Equipes.objects.get(pk=equipe01)

        equipe02 = request.POST['radio-EE-E2']
        equipevisitante = Equipes.objects.get(pk=equipe02)

        displayec = equipecasa.display
        displayev = equipevisitante.display
        
        desc = desc.split()  

        #altera {Equipe01} para equipe1
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Equipe01}":
                desc.pop(i)
                desc.insert(i, displayec)
                break

        str = " "
        str1 = str.join(desc)
        desc = str1.split() 

        #altera {Equipe02} para equipe1
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Equipe02}":
                desc.pop(i)
                desc.insert(i, displayev)
                break

        
        str = " "
        str1 = str.join(desc)
        comentario_pronto = momento+str1
        #print comentario_pronto        
        context = {'comentario_pronto':comentario_pronto, 'partida':partida}

    elif comentario.tipo == 'EJ':
        equipe01 = request.POST['radio-EJ-E1']
        equipe = Equipes.objects.get(pk=equipe01)
        displaye = equipe.display


        jogador1 = request.POST['select-EJ-J1']
        jogador = Jogadores.objects.get(pk=jogador1)
        displayj = jogador.display


        desc = desc.split()  

        #altera {Equipe01} para equipe01
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Equipe01}":
                desc.pop(i)
                desc.insert(i, displaye)
                break

        str9 = " "
        str10 = str9.join(desc)

        desc = str10.split() 

        #altera {Jogador1} para jogador
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Jogador1}":
                desc.pop(i)
                desc.insert(i, displayj)
                break

        str3 = " "
        str2 = str3.join(desc)
        comentario_pronto = momento+str2
        #print comentario_pronto        
        context = {'comentario_pronto':comentario_pronto, 'partida':partida}

    elif comentario.tipo == 'SJ':
        jogador1 = request.POST['select-SJ-J1']
        jogador = Jogadores.objects.get(pk=jogador1)
        display = jogador.display
        print display
        desc = desc.split()      

        #altera {Jogador1} para equipe1
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Jogador1}":
                desc.pop(i)
                desc.insert(i, display)
                break

        #momento = "03' 2º T | "
        str = " "
        str1 = str.join(desc)
        comentario_pronto = momento+str1
        #print comentario_pronto        
        context = {'comentario_pronto':comentario_pronto, 'partida':partida}

    elif comentario.tipo == 'JJ':
        jogador1 = request.POST['select-JJ-J1']
        jogador1ok = Jogadores.objects.get(pk=jogador1)

        jogador2 = request.POST['select-JJ-J2']
        jogador2ok = Jogadores.objects.get(pk=jogador2)

        displayec = jogador1ok.display
        displayev = jogador2ok.display
        
        desc = desc.split()  

        #altera {Jogador1} para jogador1ok
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Jogador1}":
                desc.pop(i)
                desc.insert(i, displayec)
                break

        str = " "
        str1 = str.join(desc)
        desc = str1.split() 

        #altera {Jogador2} para jogador2ok
        for i in range(len(desc)):
            palavra = desc[i]
            if palavra == "{Jogador2}":
                desc.pop(i)
                desc.insert(i, displayev)
                break

        
        str = " "
        str1 = str.join(desc)
        comentario_pronto = momento+str1
        #print comentario_pronto        
        context = {'comentario_pronto':comentario_pronto, 'partida':partida}


    return render(request, 'futebol/formConfirmaPublicacao.html', context)



################################## AUX AJAX #################################################
class Buscarcomentario(TemplateView):

    def get(self, request, *args, **kwargs):
        txtBusca = request.GET['text']
        cat = request.GET['cat']
        tipo = request.GET['tipo']

        comentarios = Comentarios.objects.filter(user__id=request.user.id).order_by('categoria')

        if cat != "0":
            comentarios = comentarios.filter(categoria=cat).order_by('tipo')
        if tipo != "all":
            comentarios = comentarios.filter(tipo=tipo).order_by('name')
        if txtBusca:
            comentarios = comentarios.filter((Q(name__contains=txtBusca) |Q(desc__contains=txtBusca))).order_by('name')

        data = serializers.serialize('json', comentarios, fields=('name', 'desc', 'tipo'))
        return HttpResponse(data, mimetype='application/json')

class BuscaajaxView(ListView):
    model = CategoriaComentarios
    template_name = 'futebol/examplebusca.html'
    context_object_name = 'autores'

class BuscarajaxView(TemplateView):

    def get(self, request, *args, **kwargs):
        tipo = request.GET['id']
        categoria = request.GET['cat']
        #print tipo
        #print categoria
        comentarios2 = Comentarios.objects.filter(categoria=categoria).order_by('tipo')

        if tipo == '1':
            comentarios = comentarios2.filter(tipo='SC').order_by('name')
            tipo = 'Somente Comentário'
            context ={'comentarios':comentarios, 'tipo':tipo}

        elif tipo == '2':
            comentarios = comentarios2.filter(tipo='ST').order_by('name')
            tipo = 'Somente 1 Time'
            context ={'comentarios':comentarios, 'tipo':tipo}

        elif tipo == '3':
            comentarios = comentarios2.filter(tipo='TT').order_by('name')
            tipo = 'Casa+Visitante'
            context ={'comentarios':comentarios, 'tipo':tipo}

        elif tipo == '4':
            comentarios = comentarios2.filter(tipo='TJ').order_by('name')
            tipo = 'Time+Jogador'
            context ={'comentarios':comentarios, 'tipo':tipo}

        elif tipo == '5':
            comentarios = comentarios2.filter(tipo='SJ').order_by('name')
            tipo = 'Somente 1 Jogador'
            context ={'comentarios':comentarios, 'tipo':tipo}
            
        elif tipo == '6':
            comentarios = comentarios2.filter(tipo='JJ').order_by('name')
            tipo = 'JogadorA+JogadorB'
            context ={'comentarios':comentarios, 'tipo':tipo}  

        print comentarios

        data = serializers.serialize('json', comentarios, fields=('name', 'desc', 'tipo'))
        return HttpResponse(data, mimetype='application/json')

################################## COMENTARIOS ###################################

@login_required
def homeComentariosCat(request):
    categorias = CategoriaComentarios.objects.filter(user__id=request.user.id)
    context = {'categorias':categorias}
    
    return render(request, 'futebol/comentarios.html', context)

@login_required
def escolhaCategoria(request):

    usuariologado = User.objects.get(id=request.user.id)
    categorias = CategoriaComentarios.objects.filter(user__id=usuariologado.pk)
    if categorias:
        context = {'categorias':categorias}
    else:
        msg = "Não há categorias."
        context = {'msg': msg}

    return render(request, 'futebol/formEscolhaCategoria.html', context)

@login_required
def newComentarios(request):
    categoria = CategoriaComentarios.objects.get(pk=request.POST.get('tipo'))

    form = ComentariosForm()
    return render(request, 'futebol/formComentario2.html', {'form': form, 'categoria':categoria})

@login_required
def saveComentarios(request, pk=0):
    if request.method == 'POST':
        try:
            comentario = Comentarios.objects.get(pk=request.POST.get('id','0'))
            form = ComentariosForm(request.POST, instance=comentario)
        except:
            form = ComentariosForm(request.POST)

        if form.is_valid():
            comentario = form.save()
            return HttpResponseRedirect('/futebol/')
        else:
            return render(request, 'futebol/formComentario.html', {'form': form})
    else:
        return HttpResponseRedirect('/futebol/')

@login_required
def delComentarios(request, pk=0):
    try:
        comentario = Comentarios.objects.get(pk=pk)
        comentario.delete()
        return HttpResponseRedirect('/futebol/comentarios/')
    except:
        return HttpResponseRedirect('/futebol/comentarios/')

@login_required
def searchComentarios(request):
    if request.method == 'POST':
        txtBusca = request.POST.get('txtBusca', '')
        try:
            if txtBusca == '':
                comentarios = Comentarios.objects.filter(user=request.user.id).order_by('name')
            else:
                query_comentarios = Comentarios.objects.filter(user=request.user.id).order_by('name')
                comentarios = query_comentarios.filter(
                (Q(name__contains=txtBusca) |
                Q(desc__contains=txtBusca))).order_by('name')
        except:
            comentarios = []
            #print comentarios

        return render(request, 'futebol/comentarios.html', {'comentarios':comentarios, 'txtBusca':txtBusca})

class searchAJAX(TemplateView):

    def get(self, request, *args, **kwargs):
        search = request.GET['q']

        comentarios = query_comentarios.filter((Q(name__contains=search))).order_by('name')

        #print comentarios

        data = serializers.serialize('json', comentarios, fields=('name', 'desc', 'tipo'))
        return HttpResponse(data, mimetype='application/json')

@login_required
def listComentarios(request, pk=0):

    usuariologado = User.objects.get(id=request.user.id)
    categoria = CategoriaComentarios.objects.get(pk=pk)

    usercategoria = categoria.user.pk
    userlogado = usuariologado.pk
    #validando o owner
    if usercategoria == userlogado:
        print 'Usuario-correto-comentarios'
        comentarios = Comentarios.objects.filter(categoria=pk).order_by('name')
        context = {'comentarios':comentarios, 'pk':pk, 'categoria':categoria}
    else:
        print 'Usuario-incorreto-comentarios'
        return HttpResponseRedirect('/futebol/comentarios/')

    return render(request, 'futebol/tipo-comentarios.html', context)

@login_required
def listdetailComentarios(request):

    if request.method == 'POST':

        idcategoria = request.POST.get('idCategoria','')        
        tipo = request.POST.get('tipo','')
        comentarios2 = Comentarios.objects.filter(categoria=idcategoria).order_by('tipo')

        if tipo == '1':
            comentarios = comentarios2.filter(tipo='SC').order_by('name')
            tipo = 'Somente Comentário'
            categoria = CategoriaComentarios.objects.get(pk=idcategoria)
            context ={'comentarios':comentarios, 'tipo':tipo, 'categoria':categoria}
        elif tipo == '2':
            comentarios = comentarios2.filter(tipo='ST').order_by('name')
            tipo = 'Somente 1 Time'
            categoria = CategoriaComentarios.objects.get(pk=idcategoria)
            context ={'comentarios':comentarios, 'tipo':tipo, 'categoria':categoria}
        elif tipo == '3':
            comentarios = comentarios2.filter(tipo='TT').order_by('name')
            tipo = 'Casa+Visitante'
            categoria = CategoriaComentarios.objects.get(pk=idcategoria)
            context ={'comentarios':comentarios, 'tipo':tipo, 'categoria':categoria}
        elif tipo == '4':
            comentarios = comentarios2.filter(tipo='TJ').order_by('name')
            tipo = 'Time+Jogador'
            categoria = CategoriaComentarios.objects.get(pk=idcategoria)
            context ={'comentarios':comentarios, 'tipo':tipo, 'categoria':categoria}
        elif tipo == '5':
            comentarios = comentarios2.filter(tipo='SJ').order_by('name')
            tipo = 'Somente 1 Jogador'
            categoria = CategoriaComentarios.objects.get(pk=idcategoria)
            context ={'comentarios':comentarios, 'tipo':tipo, 'categoria':categoria}
        elif tipo == '6':
            comentarios = comentarios2.filter(tipo='JJ').order_by('name')
            tipo = 'JogadorA+JogadorB'
            categoria = CategoriaComentarios.objects.get(pk=idcategoria)
            context ={'comentarios':comentarios, 'tipo':tipo, 'categoria':categoria}            


        return render(request, 'futebol/listComentarios.html', context)


@login_required
def editComentarios(request, pk=0):
    comentario = Comentarios.objects.get(pk=pk)
    categoria = comentario.categoria
    usuariologado = User.objects.get(id=request.user.id)    
    usercategoria = categoria.user
    owner = usercategoria.pk
    userlogado = usuariologado.pk
    try:
        
        #validando o owner
        if userlogado == owner:
            form = ComentariosForm(instance=comentario)
            print 'certo-comentario'
        else:
            print 'errado-comentario'
            return HttpResponseRedirect('/futebol/comentarios/')

    except:
        return HttpResponseRedirect('/futebol/comentarios/')

    return render(request, 'futebol/formComentario.html', {'form': form, 'categoria':categoria})

################################## CATEGORIAS COMENTARIOS ###################################

@login_required
def listCategorias(request):
    modalidade = 1
    usuario = User.objects.filter(id=request.user.id).order_by('id')
    categorias = CategoriaComentarios.objects.filter(user__id=usuario).order_by('name')
    context = {'categorias':categorias}    

    return render(request, 'futebol/listCategorias.html', context)

@login_required
def newCategorias(request):
    form = CategoriaForm()
    return render(request, 'futebol/formCategoria.html', {'form': form})

@login_required
def saveCategorias(request, pk=0):
    if request.method == 'POST':
        try:
            categoria = CategoriaComentarios.objects.get(pk=request.POST.get('id','0'))
            form = CategoriaForm(request.POST, instance=categoria)
        except:
            form = CategoriaForm(request.POST)

        if form.is_valid():
            categoria = form.save()
            return HttpResponseRedirect('/futebol/categorias/')
        else:
            return render(request, 'futebol/formCategoria.html', {'form': form})
    else:
        return HttpResponseRedirect('/futebol/categorias/')

@login_required
def editCategorias(request, pk=0):

    usuario = User.objects.filter(id=request.user.id).order_by('id')
    
    try:
        categoria = CategoriaComentarios.objects.get(pk=pk)
        #validando o owner
        urlnome = categoria.user
        logadonome = usuario[0]
        if logadonome == urlnome:
            form = CategoriaForm(instance=categoria)
            print 'certo-categoria'
        else:
            print 'errado-categoria'
            return HttpResponseRedirect('/futebol/categoria/')

    except:
        return HttpResponseRedirect('/futebol/equipes/')

    return render(request, 'futebol/formCategoria.html', {'form': form})

@login_required
def delCategorias(request, pk=0):
    try:
        categoria = CategoriaComentarios.objects.get(pk=pk)
        categoria.delete()
        return HttpResponseRedirect('/futebol/categorias/')
    except:
        return HttpResponseRedirect('/futebol/categorias/')


################################## JOGADORES ###################################
@login_required
def listJogadores(request, pk=0):
    equipe = Equipes.objects.get(pk=pk)
    jogadores = Jogadores.objects.filter(equipe__id=equipe.pk).order_by('num')
    usuario2 = User.objects.filter(id=request.user.id).order_by('id')
    urlnome = equipe.user
    logadonome = usuario2[0]
    if logadonome == urlnome:
        context = {'jogadores':jogadores, 'equipe':equipe}
        print 'certo'
    else:
        print 'errado'
        return HttpResponseRedirect('/futebol/equipes/')

    return render(request, 'futebol/listJogadores.html', context)

@login_required
def newJogadores(request, pk=0):
    equipeobj = Equipes.objects.get(pk=pk)
    form = JogadoresForm()
    return render(request, 'futebol/formJogadores.html', {'form': form, 'equipeobj': equipeobj})

@login_required
def saveJogadores(request):

    #jogador = Jogadores.objects.get(pk=codigo)
    #equipepk = jogador.equipe_id
    #equipeobj = Equipes.objects.get(pk=equipepk)
    #pke = equipeobj.id
    if request.method == 'POST':
        try:
            jogador = Jogadores.objects.get(pk=request.POST.get('id','0'))
            equipe = Equipes.objects.get(pk=request.POST.get('equipe'))
            #equipepk = jogador.equipe_id
            #equipeobj = Equipes.objects.get(pk=equipepk)
            pke = equipe.pk
            print pke
            form = JogadoresForm(request.POST, instance=jogador)
        except:
            equipe = Equipes.objects.get(pk=request.POST.get('equipe'))
            pke = equipe.pk
            print pke
            form = JogadoresForm(request.POST)

        if form.is_valid():
            
            jogador = form.save()
            
            return HttpResponseRedirect('/futebol/jogadores/'+str(pke))
        else:
            return render(request, 'futebol/formJogadores.html', {'form': form})
    else:
        return HttpResponseRedirect('/futebol/jogadores/'+str(pke))

@login_required
def editJogadores(request, pk=0):
    usuario = User.objects.filter(id=request.user.id).order_by('id')
    jogador = Jogadores.objects.get(pk=pk)
    #validando o owner
    equipepk = jogador.equipe_id
    equipeobj = Equipes.objects.get(pk=equipepk)
    pke = equipeobj.id

    try:
        jogador = Jogadores.objects.get(pk=pk)
        #validando o owner
        equipepk = jogador.equipe_id
        pke = equipeobj.pk
        equipeobj = Equipes.objects.get(pk=equipepk)
        logadonome = usuario[0]
        form = JogadoresForm(instance=jogador)
        if logadonome == equipeobj.user:
            context = {'equipeobj':equipeobj, 'form':form}
            print 'certo-jogador'
        else:
            #print 'errado-jogador'
            return HttpResponseRedirect('/futebol/jogadores/'+str(pke))
    except:
        return HttpResponseRedirect('/futebol/jogadores/'+str(pke))

    return render(request, 'futebol/formJogadores.html',context)

@login_required
def delJogadores(request, pk=0):
    try:
        jogador = Jogadores.objects.get(pk=pk)
        equipepk = jogador.equipe_id
        equipeobj = Equipes.objects.get(pk=equipepk)
        pke = equipeobj.id
        jogador.delete()
        return HttpResponseRedirect('/futebol/jogadores/'+str(pke))
    except:
        return HttpResponseRedirect('/futebol/equipes/')

################################## EQUIPES ###################################

@login_required
def listEquipes(request, template='futebol/listEquipes.html'):

    equipes = Equipes.objects.filter(user__id=request.user.id).order_by('id')
    print request.user.id
    usuario = User.objects.filter(id=request.user.id).order_by('id')
    context = {'usuario':usuario, 'equipes':equipes}
    
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@page_template('futebol/paginacao.html')  # just add this decorator
def entry_index(request, template='futebol/listEquipes-ajax.html', extra_context=None):
    entries = Equipes.objects.all
    context = {
        'entries': entries,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(
        template, context, context_instance=RequestContext(request))

@login_required
def editEquipes(request, pk=0):
    usuario = User.objects.filter(id=request.user.id).order_by('id')

    try:
        equipe = Equipes.objects.get(pk=pk)
        #validando o owner
        urlnome = equipe.user
        logadonome = usuario[0]
        if logadonome == urlnome:
            form = EquipesForm(instance=equipe)
            print 'certo-equipe'
        else:
            print 'errado-equipe'
            return HttpResponseRedirect('/futebol/equipes/')

    except:
        return HttpResponseRedirect('/futebol/equipes/')

    return render(request, 'futebol/formEquipes.html', {'form': form})

@login_required
def newEquipes(request):
    form = EquipesForm()
    return render(request, 'futebol/formEquipes.html', {'form': form})

@login_required
def saveEquipes(request):
    if request.method == 'POST':
        try:
            equipe = Equipes.objects.get(pk=request.POST.get('id','0'))
            form = EquipesForm(request.POST, instance=equipe)
        except:
            form = EquipesForm(request.POST)

        if form.is_valid():
            equipe = form.save()
            return HttpResponseRedirect('/futebol/equipes/')
        else:
            return render(request, 'futebol/formEquipes.html', {'form': form})
    else:
        return HttpResponseRedirect('/futebol/equipes/')

@login_required
def delEquipes(request, pk=0):
    try:
        equipe = Equipes.objects.get(pk=pk)
        equipe.delete()
        return HttpResponseRedirect('/futebol/equipes/')
    except:
        return HttpResponseRedirect('/futebol/equipes/')

