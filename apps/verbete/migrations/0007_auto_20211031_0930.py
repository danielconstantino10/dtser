# Generated by Django 3.1.13 on 2021-10-31 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verbete', '0006_auto_20211031_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verbetecarta',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/carta'),
        ),
        migrations.AlterField(
            model_name='verbeteviatura',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/viatura'),
        ),
    ]
