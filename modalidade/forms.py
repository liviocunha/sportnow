from django import forms
from modalidade.models import Modalidade

class ModalidadeForm(forms.ModelForm):
    class Meta:
        model = Modalidade