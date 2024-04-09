from django.contrib.messages.api import error
from apps.accounts.forms import PessoaFisicaForm, PessoaForm
from apps.website.views import home_index
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import *
from .models import Pessoa, PessoaFisica, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

# Create your views here.

def sign_in(request):
    template_name = 'accounts/sign_in.html'
    form_class = UserLoginForm(request.POST or None)
    if request.POST and form_class.is_valid():
        username = form_class.cleaned_data['username']
        password = form_class.cleaned_data['password']
        user = form_class.authenticate_user(username=username, password=password)
        if user:
            login(request, user)
            return redirect('administration:index')
    return render(request, template_name, {'form_class': form_class})

@login_required
def sign_out(request):
    """User sign-out view."""
    logout(request)
    return redirect('accounts:sign_in')

def sign_up(request, commit=True):
    template_name = 'accounts/sign_up.html'
    form = UserRegistrationForm(request.POST)
    form_pessoa = PessoaForm(request.POST)
    form_pessoa_fisica = PessoaFisicaForm(request.POST)
    identificacao_exists=Pessoa.objects.filter(numero_identificacao=request.POST.get('numero_identificacao', False)).exists()
    username_exists=User.objects.filter(username=request.POST.get('username', False)).exists()
    
    ano_actual = datetime.now().year
    if request.method == 'POST':
        if username_exists == True:
            messages.error(request, 'Erro ao gravar, esse Nome de usuário "' + request.POST['username'] + '" já existente...')
        else:
            if (form.is_valid() and form_pessoa.is_valid() and form_pessoa_fisica.is_valid()):
                _pessoa = form_pessoa.save(commit=False)
                ano_nascimento = form_pessoa_fisica.cleaned_data['data_nascimento'].year
                print(ano_nascimento)
                idade = ano_actual- ano_nascimento
                if idade < 18:
                    messages.error(request, 'Não foi possivel efectuar o cadastro porque a idade é menor que 18')
                else:
                    if identificacao_exists == False:
                        _pessoa.save()
                        if commit:
                            _pessoa_fisica = form_pessoa_fisica.save(commit=False)
                            _pessoa_fisica.data_nascimento = form_pessoa_fisica.cleaned_data['data_nascimento']
                            _pessoa_fisica.pessoa = _pessoa
                            _pessoa_fisica.save()
                            if commit:
                                _user = form.save(commit=False)
                                _nome_completo = _pessoa.nome.split()
                                _user.password = "dtser2021"
                                _user.first_name = _nome_completo[0]
                                _user.last_name = _nome_completo[-1]
                                _user.pessoa = _pessoa
                                _user.save()
                                messages.success(request, 'Usuário "' + _pessoa.nome + '" registado com sucesso.')
                    else:
                        pessoa = Pessoa.objects.get(numero_identificacao=request.POST['numero_identificacao'])
                        _pessoa_fisica = form_pessoa_fisica.save(commit=False)
                        _pessoa_fisica.data_nascimento = form_pessoa_fisica.cleaned_data['data_nascimento']
                        _pessoa_fisica.pessoa = pessoa
                        _pessoa_fisica.save()
                        if commit:
                            _user = form.save(commit=False)
                            _nome_completo = _pessoa.nome.split()
                            _user.password = 'dtser2021'
                            _user.first_name = _nome_completo[0]
                            _user.last_name = _nome_completo[-1]
                            _user.pessoa = _pessoa
                            _user.save()
                            messages.success(request, 'Usuário "' + _pessoa.nome + '" registado com sucesso.')
                
    context = {
        'form': form,
        'form_pessoa': form_pessoa,
        'form_pessoa_fisica': form_pessoa_fisica
    }          
    return render(request, template_name, context)

def visualizar_users(request):
    template_name = 'accounts/user-list.html'
    context = {
        'users': User.objects.exclude(department='3')

    }
    return render(request, template_name, context)