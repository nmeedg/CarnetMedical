# Generated by Django 5.0.1 on 2024-04-29 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0020_rename_directeur_hopital_matricule_hopital_connexion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='date_de_debut',
            field=models.DateTimeField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='examen',
            name='date_fin',
            field=models.DateTimeField(null=True),
        ),
    ]
