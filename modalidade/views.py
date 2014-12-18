# coding: utf-8
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect,HttpResponseRedirect, render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialToken, SocialAccount
from modalidade.models import Modalidade
from modalidade.forms import ModalidadeForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.utils import timezone
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core import serializers
import facebook
from authomatic import Authomatic
from django.contrib import messages

@login_required
def modalidade(request, modalidade_id):
    if modalidade_id == '1': #futebol
        
        return render(request, 'core/form_futebol.html')
    else:
        msg =  404
        print msg
        return HttpResponseRedirect('/logado/%s/' %msg)

@login_required
def create(request):
    form = ModalidadeForm()
    return render(request, 'modalidadeform.html', {'form': form, 'page_name': 'Nova Modalidade'})

@login_required
def save(request):
    if request.method == 'POST':
        try:
            modalidade = Modalidade.objects.get(pk=request.POST.get('id','0'))   
            form = ModalidadeForm(request.POST, instance=post)  
        except:
            form = ModalidadeForm(request.POST)
        
        if form.is_valid():

            modalidade = form.save()
            return HttpResponseRedirect('/')
        else:
            return render(request, 'modalidadeform.html', {'form': form})    
    else:
        return HttpResponseRedirect('/')