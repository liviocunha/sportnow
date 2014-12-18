# coding: utf-8
from django.contrib import admin
from modalidade.models import Modalidade

class ModalidadeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'desc')

admin.site.register(Modalidade, ModalidadeAdmin)


