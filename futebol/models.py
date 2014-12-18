# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class CategoriaComentarios(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, blank=False, null=False)

    class Meta:
        verbose_name = _('categoria dos comentarios')
        verbose_name_plural = _('categorias dos comentarios ')

    def __unicode__(self): return self.name 

class Comentarios(models.Model):
    CHOICES_TIPO = (
        ('SC', 'Comentário'),
        ('SE', 'Equipe01'),
        ('EE', 'Equipe01+Equipe02'),
        ('EJ', 'Equipe1+Jogador1'),
        ('SJ', 'Jogador1'),
        ('JJ', 'Jogador1+Jogador2'),
    )
    name = models.CharField(max_length=50, blank=False, null=False)
    desc = models.CharField(max_length=130, blank=False, null=False)
    tipo = models.CharField(max_length=2, choices=CHOICES_TIPO)
    categoria = models.ForeignKey('CategoriaComentarios')
    user = models.ForeignKey(User)
    
    class Meta:
        verbose_name = _('comentario')
        verbose_name_plural = _('comentarios')

    def __unicode__(self): return u"%s" %(self.categoria.pk)
        
class Equipes(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(_(u'Nome'), max_length=50, blank=False, null=False)
    display = models.CharField(_(u'Display'), max_length=10, blank=False, null=False)
    hashtag = models.CharField(_(u'Hashtag'), max_length=10, blank=False, null=False)

    class Meta:
        verbose_name = _('equipe')
        verbose_name_plural = _('equipes')

    def __unicode__(self): return self.name   

class EquipeCasa(models.Model):
    pk_equipe = models.ForeignKey('Equipes')
    
    class Meta:
        verbose_name = _('equipe casa')
        verbose_name_plural = _('equipes casa')

    def __unicode__(self): return u"%s" %(self.pk_equipe)

class EquipeVisitante(models.Model):
    pk_equipe = models.ForeignKey('Equipes')
    
    class Meta:
        verbose_name = _('equipe visitante')
        verbose_name_plural = _('equipes visitante')

    def __unicode__(self): return u"%s" %(self.pk_equipe)
        
class Jogadores(models.Model):
    equipe = models.ForeignKey('Equipes')
    nome = models.CharField(db_index=True, max_length='15', blank=False, null=False)
    num =  models.IntegerField(max_length='10', blank=False, null=False)
    display = models.CharField(_(u'Display'), max_length=10, blank=False, null=False)

    class Meta:
        verbose_name = _('jogador')
        verbose_name_plural = _('jogadores')

    def __unicode__(self): return self.nome   

class Partidas(models.Model):
    data = models.DateField(_(u'Data'), blank=True)
    hora = models.TimeField(_(u'Hora'), blank=True)
    id_casa = models.CharField(_(u'ID_casa'), max_length=10, blank=False, null=False)
    id_visitante = models.CharField(_(u'ID_visitante'), max_length=10, blank=False, null=False)
    cidade = models.CharField(_(u'Cidade'), max_length=10, blank=False, null=False)
    local = models.CharField(_(u'Local'), max_length=10, blank=False, null=False)
    user = models.ForeignKey(User)
    status = models.CharField(_(u'Status'), max_length=3)
    
    class Meta:
        verbose_name = _('partida')
        verbose_name_plural = _('partidas')

    def __unicode__(self): return unicode(self.pk)

