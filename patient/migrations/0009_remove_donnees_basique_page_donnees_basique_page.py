# Generated by Django 5.0.1 on 2024-04-28 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0008_alter_donnees_basique_poids_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donnees_basique',
            name='page',
        ),
        migrations.AddField(
            model_name='donnees_basique',
            name='page',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='patient.page_carnet'),
        ),
    ]
