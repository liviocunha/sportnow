from django.contrib import admin
from futebol.models import *


class EquipesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user', 'hashtag')


class JogadoresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nome', 'equipe', 'num')

		
class EquipeCasaAdmin(admin.ModelAdmin):
    pass

class EquipeVisitanteAdmin(admin.ModelAdmin):
    pass

class ComentariosAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'desc', 'tipo', 'categoria', 'user')
        }),
    )

    list_display = ('pk', 'categoria', 'user','name','tipo')
    list_display_links = ('pk', 'name')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name')

class PartidasAdmin(admin.ModelAdmin):
    list_display = ('pk', 'data', 'cidade', 'user')

admin.site.register(Equipes, EquipesAdmin)
admin.site.register(Jogadores, JogadoresAdmin)
admin.site.register(Partidas, PartidasAdmin)
admin.site.register(EquipeCasa, EquipeCasaAdmin)
admin.site.register(EquipeVisitante, EquipeVisitanteAdmin)
admin.site.register(Comentarios, ComentariosAdmin)
admin.site.register(CategoriaComentarios, CategoriaAdmin)

