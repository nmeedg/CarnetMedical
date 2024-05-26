from django.db import models
from datetime import date


class Ville(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='nom de la ville')


class Quartier(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='nom de la ville')
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE, default=0)


class Carnet(models.Model):
    date_creation = models.DateField(verbose_name='cree le',auto_now=True)
    derniere_visite = models.DateField(verbose_name='derniere visite',auto_now_add=True,null=True)


class patient(models.Model):
    name = models.CharField(max_length=64, unique=False, verbose_name='nom')
    surname = models.CharField(max_length=64, unique=False, verbose_name='prenom')
    password = models.CharField(max_length=104, verbose_name='mot de passe')
    username = models.CharField(max_length=64, verbose_name='nom utilisateur')
    connexion = models.BooleanField(default=False)
    ddn = models.DateField(null=True)
    img = models.ImageField(null=True)
    quartier = models.ForeignKey(Quartier, on_delete=models.CASCADE)
    numero = models.CharField(max_length=50, verbose_name='numero personnel')
    numero_urgence = models.CharField(max_length=50)
    carnet = models.OneToOneField(Carnet, on_delete=models.CASCADE)
    nationalite = models.CharField(max_length=30)
    celibataire = models.BooleanField(default=True ,verbose_name='marie ?')
    sexe = models.CharField(default='M',max_length=1)
    addresse_email = models.CharField(default='flashmac402@gmail.com',max_length=100)


class Hopital(models.Model):
    nom = models.CharField(max_length=50)
    lieux = models.CharField(max_length=20)
    date_de_creation = models.DateField(auto_created=True)
    password = models.CharField(max_length=104)
    matricule = models.CharField(max_length=100)
    contact = models.CharField(max_length=50, default='+237 99 99 99 00')
    connexion = models.BooleanField(default=False)


class Service(models.Model):
    nom = models.CharField(max_length=60, default='pediatrie')
    description = models.TextField(default='aucune')
    hopitals = models.ManyToManyField(Hopital)




class Personnel(models.Model):
    name = models.CharField(max_length=64, unique=False, verbose_name='nom')
    surname = models.CharField(max_length=64, unique=False, verbose_name='prenom')
    addresse_email = models.CharField(max_length=100, default='medecin1')
    connexion = models.BooleanField(default=False)
    password = models.CharField(max_length=104)
    ddn = models.DateField(null=True)
    img = models.ImageField(null=True)
    post = models.CharField(max_length=50)
    specialite = models.CharField(max_length=50)
    autre_fonction = models.CharField(null=True,max_length=50)
    hospital = models.ForeignKey(Hopital, on_delete=models.CASCADE)
    experiences = models.IntegerField()


class page_carnet(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    observation = models.TextField(default='RAS')
    carnet = models.ForeignKey(Carnet, on_delete=models.CASCADE)
    conclusion = models.TextField(default='en attente de resultat examen')
    medecin_en_charge = models.ForeignKey(Personnel, on_delete=models.DO_NOTHING, default=0)



class donnees_basique(models.Model):
    page = models.OneToOneField(Carnet, on_delete=models.CASCADE, default=1)
    traitement_actuels = models.TextField()
    groupe_sanguin = models.CharField(max_length=2,default='B')
    rhesus = models.CharField(max_length=1, default='-')
    drepanocythose = models.CharField(max_length=2, null=True)
    poids = models.IntegerField()
    taille = models.IntegerField()
    maladies = models.TextField()
    handicap = models.TextField()

class Allergie(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(default=" aucune ")
    type = models.CharField(max_length=50, default='aucun')
    page = models.ManyToManyField(donnees_basique)


class symptome(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(default='aucune')
    duration = models.CharField(max_length=50,null=True)
    intensity = models.CharField(max_length=50,null=True)
    page = models.ForeignKey(page_carnet, on_delete=models.CASCADE, default=1)
    date = models.DateTimeField(auto_now=True)
    medecin= models.ForeignKey(Personnel,on_delete=models.DO_NOTHING, default=1)


class examen(models.Model):
    nom = models.CharField(max_length=50)
    type = models.CharField(max_length=60, null=True)
    parametres = models.TextField(default='')
    conclusion = models.TextField(default='en cours ...')
    date_de_debut = models.DateTimeField(auto_now=True)
    date_fin = models.DateTimeField(null=True)
    page = models.ForeignKey(page_carnet, on_delete=models.CASCADE, default=1)




class image(models.Model):
    titre = models.CharField(max_length=60)
    views = models.ImageField()
    exam = models.ManyToManyField(examen)


class Message(models.Model):
    expediteur_id = models.IntegerField()
    recepteur = models.IntegerField()
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
