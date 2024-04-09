from django.db import models
from apps.accounts.models import *

# Create your models here.

class Proprietario(models.Model):
    pessoa = models.OneToOneField(Pessoa, primary_key=True, on_delete=models.CASCADE, related_name='pessoa_proprietario_id')
    data_registo = models.DateTimeField(auto_now=True)
    operador = models.ForeignKey(User, on_delete=models.CASCADE,related_name='pessoa_operador_id')

    def __str__(self):
        return "{}".format(self.pessoa)