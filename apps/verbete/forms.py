from django import forms
from .models import *
from django_select2.forms import Select2Widget

class VerbeteCartaForm(forms.ModelForm):
    class Meta:
        model = VerbeteCarta
        fields = (
            'numero_carta',
            'categoria',
        )
        widgets = {
            'numero_carta': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'})
        }

class ProrrogarVerbeteViaturaForm(forms.ModelForm):
    class Meta:
        model = VerbeteViatura
        fields = (
            'registo_inicial',
        )
        widgets = {
            'registo_inicial': forms.TextInput(attrs={'class': 'form-control'})
        }
