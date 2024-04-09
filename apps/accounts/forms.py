from django import forms
from django.contrib.auth import authenticate
from apps.accounts.models import Pessoa,PessoaFisica, PessoaJuridica
from django.utils.translation import ugettext_lazy as _
from apps.accounts import models

class UserLoginForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control line-input', 'placeholder': 'Nome de usuário'}),
            'password': forms.TextInput(attrs={'class': 'form-control line-input', 'placeholder': 'Senha'}),
        }
        labels = {
            'username': _(u'person'),
            'password': _(u'lock'),
        }

    # Validar/autenticar campos de login
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(u"Usuário ou senha inválidos.")
        return self.cleaned_data

    def authenticate_user(self, username, password):
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(u"Usuário ou senha inválidos.")
        return user

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control line-input'}))

    class Meta:
        model = models.User
        fields = ('username', 'department',)
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'})
        }

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = (
            'nome',
            'numero_identificacao',
        )
        widgets = {
            'nome': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'numero_identificacao': forms.TextInput(attrs={'type': 'text','class': 'form-control'})
        }

class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = [
            'data_nascimento',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type':'date', 'class': 'form-control'})
        }

class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = [
            'responsavel',
        ]
        widgets = {
            'responsavel': forms.TextInput(attrs={'type': 'text','class': 'form-control'}),
        }