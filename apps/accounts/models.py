from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

TIPO_PESSOA_CHOICES = [
    ('1', 'Pessoa Física'),
    ('2', 'Pessoa Jurídica'),
]
 
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):

        if not username:
            raise ValueError('É necessário preencher o campo usuário')

        # identifier = self.normalize_email(identifier)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):

        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser need to be is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser need to be is_staff=True')

        return self._create_user(username, password, **extra_fields)

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    tipo_pessoa = models.CharField(max_length=1, choices=TIPO_PESSOA_CHOICES, default='1')
    numero_identificacao=models.CharField(max_length=50,unique=True, blank=True, null=True)
    data_criacao = models.DateTimeField(editable=False, default=timezone.now)
    data_edicao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nome

class PessoaFisica(models.Model):
    pessoa_id = models.OneToOneField(Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='pessoa_fis_info')
    data_nascimento = models.DateField(null=True, blank=True)
            
class PessoaJuridica(models.Model):
    pessoa_id = models.OneToOneField(
        Pessoa, on_delete=models.CASCADE, primary_key=True, related_name='pessoa_jur_info')
    responsavel = models.CharField(max_length=32, null=True, blank=True)

    @property
    def format_responsavel(self):
        if self.responsavel:
            return 'Representante: {}'.format(self.responsavel)
        else:
            return ''

class User(AbstractUser):

    DEPARTMENT_CHOICES = (
        ('1', 'Chefe do Departamento'),
        ('2', 'Inspector'),
        ('3', 'Super User'),
    )

    is_staff = models.BooleanField(default=True)
    department = models.CharField(
        max_length=3,
        choices=DEPARTMENT_CHOICES,
        default='1'
    )
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'department']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name']

    def __str__(self):
        return self.username

    objects = UserManager()