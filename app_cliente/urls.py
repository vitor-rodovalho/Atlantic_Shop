from django.urls import path
from app_cliente import views
from django.contrib.auth import views as auth_views
from django.shortcuts import render

urlpatterns = [
    path('', views.visualizar, name = 'visualizar_cliente'),   # localhost:8000/cliente
    path('login/', auth_views.LoginView.as_view(template_name='app_cliente/registration/login.html'), name='login'),   # localhost:8000/cliente/login
    path('cadastro/', views.cadastro, name = 'cadastro_cliente'),  # localhost:8000/cliente/cadastro
    path('cadastro_concluido/', lambda request: render(request, 'app_cliente/cadastro_concluido.html'), name='cadastro_concluido'),   # localhost:8000/cliente/cadastro_concluido
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),   # localhost:8000/cliente/logout

]