# Generated by Django 3.1.13 on 2021-10-16 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211016_1803'),
        ('proprietario', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proprietario',
            name='id',
        ),
        migrations.AlterField(
            model_name='proprietario',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='pessoa_proprietario_id', serialize=False, to='accounts.pessoa'),
        ),
    ]
