# Generated by Django 3.1.13 on 2021-10-19 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proprietario', '0002_auto_20211016_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proprietario',
            name='data_registo',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
