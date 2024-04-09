from django.db import models
from apps.accounts.models import *
from apps.proprietario.models import *

# Create your models here.

class Marca(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Cor(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.nome

class Modelo(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class RegistoInicial(models.Model):
    TIPO_VEICULO_CHOICES = (
        ('1', 'Ligerio'),
        ('2', 'Pesado')
	)
    numero_motor = models.CharField(max_length=20, unique=True)
    numero_quadro = models.CharField(max_length=20, unique=True)
    matricula = models.CharField(max_length=20, unique=True)
    lotacao = models.PositiveIntegerField()
    tipo_veiculo = models.CharField(max_length=1, choices=TIPO_VEICULO_CHOICES, default='1')
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    cor = models.ForeignKey(Cor, on_delete=models.CASCADE)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    data_registo = models.DateTimeField(auto_now = True)

    def __str__(self):
        return "{} - {}".format(self.pk,self.proprietario)
