"""
URL configuration for Atlantic_Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# O que cada URL vai apresentar, incluindo todas as urls de cada app já separadamente, com o include()
# A página inicial, '', é apresentada pela URL '' do APP loja
urlpatterns = [
    path('admin/', admin.site.urls),   # localhost:8000/admin
    path('', include('app_loja.urls')),  # localhost:8000
    path('cliente/', include('app_cliente.urls')),   # localhost:8000/cliente
    path('pagamento/', include('app_pagamento.urls')),   # localhost:8000/pagamento
]
