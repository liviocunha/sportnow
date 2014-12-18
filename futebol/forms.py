from django import forms
from futebol.models import *

class EquipesForm(forms.ModelForm):
    class Meta:
        model = Equipes

class ValidadForm(forms.Form):
    name = forms.CharField(max_length='50', required=True)
    hashtag = forms.CharField(max_length='25', required=True)

class JogadoresForm(forms.ModelForm):
    class Meta:
        model = Jogadores

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaComentarios

class ComentariosForm(forms.ModelForm):
    class Meta:
        model = Comentarios

class PartidasForm(forms.ModelForm):
    class Meta:
        model = Partidas
        widgets = {'data' : forms.DateInput(attrs={'data-role':'date', 'id':'date-input'})}