# URLs específicas da parte da loja, exibição de produtos e página inicial

from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name = 'lista_produtos'),   # localhost:8000
    path('produto/<int:id>/', views.detalhe_produto, name = 'detalhe_produto'),   # localhost:800/produto/id
    path('adicionar_ao_carrinho/<int:id>/', views.adicionar_ao_carrinho, name = 'adicionar_ao_carrinho'),   # localhost:800/adicionar_ao_carrinho/id
    path('carrinho/', views.ver_carrinho, name = 'ver_carrinho'),   # localhost:800/carrinho
]