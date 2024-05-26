# Generated by Django 5.0.1 on 2024-04-28 05:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField(default=' lol ')),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Carnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField(auto_now=True, verbose_name='cree le')),
                ('derniere_visite', models.DateField(auto_now_add=True, null=True, verbose_name='derniere visite')),
            ],
        ),
        migrations.CreateModel(
            name='examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=60)),
                ('parametres', models.TextField()),
                ('conclusion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Hopital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_de_creation', models.DateField(auto_created=True)),
                ('nom', models.CharField(max_length=50)),
                ('lieux', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=104)),
                ('directeur', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expediteur_id', models.IntegerField()),
                ('recepteur', models.IntegerField()),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quartier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='nom de la ville')),
            ],
        ),
        migrations.CreateModel(
            name='Ville',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='nom de la ville')),
            ],
        ),
        migrations.CreateModel(
            name='donnees_basique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('traitement_actuels', models.TextField()),
                ('groupe_sanguin', models.CharField(default='B', max_length=2)),
                ('rhesus', models.CharField(default='-', max_length=1)),
                ('drepanocythose', models.CharField(max_length=2, null=True)),
                ('poids', models.CharField(max_length=6)),
                ('taille', models.TextField(max_length=6)),
                ('maladies', models.TextField()),
                ('handicap', models.TextField()),
                ('allergies', models.ManyToManyField(to='patient.allergie')),
            ],
        ),
        migrations.AddField(
            model_name='allergie',
            name='patients',
            field=models.ManyToManyField(to='patient.donnees_basique'),
        ),
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=60)),
                ('views', models.ImageField(upload_to='')),
                ('exam', models.ManyToManyField(to='patient.examen')),
            ],
        ),
        migrations.AddField(
            model_name='examen',
            name='img',
            field=models.ManyToManyField(to='patient.image'),
        ),
        migrations.CreateModel(
            name='page_carnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now=True)),
                ('observation', models.TextField()),
                ('images', models.BinaryField(null=True)),
                ('remarque', models.TextField()),
                ('conclusion', models.TextField()),
                ('carnet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.carnet')),
                ('examens', models.ManyToManyField(to='patient.examen')),
            ],
        ),
        migrations.AddField(
            model_name='examen',
            name='pages_carnet',
            field=models.ManyToManyField(to='patient.page_carnet'),
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='nom')),
                ('surname', models.CharField(max_length=64, verbose_name='prenom')),
                ('password', models.CharField(max_length=104)),
                ('ddn', models.DateField(null=True)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('post', models.CharField(max_length=50)),
                ('specialite', models.CharField(max_length=50)),
                ('autre_fonction', models.JSONField(null=True)),
                ('experiences', models.IntegerField()),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.hopital')),
            ],
        ),
        migrations.CreateModel(
            name='patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='nom')),
                ('surname', models.CharField(max_length=64, verbose_name='prenom')),
                ('password', models.CharField(max_length=104, verbose_name='mot de passe')),
                ('username', models.CharField(max_length=64, verbose_name='nom utilisateur')),
                ('connexion', models.BooleanField(default=False)),
                ('ddn', models.DateField(null=True)),
                ('img', models.ImageField(null=True, upload_to='')),
                ('numero', models.CharField(max_length=50, verbose_name='numero personnel')),
                ('numero_urgence', models.CharField(max_length=50)),
                ('nationalite', models.CharField(max_length=30)),
                ('celibataire', models.BooleanField(default=True, verbose_name='marie ?')),
                ('sexe', models.CharField(default='M', max_length=1)),
                ('addresse_email', models.CharField(default='flashmac402@gmail.com', max_length=100)),
                ('carnet', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='patient.carnet')),
                ('quartier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.quartier')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default='pediatrie', max_length=60)),
                ('description', models.TextField(default='aucune')),
                ('hopitals', models.ManyToManyField(to='patient.hopital')),
            ],
        ),
        migrations.CreateModel(
            name='symptome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(default='aucune')),
                ('duration', models.CharField(max_length=50, null=True)),
                ('intensity', models.CharField(max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('page_carnets', models.ManyToManyField(to='patient.page_carnet')),
            ],
        ),
        migrations.AddField(
            model_name='page_carnet',
            name='symptomes',
            field=models.ManyToManyField(to='patient.symptome'),
        ),
        migrations.AddField(
            model_name='quartier',
            name='ville',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='patient.ville'),
        ),
    ]