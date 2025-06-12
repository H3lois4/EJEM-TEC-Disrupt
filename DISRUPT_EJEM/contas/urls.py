from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.logar, name='login'),
    path('logout/', views.deslogar, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
   
]
