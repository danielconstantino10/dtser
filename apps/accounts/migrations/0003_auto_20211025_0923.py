# Generated by Django 3.1.13 on 2021-10-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211016_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='tipo_pessoa',
            field=models.CharField(choices=[('1', 'Pessoa Física'), ('2', 'Pessoa Jurídica')], default='1', max_length=1),
        ),
    ]
