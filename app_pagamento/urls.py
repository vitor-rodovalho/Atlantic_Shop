from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('processar/<int:pedido_id>/', views.processar_pagamento, name='processar_pagamento'),  # localhost:8000/pagamento/processar/id/
    path('concluido/', lambda request: render(request, 'app_pagamento/pagamento_concluido.html'), name='pagamento_concluido'),  # localhost:8000/pagamento/concluido
]
