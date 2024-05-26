# Generated by Django 5.0.1 on 2024-04-29 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_examen_nom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examen',
            name='conclusion',
            field=models.TextField(default='en cours ...'),
        ),
        migrations.AlterField(
            model_name='examen',
            name='nom',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='examen',
            name='type',
            field=models.CharField(max_length=60, null=True),
        ),
    ]