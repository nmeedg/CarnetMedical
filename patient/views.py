import base64
import json
from datetime import datetime
import qrcode
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .models import *
from rest_framework.decorators import api_view


def str_to_date(v:str):
    a = v.split('-')
    a = [int(a[i]) for i in range(len(a))]
    date = datetime(a[0], a[1], a[2])
    return date.date()

@api_view(['POST'])
def auth(request):
    content = {'id': -1}
    data = json.loads(request.body)
    password = data['password']
    username = data['username']
    v = patient.objects.all()
    for i in v:
        print(i)
        if i.username == username and i.password == password:
            i.connexion = True
            print(i.connexion)
            i.save()
            return JsonResponse({'id': i.id})
    return JsonResponse(content)


def deconnect(request, id):
    try:
        user = get_object_or_404(patient, pk=id)
        user.connexion = False
        user.save()
        return JsonResponse({'response': True})
    except:
        return JsonResponse({'response':False})


# def sign_up(request):
# template = loader.get_template(('patient/sign_up.html'))
#  return HttpResponse(template.render(request))

@api_view(['GET'])
def home(request, id):
    user = get_object_or_404(patient,  pk=id)

    if user.connexion == True:
        data = model_to_dict(user, exclude=['password','img','quartier'])
        data2 = model_to_dict(get_object_or_404(Carnet, pk=id))
        id_quartier = int(user.quartier.id)
        id_ville= user.quartier.ville.id
        data3 = model_to_dict(get_object_or_404(Quartier, pk= id_quartier), exclude=['ville', 'id'])
        data4 = model_to_dict(get_object_or_404(Ville,pk=id_ville), exclude=['id'])
        return JsonResponse({'user':data, 'carnet':data2, 'quartier': data3, 'ville':data4})
    return JsonResponse({})


def message(request, Test_id):
    data = {}
    list_message = Message.objects.all().filter(recepteur=Test_id).order_by('-date')
    print(list_message)
    i = 0
    for message in list_message:
        data1 = model_to_dict(message)
        data[f'{i}'] = data1
        i +=1
    return JsonResponse(data)


def set_password(request,id):
    data = json.loads(request.body)
    password = data['password']
    new_password = data['new_password']
    user = get_object_or_404(patient, pk=id)
    if user.password == password:
        user.password = new_password
        user.save()
        return JsonResponse({'response': True})
    return JsonResponse({'response': False})


def set_username(request, id):
    try:
        user = get_object_or_404(patient, pk=id)
        data = json.loads(request.body)
        new_username = data['new_username']
        user.username = new_username
        user.save()
        createQR(user.username, user.password, id, patern='patient')
        return JsonResponse({'response': True})
    except:
        return JsonResponse({'response': False})

@api_view(['POST'])
def sign_up(request):
    response = {'response': False}
    data = json.loads(request.body)
    print(data)
    ville = Ville.objects.all().filter(name=data['ville'])
    try:
        quartier = Quartier.objects.get(name=data['quartier'])
    except:
        Quartier.objects.create(name=data['quartier'], ville=ville[0])
        quartier = get_object_or_404(Quartier,name=data['quartier'])
    carnet = Carnet()
    carnet.save()
    carnet.derniere_visite = None
    carnet.save()
    user = patient(name=data['name'],surname= data['surname'], password=data['password'],username=data['username'],
                            numero=data['numero'],sexe=data['sexe'], numero_urgence=data['numero_urgence'],
                            nationalite=data['nationalite'],
                            ddn=str_to_date(data['ddn']),
                            celibataire=data['celibataire'], addresse_email=data['addresse_email'],
                            carnet=carnet, quartier=quartier)
    user.save()
    createQR(data['username'], user.password, user.id)
    response = {'response': True}

    return JsonResponse(response)


def image_to_json(name_image, extension='png'):
    with open(f'{name_image}.{extension}', 'rb') as fic:
        image_data = base64.b64encode(fic.read()).decode('utf-8')
        data = {'image': image_data}
        return data

@api_view(['GET'])
def get_qr(request, id):
    try:
        data = image_to_json(f'qrpatient_{id}')
    except:
        data = {}
    return JsonResponse(data)


def createQR(data1, data2, i, patern='patient'):
    qr = qrcode.QRCode()
    qr.add_data(data1)
    qr.add_data('\n')
    qr.add_data(data2)
    image=qr.make_image()
    image.save(f'qr{patern}_{i}.png')


def alls_data(request, id):
    # On prend en parametre le nom d'utilisateur et le mot de passe ou l'id
    data = json.loads(request.body)
    try:
        user = patient.objects.get(id=id)
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

