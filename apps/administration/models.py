from django.db import models

from apps.accounts.models import User

# Create your models here.
class Investidor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Empreendidor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Startup(models.Model):
    nome = models.CharField(max_length=100)
    empreendidor = models.ForeignKey(Empreendidor, on_delete=models.CASCADE)

class Investimento(models.Model):
    PENDENTE = 'p'
    CONFIRMADO = 'c'
    STATUS_INVESTIMENTO = (
        (PENDENTE, 'Pendente'),
        (CONFIRMADO, 'Confirmado'),
    )

    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    obs = models.TextField(max_length=500)
    investidor = models.ForeignKey(Investidor, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_INVESTIMENTO, default=PENDENTE)