import django.http
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from patient.models import Hopital, Service
import json
from patient.views import str_to_date
from rest_framework.decorators import api_view

@api_view(['POST'])
def nouvelHopital(request):
    try:
        data = json.loads(request.body)
        date = str_to_date(data['date'])
        print(date)
        hop = Hopital(nom=data['nom'], lieux=data["lieux"],
                      date_de_creation=date,
                      password=data['password'],
                      matricule=data["directeur"],
                      contact=data['contact'],
                      )
        hop.save()
        response = {'response': True}
    except:
        response = {'response': False}
    return django.http.JsonResponse(response)


def ajouterService(request, id):
    try:
        data = json.loads(request.body)
        ser = Service.objects.create(
            nom=data['nom'],
            description=data['description'])
        ser.hopitals.add(Hopital.objects.get(id=id))
        response = {'response': True}
    except:
        response = {'response': False}
    return django.http.JsonResponse(response)

@api_view(['POST'])
def sign_in(request):
    data = json.loads(request.body)
    print(data)
    k = Hopital.objects.all().filter(password=data['password'], matricule=data['matricule'])
    try:
        v = k[0]
        v.connexion = True
        v.save()
        id1 = v.id
        print(id1)
        return JsonResponse({'id': v.id})
    except:
        return JsonResponse({'id':-1})


def deconnect(request, id_hopital):
    try:
        user = get_object_or_404(Hopital, pk=id)
        user.connexion = False
        user.save()
        return JsonResponse({'response': True})
    except:
        return JsonResponse({'response':False})