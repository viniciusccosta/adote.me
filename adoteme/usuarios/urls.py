from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/'   , views.entrar  , name='login'),
    path('logout/'  , views.sair    , name='logout'),
]
