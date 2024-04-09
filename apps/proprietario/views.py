from apps.verbete.forms import VerbeteCartaForm
from apps.accounts.models import *
from apps.veiculo.models import *
from apps.verbete.models import *
from apps.proprietario.forms import *
from django.shortcuts import render
from apps.accounts.forms import *
from .models import Proprietario
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, date, timedelta
# TO RENDER INVOICE 
from django.template.loader import get_template, render_to_string
from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML, CSS
import tempfile

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your views here.

@login_required
def proprietario_veiculo_add(request, commit=True):
    template_name = 'veiculo/proprietario-veiculo-add.html'
    form_pessoa = PessoaForm(request.POST)
    form_pessoa_fisica = PessoaFisicaForm(request.POST)
    form_pessoa_juridica = PessoaJuridicaForm(request.POST)
    form_veiculo = RegistoInicialForm(request.POST)
    result = Pessoa.objects.filter(numero_identificacao=request.POST.get('numero_identificacao', False))
    motor_exists = RegistoInicial.objects.filter(numero_motor=request.POST.get('numero_motor', False)).exists()
    quadro_exists = RegistoInicial.objects.filter(numero_quadro=request.POST.get('numero_quadro', False)).exists()
    matricula_exists = RegistoInicial.objects.filter(matricula=request.POST.get('matricula', False)).exists()
    if request.method == 'POST':  
        if result.exists() == False:                 
            #3
            if ((motor_exists == True) and (quadro_exists == True) and (matricula_exists == True)):
                messages.info(request, 'Esse Motor Nº: "' + request.POST['numero_motor'] + '" já existe.')  
                messages.info(request, 'Esse Quadro Nº: "' + request.POST['numero_quadro'] + '" já existe.')
                messages.info(request, 'Essa Matricula Nº: "' + request.POST['matricula'] + '" já existe.')
            #2
            elif ((motor_exists == True) and (quadro_exists == True) and (matricula_exists == False)):
                messages.info(request, 'Esse Motor Nº: "' + request.POST['numero_motor'] + '" já existe.')
                messages.info(request, 'Esse Quadro Nº: "' + request.POST['numero_quadro'] + '" já existe.')
            #2
            elif ((motor_exists == True) and (quadro_exists == False) and (matricula_exists == True)):
                messages.info(request, 'Esse Motor Nº: "' + request.POST['numero_motor'] + '" já existe.')
                messages.info(request, 'Essa Matricula Nº: "' + request.POST['matricula'] + '" já existe.')
            #1
            elif ((motor_exists == True) and (quadro_exists == False) and (matricula_exists == False)):
                messages.info(request, 'Esse Motor Nº: "' + request.POST['numero_motor'] + '" já existe.')
            #2
            elif ((motor_exists == False) and (quadro_exists == True) and (matricula_exists == True)):
                messages.info(request, 'Esse Quadro Nº: "' + request.POST['numero_quadro'] + '" já existe.')
                messages.info(request, 'Essa Matricula Nº: "' + request.POST['matricula'] + '" já existe.')
            #1
            elif ((motor_exists == False) and (quadro_exists == True) and (matricula_exists == False)):
                messages.info(request, 'Esse Quadro Nº: "' + request.POST['numero_quadro'] + '" já existe.')
            #1
            elif ((motor_exists == False) and (quadro_exists == False) and (matricula_exists == True)):
                messages.info(request, 'Essa Matricula Nº: "' + request.POST['matricula'] + '" já existe.')
            else:
                if request.POST.get('tipo_proprietario') == '2':
                    if (form_pessoa.is_valid() and form_pessoa_juridica.is_valid() and form_veiculo.is_valid()):                   
                        _object_pessoa = form_pessoa.save(commit=False)
                        _object_pessoa.tipo_pessoa=2
                        _object_pessoa.save()
                        if commit:
                            _object_pessoa_juridica = form_pessoa_juridica.save(commit=False)
                            _object_pessoa_juridica.pessoa_id = _object_pessoa
                            _object_pessoa_juridica.save()
                            if commit:
                                _proprietario = Proprietario.objects.create(
                                    pessoa = _object_pessoa, 
                                    operador = request.user
                                )
                                if commit:
                                    _veiculo = form_veiculo.save(commit=False)
                                    _veiculo.proprietario = _proprietario
                                    _veiculo.operador = request.user
                                    _veiculo.save()
                                    _verbete = VerbeteViatura(
                                        registo_inicial = _veiculo,
                                        data_validade = datetime.today() + timedelta(days=90)
                                    )
                                    _verbete.save()
                                    if commit:
                                        HistoricoVerbeteViatura.objects.create(
                                            verbete = _verbete,
                                            data_validade = datetime.today() + timedelta(days=90),
                                            operador = request.user
                                        )
                                        verbete = VerbeteViatura.objects.get(id=_verbete.id)
                                        context = {
                                          'verbete': verbete,
                                          }
                                        response = HttpResponse(content_type="application/pdf")
                                        #inline or attachment
                                        response['Content-Disposition'] = "attachment; filename=invoice.pdf"

                                        html = render_to_string("verbete/verbete-viatura-invoice.html",context)

                                        font_config = FontConfiguration()
                                        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
                                        return response
                    
                else:
                    if (form_pessoa.is_valid() and form_pessoa_fisica.is_valid() and form_veiculo.is_valid()):                   
                        _object_pessoa = form_pessoa.save(commit=False)
                        _object_pessoa.tipo_pessoa=1
                        _object_pessoa.save()
                        if commit:
                            _object_pessoa_fisica = form_pessoa_fisica.save(commit=False)
                            _object_pessoa_fisica.pessoa_id = _object_pessoa
                            _object_pessoa_fisica.save()
                            if commit:
                                _proprietario = Proprietario.objects.create(
                                    pessoa = _object_pessoa, 
                                    operador = request.user
                                )
                                if commit:
                                    _veiculo = form_veiculo.save(commit=False)
                                    _veiculo.proprietario = _proprietario
                                    _veiculo.operador = request.user
                                    _veiculo.save()
                                    _verbete = VerbeteViatura(
                                        registo_inicial = _veiculo,
                                        data_validade = datetime.today() + timedelta(days=90)
                                    )
                                    _verbete.save()
                                    if commit:
                                        data = ('Nº Verbete: ' + str(_verbete.id) + 
                                        ' Proprietário: ' +  str(_verbete.registo_inicial.proprietario.pessoa.nome) + 
                                        ' Data de Emissão: ' +  str(_verbete.data_emissao) + 
                                        'Data de Validade: ' +  str(_verbete.data_validade)
                                        )  
                                        qrcode_img = qrcode.make(data)
                                        canvas = Image.new('RGB', (290, 290), 'white')
                                        draw = ImageDraw.Draw(canvas)
                                        canvas.paste(qrcode_img)
                                        fname = f'qr_code-{_verbete.id}.png'
                                        buffer = BytesIO()
                                        canvas.save(buffer, 'PNG')
                                        _verbete.qr_code.save(fname, File(buffer), save=False)
                                        canvas.close()
                                        _verbete.save()
                                        HistoricoVerbeteViatura.objects.create(
                                            verbete = _verbete,
                                            data_validade = datetime.today() + timedelta(days=90),
                                            operador = request.user
                                        )
                                        verbete = VerbeteViatura.objects.get(id=_verbete.id)
                                        context = {
                                          'verbete': verbete,
                                          }
                                        response = HttpResponse(content_type="application/pdf")
                                        #inline or attachment
                                        response['Content-Disposition'] = "attachment; filename=invoice.pdf"
                                        html = render_to_string("verbete/verbete-viatura-invoice.html",context)

                                        font_config = FontConfiguration()
                                        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
                                        return response
        else:   
            messages.info(request, 'Não foi póssivel adicionar o proprietário do Nº de Identificação: "' + request.POST['numero_identificacao'] + '" porque já foi adicionado!')

    context = {
        'form_pessoa' : form_pessoa,
        'form': form_veiculo,
        'form_pessoa_fisica' : form_pessoa_fisica,
        'form_pessoa_juridica' : form_pessoa_juridica,
    }
    return render(request, template_name, context)

@login_required
def proprietario_carta_add(request, commit=True):
    template_name = 'proprietario/proprietario-carta-add.html'
    form_pessoa = PessoaForm(request.POST)
    form_pessoa_fisica = PessoaFisicaForm(request.POST)
    form_verbete = VerbeteCartaForm(request.POST)
    numero_carta_exists = VerbeteCarta.objects.filter(numero_carta = request.POST.get('numero_carta', False))
    if request.method == 'POST':  
        if numero_carta_exists.exists() == False:
            numero_identificacao_exists = Pessoa.objects.filter(numero_identificacao = request.POST.get('numero_identificacao', False))
            if numero_identificacao_exists.exists() == False:
                if (form_pessoa.is_valid() and form_pessoa_fisica.is_valid() and form_verbete.is_valid()):                   
                    _object_pessoa = form_pessoa.save(commit=False)
                    _object_pessoa.tipo_pessoa=1
                    _object_pessoa.save()
                    if commit:
                        _object_pessoa_fisica = form_pessoa_fisica.save(commit=False)
                        _object_pessoa_fisica.pessoa_id = _object_pessoa
                        _object_pessoa_fisica.save()
                        _proprietario = Proprietario.objects.create(
                            pessoa = _object_pessoa, 
                            operador = request.user
                        )
                        if commit:
                            if form_verbete.is_valid():
                                _object_verbete = form_verbete.save(commit=False)
                                _object_verbete.proprietario = _proprietario
                                _object_verbete.data_validade = datetime.today() + timedelta(days=90)
                                _object_verbete.save()
                                data = ('Nº Verbete: ' + str(_object_verbete.id) + 
                                  ' Proprietário: ' +  str(_object_verbete.proprietario.pessoa.nome) + 
                                  ' Data de Emissão: ' +  str(_object_verbete.data_emissao) + 
                                  'Data de Validade: ' +  str(_object_verbete.data_validade)
                                )  
                                qrcode_img = qrcode.make(data)
                                canvas = Image.new('RGB', (290, 290), 'white')
                                draw = ImageDraw.Draw(canvas)
                                canvas.paste(qrcode_img)
                                fname = f'qr_code-{_object_verbete.id}.png'
                                buffer = BytesIO()
                                canvas.save(buffer, 'PNG')
                                _object_verbete.qr_code.save(fname, File(buffer), save=False)
                                canvas.close()
                                _object_verbete.save()
                                if commit:
                                    HistoricoVerbeteCarta.objects.create(
                                        verbete = _object_verbete,
                                        data_emissao = _object_verbete.data_emissao,
                                        data_validade = datetime.today() + timedelta(days=90),
                                        operador = request.user
                                    )
                                    if commit:
                                        verbete = VerbeteCarta.objects.get(id=_object_verbete.id)
                                        context = {
                                          'verbete': verbete,
                                          }
                                        response = HttpResponse(content_type="application/pdf")
                                        #inline or attachment
                                        response['Content-Disposition'] = "attachment; filename=invoice.pdf"

                                        html = render_to_string("verbete/verbete-carta-invoice.html",context)

                                        font_config = FontConfiguration()
                                        HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
                                        return response                                                     
            else:
                _pessoa_id = Pessoa.objects.get(numero_identificacao = request.POST.get('numero_identificacao', False))
                print(_pessoa_id)
                _proprietario_exists = Proprietario.objects.filter(pessoa=_pessoa_id).exists()
                _pessoa_fisica_exists = PessoaFisica.objects.filter(pessoa_id=_pessoa_id).exists()
                if _pessoa_fisica_exists == False:
                    if form_pessoa_fisica.is_valid():
                        _object_pessoa_fisica = form_pessoa_fisica.save(commit=False)
                        _object_pessoa_fisica.pessoa_id = _pessoa_id
                        _object_pessoa_fisica.save()
                        if commit:
                            if _proprietario_exists == False:
                                if form_verbete.is_valid():
                                    _object_verbete = form_verbete.save(commit=False)
                                    _proprietario = Proprietario.objects.create(
                                        pessoa = _pessoa_id,
                                        operador = request.user
                                    )
                                    _object_verbete.data_validade = datetime.today() + timedelta(days=90)
                                    _object_verbete.save()
                                    if commit:
                                        HistoricoVerbeteCarta.objects.create(
                                            verbete = _object_verbete,
                                            data_emissao = _object_verbete.data_emissao,
                                            data_validade = datetime.today() + timedelta(days=90),
                                            operador = request.user
                                        )
                                        if commit:
                                            verbete = VerbeteCarta.objects.get(id=_object_verbete.id)
                                            context = {
                                              'verbete': verbete,
                                              }
                                            response = HttpResponse(content_type="application/pdf")
                                            #inline or attachment
                                            response['Content-Disposition'] = "attachment; filename=invoice.pdf"

                                            html = render_to_string("verbete/verbete-carta-invoice.html",context)

                                            font_config = FontConfiguration()
                                            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
                                            return response        
                            else:          
                                _proprietario = Proprietario.objects.get(pessoa = _pessoa_id)
                                print(_proprietario)
                                verbete_carta_exists = VerbeteCarta.objects.filter(proprietario=_proprietario.id).exists()   
                                if verbete_carta_exists == False:             
                                    if form_verbete.is_valid():
                                        _object_verbete = form_verbete.save(commit=False)
                                        _object_verbete.proprietario = _proprietario
                                        _object_verbete.data_validade = datetime.today() + timedelta(days=90)
                                        _object_verbete.save()
                                        if commit:
                                            HistoricoVerbeteCarta.objects.create(
                                                verbete = _object_verbete,
                                                data_emissao = _object_verbete.data_emissao,
                                                data_validade = datetime.today() + timedelta(days=90),
                                                operador = request.user
                                            )
                                            if commit:
                                                verbete = VerbeteCarta.objects.get(id=_object_verbete.id)
                                                context = {
                                                  'verbete': verbete,
                                                  }
                                                response = HttpResponse(content_type="application/pdf")
                                                #inline or attachment
                                                response['Content-Disposition'] = "inline; filename=invoice.pdf"

                                                html = render_to_string("verbete/verbete-carta-invoice.html",context)

                                                font_config = FontConfiguration()
                                                HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
                                                return response           
                                else:
                                    messages.error(request, 'Essa pessoa já tem um registo de verbete de carta...')
    
        else:
            messages.error(request, 'Essa carta Nº: "' + request.POST['numero_carta'] + '" já está associado há um condutor...')
    context = {
        'form_pessoa' : form_pessoa,
        'form_verbete': form_verbete,
        'form_pessoa_fisica' : form_pessoa_fisica,
    }
    return render(request, template_name, context)

@login_required
def proprietario_veiculo_visualizar(request):
    template_name = 'proprietario/proprietario-veiculo-visualizar.html'
    veiculos = RegistoInicial.objects.filter(
        proprietario__in=Proprietario.objects.filter(
            pessoa__in=Pessoa.objects.all())).values(
                'proprietario',
                'proprietario__pessoa__nome',
                'proprietario__pessoa__numero_identificacao',
                'proprietario__data_registo',
                ).distinct()
    context = {
        'object_list': veiculos
    }
    return render(request, template_name, context)

@login_required
def proprietario_carta_visualizar(request):
    template_name = 'proprietario/proprietario-carta-visualizar.html'
    data_actual = datetime.today()
    VerbeteCarta.objects.filter(data_validade__lt=data_actual).update(estado=False)
    condutores = VerbeteCarta.objects.all()
    context = {
        'object_list': condutores
    }
    return render(request, template_name, context)