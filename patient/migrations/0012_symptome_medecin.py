# Generated by Django 5.0.1 on 2024-04-28 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_remove_symptome_page_symptome_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='symptome',
            name='medecin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='patient.personnel'),
        ),
    ]