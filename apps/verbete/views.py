from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

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

def visualizar_verbete_carta(request):
    template_name = 'verbete/verbete-carta-list.html'
    data_actual = datetime.today()
    VerbeteCarta.objects.filter(data_validade__lt=data_actual).update(estado=False)
    context = {
        'object_list':VerbeteCarta.objects.all(),
    }
    return render(request, template_name, context)

def editar_verbete_carta(request, pk, commit=True):
    template_name = 'verbete/verbete-carta-edit.html'
    verbete = VerbeteCarta.objects.get(id=int(pk))
    form = VerbeteCartaForm(request.POST or None, instance=verbete)
    carta_exists = VerbeteCarta.objects.exclude(id=pk).filter(numero_carta = request.POST.get('numero_carta', False))
    proprietario_exists = VerbeteCarta.objects.exclude(id=pk).filter(proprietario = request.POST.get('proprietario', False))
    if carta_exists.exists() == False:
        if proprietario_exists.exists() == False:
            if form.is_valid():
                _object = form.save(commit=False)
                _object.save()
                if commit:
                    messages.success(request, 'Dados do Verbete de Carta Nº:"' + verbete.numero_carta + '" alterados com sucesso.')
                    return HttpResponseRedirect(reverse('verbete:verbete_carta_edit', kwargs={'pk':_object.id}))
        else:
            proprietario = Proprietario.objects.get(pessoa=request.POST['proprietario'])
            messages.info(request, 'Esse Proprietário Nº: "' + str(proprietario.pessoa.id) + ' - ' + proprietario.pessoa.nome + '" já tem um número de carta associado...') 
    else:
        messages.info(request, 'Essa carta Nº: "' + request.POST['numero_carta'] + '" já está associado há um condutor...')
    
    context = {
        'form':form,
        'codigo_verbete':pk
    }
    return render(request, template_name, context)

def prorrogar_verbete_carta(request, pk):
    template_name = 'verbete/verbete-carta-prorrogar.html'
    _verbete = VerbeteCarta.objects.get(id=int(pk))
    if request.method == 'POST':
        _log = HistoricoVerbeteCarta.objects.create(
            verbete = _verbete,
            data_emissao = datetime.today(),
            data_validade = datetime.today() + timedelta(days=90),
            operador = request.user
        )
        if _log:
            VerbeteCarta.objects.filter(id=pk).update(
                data_emissao = datetime.today(),
                data_validade = datetime.today() + timedelta(days=90),
                estado = True
            )
            _verbete = VerbeteCarta.objects.get(id=int(pk))
            data = (
                'Nº Verbete: ' + str(_verbete.id) + 
                ' Proprietário: ' +  str(_verbete.proprietario.pessoa.nome) + 
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
            context = {
                'verbete': _verbete,
            }
            response = HttpResponse(content_type="application/pdf")
            #inline or attachment
            response['Content-Disposition'] = "attachment; filename=invoice.pdf"

            html = render_to_string("verbete/verbete-carta-invoice.html",context)

            font_config = FontConfiguration()
            HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response, font_config=font_config, presentational_hints=True)
            return response

    context = {
        'verbete':VerbeteCarta.objects.get(id=pk)        
    }
    return render(request, template_name, context)


def prorrogar_verbete_viatura(request, pk):
    template_name = 'verbete/verbete-viatura-prorrogar.html'
    _verbete = VerbeteViatura.objects.get(id=int(pk))
    if request.method == 'POST':
        _log = HistoricoVerbeteViatura.objects.create(
            verbete = _verbete,
            data_emissao = datetime.today(),
            data_validade = datetime.today() + timedelta(days=90),
            operador = request.user
        )
        if _log:
            VerbeteViatura.objects.filter(id=pk).update(
                data_emissao = datetime.today(),
                data_validade = datetime.today() + timedelta(days=90),
                estado = True
            )
            verbete = VerbeteViatura.objects.get(id=int(pk))
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
    context = {
        'verbete':VerbeteCarta.objects.get(id=pk)        
    }
    return render(request, template_name, context)

def invoice_verbete_carta(request, pk):
    verbete = VerbeteCarta.objects.get(id=int(pk))
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

def invoice_verbete_viatura(request, pk):
    verbete = VerbeteViatura.objects.get(id=int(pk))
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

def anular_verbete_carta(request, pk):
    template_name = 'verbete/verbete-carta-delete.html'
    verbete = VerbeteCarta.objects.get(id=pk)
    if request.method == "POST":
        verbete.delete()
        return redirect('proprietario:proprietario_carta_visualizar')
    return render(request, template_name, {'verbete': verbete})
