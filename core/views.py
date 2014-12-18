# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken, SocialAccount
from modalidade.models import Modalidade
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.utils import timezone
from django.db.models import Q
from core.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
import facebook
from authomatic import Authomatic

from config import CONFIG
authomatic = Authomatic(CONFIG, 'a super secret random string')


def termos(request):
    return render(request, 'core/termos.html')

@login_required
def home(request):
    return render(request, 'core/home.html')

@login_required
def logado(request, msg):
    #1 irá ser usado para usuarios de fb e tw
    #0 usuario somente e-mail
    
    var = '0'
    tmsg = ""
    if msg == "404":
        tmsg = "Modalidade não existe!"
    
    if var == '1' :
      a = SocialAccount.objects.get(user_id=request.user.id)
      b = (a.id)
      teste = SocialToken.objects.get(pk=b)
      usuario = User.objects.filter(id=request.user.id).order_by('id')
      context = {'teste':teste, 'tmsg':tmsg, 'usuario':usuario}

    else:
      usuario = User.objects.filter(id=request.user.id).order_by('id')
      context = {'usuario':usuario}

    return render(request, 'core/home.html', context)

@login_required
def modalidade(request, modalidade_id):
    if modalidade_id == '1': #futebol
        
        return render(request, 'core/form_futebol.html')
    else:
        msg =  404
        print msg
        return HttpResponseRedirect('/logado/%s/' %msg)

      
@login_required
def postarfb(request):
    a = SocialAccount.objects.get(user_id=request.user.id)
    b = (a.id)
    teste = SocialToken.objects.get(pk=b)
    mensagem = "testando-teste"
    graph = facebook.GraphAPI(teste.token)
    graph.put_object('me', 'feed', message=mensagem, link="http://www.test1.com",
            picture='http://www.thefamilyfocus.ca/images/Inserts/Calendar.png')

    return render(request, 'core/logado.html')

@login_required
def postartw(request):
    mensagem = "testando-teste5" 
    a = SocialAccount.objects.get(user_id=request.user.id)
    b = (a.id)
    teste = SocialToken.objects.get(pk=b) 
    
    serialized_credentials = '1%0A1-5%0A' + teste.token + '%0A' + teste.token_secret
    
    response = authomatic.access(serialized_credentials,
                                         url='https://api.twitter.com/1.1/statuses/update.json',
                                         params=dict(status=mensagem),
                                         method='POST')
    return render(request, 'core/logado.html')


