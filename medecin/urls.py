from django.urls import path
from . import views


urlpatterns=[
    path('sign-up/', views.enregistrertMedecin,name='sign-up'),
    path('sign-in/', views.auth, name='auth'),
    path('<int:id_medecin>/newpage/', views.nouvellePage_carnet, name='nouvellePage_carnet'),
    path('<int:id_medecin>/set_info_patient/', views.set_donnees_Basiques, name='set_infos_basique'),
    path('<int:id_medecin>/newsymptom/', views.nouveauSymptome, name='nouveauSymptome'),
    path('<int:id_medecin>/idGet/', views.idGet, name='obtenir lidentifiant'),
    path('<int:id_medecin>/basicInfornmations/', views.getInfoBasic,name='Mes informations'),
    path('<int:id_medecin>/exams/', views.exams_to_do, name='exams'),
    path('<int:id_medecin>/end/', views.end_consultation, name='end_consultation'),
    path('<int:id_medecin>/all_informations/',views.alls_data,name='alls_informations'),
    path('<int:id_medecin>/set_examens/',views.set_examens,name='set_examens'),
    path('<int:id_medecin>/new_allergy/',views.new_allergy,name='set_examens'),
]
