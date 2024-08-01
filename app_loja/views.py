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
    
    return render(request, 'lista_categorias.html', context)


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
    pedido =  models.Pedido.objects.filter(cliente = request.user.cliente, status = 'Aberto').first()
    return render(request, 'app_loja/ver_carrinho.html', {'pedido': pedido})



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