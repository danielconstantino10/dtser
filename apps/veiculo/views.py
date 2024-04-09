from django.shortcuts import redirect, render
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template, render_to_string
from weasyprint import HTML, CSS
import tempfile

from datetime import datetime, timedelta
from apps.verbete.models import *
import json as simplejson
from django.http import HttpResponse

# TO RENDER INVOICE 
from django.template.loader import get_template, render_to_string
from weasyprint.text.fonts import FontConfiguration
from weasyprint import HTML, CSS

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# Create your views here.

def adicionar_cor(request, commit=False):
    template_name = 'cor/cor-add.html'
    form = CorForm(request.POST)
    result = Cor.objects.filter(nome=request.POST.get('nome', False))
    if result.exists() == False:
        if form.is_valid():
            _object = form.save(commit=False)
            _object.save()
            messages.success(request, 'Cor "' + request.POST['nome'] + '" adicionado com sucesso...')
    else:
        messages.info(request, 'Não foi póssivel adiconar a Cor "' + request.POST['nome'] + '" porque já foi adicionado!')

    context = {
        'form': form,
        'object_list':Cor.objects.all(),
    }
    return render(request, template_name, context)

def adicionar_marca(request, commit=False):
    template_name = 'marca/marca-add.html'
    form = MarcaForm(request.POST)
    result = Marca.objects.filter(nome=request.POST.get('nome', False))
    if result.exists() == False:
        if form.is_valid():
            _object = form.save(commit=False)
            _object.save()
            messages.success(request, 'Marca "' + request.POST['nome'] + '" adicionado com sucesso...')
    else:
        messages.info(request, 'Não foi póssivel adiconar a marca "' + request.POST['nome'] + '" porque já foi adicionado!')

    context = {
        'form': form,
        'object_list':Marca.objects.all(),
    }
    return render(request, template_name, context)

def adicionar_modelo(request, marca_id):
    template_name = 'modelo/modelo-add.html'
    form = ModeloForm(request.POST or None)
    result = Modelo.objects.filter(nome=request.POST.get('nome', False))
    if result.exists() == False:
        if form.is_valid():
            _object = form.save(commit=False)
            _object.marca = Marca.objects.get(id=marca_id)
            _object.save()
            messages.success(request, 'Modelo "' + request.POST['nome'] + '" adicionado com sucesso...')
    else:
        messages.info(request, 'Não foi póssivel adiconar esse modelo "' + request.POST['nome'] + '" porque já foi adicionado!')
    context = {
        'form': form,
        'object_list': Modelo.objects.filter(marca=marca_id),
        'nome_marca': Marca.objects.get(id=marca_id).nome
    }
    return render(request, template_name, context)

@login_required
def proprietario_viatura_details(request, pk):
    template_name = 'veiculo/proprietario-viatura-details.html'
    data_actual = datetime.today()
    VerbeteViatura.objects.filter(data_validade__lt=data_actual).update(estado=False)
    viaturas = VerbeteViatura.objects.filter(
        registo_inicial__in=RegistoInicial.objects.filter(
            proprietario__in=Proprietario.objects.filter(pessoa=pk)))
    context = {
        'viaturas': viaturas,
        'key': pk,   
    }
    return render(request, template_name, context)

@login_required
def efectuar_registo_inicial_viatura(request, pk, commit=True):
    template_name = 'veiculo/efectuar-registo-inicial-viatura.html'
    form = RegistoInicialForm(request.POST)
    motor_exists = RegistoInicial.objects.filter(numero_motor=request.POST.get('numero_motor', False)).exists()
    quadro_exists = RegistoInicial.objects.filter(numero_quadro=request.POST.get('numero_quadro', False)).exists()
    matricula_exists = RegistoInicial.objects.filter(matricula=request.POST.get('matricula', False)).exists()
    if request.method == 'POST':
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
            if form.is_valid():
                _object= form.save(commit=False)
                _object.proprietario = Proprietario.objects.get(pessoa=pk)
                _object.operador = request.user
                _object.save()
                _verbete = VerbeteViatura(
                    registo_inicial = _object,
                    data_validade = datetime.today() + timedelta(days=90)
                )
                _verbete.save()
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
                    response['Content-Disposition'] = "inline; filename=invoice.pdf"

                    html = render_to_string("verbete/verbete-viatura-invoice.html",context)

                    font_config = FontConfiguration()
                    HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
                    return response
            else:
                messages.error(request, 'Erro ao fazer o registo inicial de viatura, contacte o Administrador.')      
    context = {
        'form': form,
        'key': pk, 
    }
    return render(request, template_name, context)

def anular_registo_inicial_viatura(request, pk):
    template_name = 'veiculo/registo-inicial-viatura-delete.html'
    registo_inicial = RegistoInicial.objects.get(id=pk)
    if request.method == "POST":
        registo_inicial.delete()
        return redirect('proprietario:proprietario_veiculo_visualizar')
    return render(request, template_name, {'registo_inicial': registo_inicial})

def get_modelo(request):
    if request.is_ajax() and request.method == 'GET':
        marca_id = int(request.GET['marca'])
        modelos = Modelo.objects.filter(marca = marca_id)
        centre_dict = { 
        'id':[],
        'nome':[],
        } 
        for modelo in modelos:
            centre_dict['id'].append(modelo.id)
            centre_dict['nome'].append(modelo.nome)
        return HttpResponse(simplejson.dumps(centre_dict), content_type="application/json")
    
    return HttpResponse("Temporary 404")