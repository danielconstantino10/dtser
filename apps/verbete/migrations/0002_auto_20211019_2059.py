# Generated by Django 3.1.13 on 2021-10-19 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proprietario', '0002_auto_20211016_1803'),
        ('verbete', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verbetecarta',
            name='proprietario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='proprietario.proprietario'),
        ),
    ]
