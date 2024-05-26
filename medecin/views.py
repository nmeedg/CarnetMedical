from django.forms import model_to_dict
from django.http import JsonResponse
import json
from patient.models import *
from datetime import datetime, date
from rest_framework.decorators import api_view

@api_view(['POST'])
def enregistrertMedecin(request):
    # On auara besoin de:
    # nomHopital en dernier , et tous les autres autres attributs
    data = dict(json.loads(request.body))
    h = Hopital.objects.get(nom=data['hospital'])
    dat = datetime(year=int(data['year']), month=int(data['month']), day=int(data['day']))
    P = Personnel(
        name=data['name'],
        surname=data['surname'],
        password=data['password'],
        ddn=dat.date(),
        hospital=h,
        addresse_email=data["addresse_email"],
        post=data['post'],
        specialite=data['specialite'],
        experiences=data["experiences"]
    )
    P.save()
    return JsonResponse({'response': True})

@api_view(['POST'])
def auth(request):
    try:
        data = json.loads(request.body)
        for med in Personnel.objects.all():
            if data['addresse_email'] == med.addresse_email and data['password'] == med.password:
                med.connexion = True
                med.save()
                return JsonResponse({'id': med.id})
    except:
        return JsonResponse({'id': -1})


def nouvellePage_carnet(request, id_medecin):
    data = json.loads(request.body)
    med = Personnel.objects.get(id=id_medecin)
    try:
        user = patient.objects.get(id=data['id'])
        print(user)
    except:
        user = patient.objects.get(username=data['username'], password=data['password'])
    Page = page_carnet(
        title=data["title"],
        carnet=user.carnet,
        medecin_en_charge=med,
    )
    user.carnet.derniere_visite = datetime.today().date()
    user.carnet.save()
    Page.save()
    return JsonResponse({'id': Page.id})


def set_donnees_Basiques(request, id_medecin):
    data = json.loads(request.body)
    try:
        user = patient.objects.get(id=data['id'])
    except:
        try:
            user = patient.objects.get(username=data['username'], pasword=data['pasword'])
        except:
            return JsonResponse({'reponse': "ce patient n'a pas de compte"})
    try:
        info = donnees_basique(
            traitement_actuels=data['traitement_actuels'],
            groupe_sanguin=data['groupe_sanguin'],
            rhesus=data['rhesus'],
            drepanocythose=data['drepanocythose'],
            poids=data['poids'],
            page=user.carnet,
            taille=data["taille"],
            maladies=data['maladies'],
            handicap=data['handicap']
        )
        info.save()
        return JsonResponse({'response': True})
    except:
        return JsonResponse({'response': False})


def nouveauSymptome(request, id_medecin):
    data = json.loads(request.body)
    try:
        symp = symptome(
            name=data['name'],
            description=data['description'],
            page=page_carnet.objects.get(id=data['id_carnet']),
            medecin=Personnel.objects.get(id=id_medecin))
        symp.page.carnet.derniere_visite = datetime.today().date()
        symp.page.carnet.save()
        symp.save()
        return JsonResponse({'response': True})
    except:
        return JsonResponse({'response': False})


def idGet(request, id_medecin):
    data = json.loads(request.body)
    P = patient.objects.get(username=data['username'], password=data['password'])
    return JsonResponse({'id': P.id})

@api_view(['POST'])
def getInfoBasic(request, id_medecin):
    data = json.loads(request.body)
    try:
        P = patient.objects.get(id=data['id'])
    except:
        P = patient.objects.get(username=data['username'], password=data['password'])
    carn = P.carnet
    fast_data = donnees_basique.objects.get(page=carn)
    data1 = model_to_dict(fast_data, exclude=['page'])
    list_allergies = Allergie.objects.all().filter(page=fast_data)
    if len(list_allergies) != 0:
        allergies = ''
        for allergie in list_allergies:
            allergies = f'{allergies}  {str(allergie.name)},'
        data2 = {'allergies': allergies}
    else:
        data2 = {'allergies': 'aucune'}
    data3 = {**data1, **data2}
    return JsonResponse(data3)


def exams_to_do(request, id_medecin):
    data = json.loads(request.body)
    for exam in data['examens']:
        a = examen.objects.create(nom=exam, page=page_carnet.objects.get(id=data['id_page_carnet']))
    return JsonResponse({'response': True})


def end_consultation(request, id_medecin):
    data = json.loads(request.body)
    if data == {}:
        return JsonResponse({'response': True})
    else:
        page_en_consultation = page_carnet.objects.get(id=data['id_page_carnet'])
        page_en_consultation.observation = data['observation']
        page_en_consultation.conclusion = data['conclusion']
        page_en_consultation.carnet.derniere_visite = datetime.today().date()
        page_en_consultation.carnet.save()
        page_en_consultation.save()
        basic_data = donnees_basique.objects.get(page=page_en_consultation.carnet)
        basic_data.traitement_actuels = data['conclusion']
        basic_data.save()
        return JsonResponse({'response': True})


def alls_data(request, id_medecin):
    # On prend en parametre le nom d'utilisateur et le mot de passe ou l'id
    data = json.loads(request.body)
    try:
        user = patient.objects.get(id=data['id_patient'])
    except:
        user = patient.objects.get(username=data["username"], pasword=data['password'])
    # Obtenir le carnet du patient
    carn = user.carnet
    # Obtenir toutes les pages liés aux carnets
    Page = page_carnet.objects.all().filter(carnet=carn)
    donneesB = donnees_basique.objects.get(page=carn)
    allerG = donneesB.allergie_set.all()
    exam = []
    for element in Page:
        exam.append(examen.objects.all().filter(page=element))
    symp = []
    for element in Page:
        symp.append(symptome.objects.all().filter(page=element))
    print(symp)
    dictpage = {}
    for n in range(len(Page)):
        temp = {}
        temp['title'] = Page[n].title
        temp['medecin_en_charge'] = f'{Page[n].medecin_en_charge.name}, {Page[n].medecin_en_charge.post}'
        temp['date'] = Page[n].date
        temp['hopital'] = Page[n].medecin_en_charge.hospital.nom
        dictpage[f'page{n}'] = temp

    dicExam = {}
    i = 0
    print(type(exam[0]))
    for j in range(len(exam)):
        for elt in exam[j]:
            i += 1
            temp = {}
            temp['nom'] = elt.nom
            temp['type'] = elt.type
            temp['parametres'] = elt.parametres
            temp['conclusion'] = elt.conclusion
            temp['date_de_debut'] = elt.date_de_debut
            temp['nomMedecin'] = elt.page.medecin_en_charge.name
            temp['date_fin'] = elt.date_fin

            dicExam[f'examen{i}page{j + 1}'] = temp
    dicSymp = {}
    k = i
    for j in range(1, len(symp) + 1):
        for elt in symp[j - 1]:
            i += 1
            temp = {}
            temp['name'] = elt.name
            temp['description'] = elt.description
            temp['duration'] = elt.duration
            temp['intensity'] = elt.intensity
            temp['date'] = elt.date
            temp['nomMedecin'] = elt.medecin.name
            dicSymp[f'symptome{i - k}page{j}'] = temp
    k = i
    dicAllergie = {}
    for elt in allerG:
        i += 1
        temp = {}
        temp['name'] = elt.name
        temp['description'] = elt.description
        temp['type'] = elt.type
        dicAllergie[f'allergie{i - k}'] = temp
    dicFinal = {**dictpage, **dicSymp, **dicExam, **dicAllergie}
    return JsonResponse(dicFinal)


def set_examens(request, id_medecin):
    try:
        data = json.loads(request.body)
        this_page = page_carnet.objects.get(id=data['id_page_carnet'])
        exam = examen.objects.get(page=this_page, nom=data['nom'])
        exam.date_fin = datetime.now()
        exam.conclusion = data['conclusion']
        exam.save()
        return JsonResponse({'response': True})
    except:
        return JsonResponse({'response': False})


def new_allergy(request, id_medecin):
    data = json.loads(request.body)
    user = patient.objects.get(id=data['id_patient'])
    basic = donnees_basique.objects.get(page=user.carnet)
    new = Allergie(name=data['name'])
    new.save()
    new.page.add(basic)
    return JsonResponse({'response': True})
