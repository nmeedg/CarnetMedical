from django.urls import path
from . import views
urlpatterns = [
    path('sign-up/', views.nouvelHopital,name='nouveau hopital'),
    path('sign-in/', views.sign_in,name='connection'),
    path('<int:id_hopital>/deconnexion/', views.sign_in,name='connection'),
    path('user/<int:id_hopital>/service/new/', views.ajouterService, name='nouveau service'),
    ]