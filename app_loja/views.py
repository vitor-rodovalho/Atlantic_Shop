from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth.decorators import login_required
import csv
import os
from django.conf import settings

def lista_categorias(request):
    categorias = [
        "Acessórios e Artigos",
        "Moda e Acessórios Pessoais",
        "Bebês e Crianças",
        "Alimentos e Bebidas",
        "Casa e Cozinha",
        "Ferramentas e Equipamentos",
        "Esporte e Lazer",
        "Eletrônicos e Tecnologia",
        "Livros e Mídia",
        "Cuidados Pessoais e Saúde",
        "Pet Shop",
        "Jogos e Consoles"
    ]
    
    context = {
        'categorias': categorias
    }
    
    return render(request, 'app_loja/lista_categorias.html', context)


def lista_produtos(request):
    produtos = models.Produto.objects.all()
    return render(request, 'app_loja/produtos.html', {'produtos': produtos})

def detalhe_produto(request, id):
    produto = get_object_or_404( models.Produto, id = id)
    return render(request, 'app_loja/detalhe_produto.html', {'produto': produto})

@login_required
def adicionar_ao_carrinho(request, id):
    produto = get_object_or_404( models.Produto, id = id)
    quantidade = int(request.POST.get('quantidade', 1))
    preco_unitario = produto.preco

    item =  models.Item(produto = produto, quantidade = quantidade, preco_unitario = preco_unitario)
    item.save()

    pedido, created =  models.Pedido.objects.get_or_create(cliente = request.user.cliente, status = 'Aberto')
    pedido.itens.add(item)
    pedido.save()

    return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    pedido = models.Pedido.objects.filter(cliente=request.user.cliente, status='Aberto').first()
    return render(request, 'app_loja/ver_carrinho.html', {'pedido': pedido})

@login_required
def finalizar_compra(request):
    pedido = models.Pedido.objects.filter(cliente=request.user.cliente, status='Aberto').first()
    if pedido:
        return redirect('processar_pagamento', pedido_id=pedido.id)  # Redirecionar para a view processar_pagamento com pedido_id
    else:
        return redirect('ver_carrinho')



# def carregar_produtos_csv(request):
#     # Caminho para o arquivo CSV
#     csv_file_path = os.path.join(settings.BASE_DIR, 'static/', 'dataset-teste.csv')

#     if request.method == 'POST':
#         try:
            # # Lemos o conteúdo do CSV
            # with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            #     linhas = csv.reader(csvfile)
                
            #     # Ignora o cabeçalho
            #     next(linhas)

            #     produtos_criados = []
            #     for linha in linhas:
            #         # Extraímos os dados de cada linha
            #         title, imgUrl, stars, reviews, price, categoryName = linha

            #         # Criamos um novo produto
            #         produto = models.Produto.objects.create(
            #             nome=title,  # Aqui usamos title para nome
            #             imgUrl=imgUrl,
            #             stars=float(stars),  # Convertendo estrelas para float, se necessário
            #             reviews=int(reviews),  # Convertendo reviews para int, se necessário
            #             preco=float(price),  # Convertendo price para float
            #             categoria=categoryName  # Usando categoryName para categoria
            #         )
            #         produtos_criados.append(produto.nome)  # Adiciona o nome do produto à lista

            # Obtemos todos os produtos para exibir na tela
    #         produtos = models.Produto.objects.all()
    #         return render(request, 'app_loja/produtos.html', {'produtos': produtos, 'produtos_criados': produtos_criados})

    #     except FileNotFoundError:
    #         return render(request, 'app_loja/produtos.html', {'error': 'Arquivo CSV não encontrado.'})
    #     except Exception as e:
    #         return render(request, 'app_loja/produtos.html', {'error': str(e)})
    
    # return render(request, 'app_loja/produtos.html', {'error': 'Método não permitido.'})



# Script de carregamento de CSV para popular o banco de dados:
# import csv
# from app_loja.models import Produto

# def carregar_csv():
#     with open('path/to/seu_arquivo.csv', 'r') as file:
#         reader = csv.reader(file)
#         next(reader)  # Skip the header row
#         for row in reader:
#             Produto.objects.create(
#                 nome=row[0],
#                 preco=row[1],
#                 categoria=row[2],
#                 subcategoria=row[3],
#                 descricao=row[4],
#                 imagem=row[5]
#             )


# View pra exibir categorias e produtos aleatorios filtrados
# from django.shortcuts import render
# from .models import Produto
# import random

# def lista_categorias(request):
#     return render(request, 'app_loja/lista_categorias.html')

# def lista_produtos(request, categoria):
#     produtos = Produto.objects.filter(categoria=categoria)
#     if produtos.exists():
#         produtos_aleatorios = random.sample(list(produtos), 5)  # Seleciona 5 produtos aleatórios
#     else:
#         produtos_aleatorios = []
#     return render(request, 'app_loja/lista_produtos.html', {'produtos': produtos_aleatorios, 'categoria': categoria})
