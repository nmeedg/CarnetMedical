# Generated by Django 5.0.1 on 2024-04-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_alter_examen_date_fin'),
    ]

    operations = [
        migrations.AddField(
            model_name='hopital',
            name='contact',
            field=models.CharField(default='+237 99 99 99 00', max_length=50),
        ),
    ]