from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_categorias, name = 'categorias'),   # localhost:8000
    path('produto/<int:id>/', views.detalhe_produto, name = 'detalhe_produto'),   # localhost:8000/produto/id
    path('adicionar_ao_carrinho/<int:id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),  # localhost:8000/adicionar_ao_carrinho/id
    path('carrinho/', views.ver_carrinho, name = 'ver_carrinho'),   # localhost:8000/carrinho
    path('resultado_produto/', views.resultado_produto, name='resultado_produto'),   # localhost:8000/resultado_produto
    path('produtos/categoria/<str:categoria_nome>/', views.lista_produtos, name='lista_produtos_categoria')   # localhost:8000/produtos/categoria/nomedacategoria
]