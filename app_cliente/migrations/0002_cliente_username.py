# Generated by Django 5.0.7 on 2024-07-31 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_cliente', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='username',
            field=models.CharField(default='', max_length=1),
        ),
    ]
