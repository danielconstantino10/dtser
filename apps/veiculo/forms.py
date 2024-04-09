from django import forms
from .models import *
from django_select2.forms import Select2Widget

class CorForm(forms.ModelForm):
    class Meta:
        model = Cor
        fields = (
            'nome',
        )
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'})
        }

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = (
            'nome',
        )
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'})
        }

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = (
            'nome',
        )
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegistoInicialForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), widget=Select2Widget(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = RegistoInicial
        fields = (
            'numero_motor', 
            'numero_quadro', 
            'matricula', 
            'lotacao',
            'tipo_veiculo',
            'marca',
            'modelo',
            'cor',
            )
        widgets = {
            'numero_motor': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_quadro': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'lotacao': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_veiculo': Select2Widget(attrs={'class': 'form-control'}),
            'modelo': Select2Widget(attrs={'class': 'form-control'}),
            'cor': Select2Widget(attrs={'class': 'form-control'}),
        }