from django.db import models
from apps.veiculo.models import *
from apps.accounts.models import *
from apps.proprietario.models import *

# Create your models here.


class VerbeteCarta(models.Model):
    CATEGORIA_CHOICES = (
        ('1','Lig Amador'),
        ('2','Ligerio Profissional'),
        ('3','Pesado')
    )
    numero_carta = models.CharField(max_length=20, unique=True)
    data_emissao = models.DateTimeField(auto_now = True)
    data_validade = models.DateField()
    estado = models.BooleanField(default=True)
    categoria = models.CharField(max_length=1, choices=CATEGORIA_CHOICES, default='1')
    proprietario = models.OneToOneField(Proprietario, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='qr_codes/carta', blank=True)

class VerbeteViatura(models.Model):
    registo_inicial = models.OneToOneField(RegistoInicial, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField(auto_now = True)
    data_validade = models.DateField()
    estado = models.BooleanField(default=True)
    qr_code = models.ImageField(upload_to='qr_codes/viatura', blank=True)

class HistoricoVerbeteCarta(models.Model):
    verbete = models.ForeignKey(VerbeteCarta, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField(auto_now = True)
    data_validade = models.DateField()
    estado = models.BooleanField(default=True)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)

class HistoricoVerbeteViatura(models.Model):
    verbete = models.ForeignKey(VerbeteViatura, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField(auto_now = True)
    data_validade = models.DateField()
    estado = models.BooleanField(default=True)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)