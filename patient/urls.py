from django.urls import path
from . import views
base_dir_home = 'user/<int:id>/'
base_dir_set = base_dir_home + 'set/'
urlpatterns = [
    path('sign-up/', views.sign_up, name='inscription'),
    path('sign-in/', views.auth, name='auth'),
    path(base_dir_home, views.home, name='home'),
    path(base_dir_home+'qrcode/', views.get_qr, name='get_qrcode'),
    path('user/<int:id>/deconnexion/', views.deconnect, name='deconnect'),
    path(base_dir_set + 'password/', views.set_password, name='set_password'),
    path(base_dir_set+'username/', views.set_username, name='username'),
    path(base_dir_home+'mycarnet/', views.alls_data,name='my carnet'),
]
