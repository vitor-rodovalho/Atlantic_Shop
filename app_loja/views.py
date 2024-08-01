from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth.decorators import login_required
from django.conf import settings


def lista_produtos(request, categoria_nome):
    print(categoria_nome)
    subcategoria_lista = []
    for categoria, subcategorias in categorias:
        if categoria == categoria_nome:
            subcategoria_lista = subcategorias
            break

    # Filtra os produtos que pertencem às subcategorias
    produtos = models.Produto.objects.filter(subcategoria__in=subcategoria_lista)
    print(f"Subcategorias usadas para filtro: {subcategoria_lista}")
    print(f"Quantidade de produtos encontrados: {produtos.count()}")
    
    # Renderizar o template com os produtos filtrados
    return render(request, 'app_loja/produtos.html', {'produtos': produtos, 'categoria_nome': categoria_nome})



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
            #         title, imgUrl, price, categoryName = linha

            #         # Criamos um novo produto
            #         produto = models.Produto.objects.create(
            #             nome=title,  # Aqui usamos title para nome
            #             imgUrl=imgUrl,
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

def lista_categorias(request):
    
    context = {
        'categorias': categorias
    }

    return render(request, 'app_loja/lista_categorias.html', context)

categorias = [
    ("acessorios-e-artigos", [
        "Acessórios de Ferramentas Elétricas",
        "Acessórios e Artigos Eletrônicos",
        "Acessórios e Peças para Motos",
        "Acessórios para Celular",
        "Acessórios para Computador",
        "Acessórios para Gatos",
        "Acessórios para Home Theater",
        "Acessórios para Viagem",
        "Carregadores de Celular",
        "Drones e Acessórios",
        "Impressoras e Acessórios",
        "Jogos e Acessórios",
        "Peças e Acessórios para Automóveis",
        "Peças e Componentes de Computador",
        "Produtos para Câmeras e Foto",
        "Telefones e Acessórios"
    ]),
    
    ("moda-e-acessorios-pessoais", [
        "Achados em Moda",
        "Beleza",
        "Bolsas",
        "Bolsas de Mão e Ombro Femininas",
        "Bolsas e Mochilas Escolares",
        "Compras Internacionais em Moda",
        "Feminino",
        "Maquiagem",
        "Masculino",
        "Meninas",
        "Meninos",
        "Mochilas",
        "Moda",
        "Moda Masculina",
        "Roupas Íntimas para Incontinência",
        "Roupas, Calçados e Joias"
    ]),
    
    ("bebes-e-criancas", [
        "Alimentação de Bebês e Crianças Pequenas",
        "Banho, Higiene e Troca de Fraldas do Bebê",
        "Bebês",
        "Chupetas e Mordedores",
        "Diversão e Atividades para Bebês",
        "Papinhas de Bebê",
        "Produtos de Passeio e Viagem para Bebês",
        "Produtos para a Segurança do Bebê",
        "Troca de Fraldas do Bebê"
    ]),
    
    ("alimentos-e-bebidas", [
        "Alimentos e Bebidas",
        "Bebidas Alcoólicas",
        "Café, Chá e Expresso",
        "Café, Chá e outras Bebidas",
        "Cereal de Café da Manhã",
        "Cerveja",
        "Gin",
        "Grãos Secos, Arroz e Massas",
        "Lanches e Doces",
        "Molhos e Condimentos",
        "Vodka",
        "Whisky",
        "Óleos, Azeites, Vinagres e Molhos para Salada"
    ]),
    
    ("casa-e-cozinha", [
        "Ar e Ventilação",
        "Assadeiras, Fôrmas e Recipientes de Forno",
        "Casa",
        "Casa Inteligente",
        "Cozinha",
        "Cortinas e Persianas",
        "Iluminação",
        "Instalações de Cozinha e Banheiro",
        "Móveis e Acessórios para Jardim e Quintal",
        "Móveis e Decoração",
        "Móveis para Escritório",
        "Organização e Armazenamento para Casa",
        "Panelas e Utensílios para Cozinhar",
        "Produtos de Decoração para Casa",
        "Produtos de Limpeza",
        "Produtos de Limpeza para Casa",
        "Talheres",
        "Utensílios de Cozinha",
        "Utensílios de Limpeza"
    ]),
    
    ("ferramentas-e-equipamentos", [
        "Ferramentas Elétricas",
        "Ferramentas Manuais",
        "Ferramentas de Medição",
        "Ferramentas e Equipamentos Automotivos",
        "Ferramentas e Materiais de Construção",
        "Organizador de Ferramentas"
    ]),
    
    ("esporte-e-lazer", [
        "Automotivo",
        "Bonecas e Acessórios",
        "Brinquedos de Construir e de Montar",
        "Brinquedos e Jogos",
        "Brinquedos para Faz de Conta e Casinha",
        "Colecionáveis e Miniaturas para Hobby",
        "Esportes com Raquete",
        "Esportes e Aventura",
        "Esportes e Brincadeiras ao Ar Livre",
        "Equipamento de Ciclismo",
        "Equipamento de Natação",
        "Equipamento para Exercícios e Academia",
        "Equipamento para Trilha e Acampamento",
        "Jardinagem, Ferramentas e Rega para Jardim",
        "Material de Futebol",
        "Skates, Patins, Patinetes e Acessórios"
    ]),
    
    ("eletronicos-e-tecnologia", [
        "Celulares e Comunicação",
        "Celulares e Smartphones",
        "Computadores Desktop",
        "Computadores e Informática",
        "Eletrônicos",
        "Eletrônicos e Aparelhos",
        "Eletrônicos e Tecnologia Automotivos",
        "Eletrônicos e Tecnologia para Escritório",
        "Equipamento Elétrico",
        "Fire TV Stick Apps",
        "Fragmentadoras",
        "Memória e Armazenamento de Dados",
        "Monitores de Computador",
        "Notebooks",
        "Roteadores, Modems e Dispositivos de Rede",
        "Tablets",
        "Wearables e Tecnologia Vestível"
    ]),
    
    ("livros-e-midia", [
        "Apps e Jogos",
        "Audiolivros Audible",
        "CD e Vinil",
        "Didáticos e Escolares",
        "Filmes",
        "HQs, Mangás e Graphic Novels",
        "Livros",
        "Livros Infantis",
        "Livros Universitários, Técnicos e Profissionais",
        "Livros em Oferta",
        "Loja Kindle",
        "Música Nacional",
        "Programas de TV",
        "eBooks Gratuitos",
        "eBooks Kindle"
    ]),
    
    ("cuidados-pessoais-e-saude", [
        "Desodorantes e Antitranspirantes",
        "Produtos de Bem-Estar Sexual",
        "Produtos de Corpo e Banho",
        "Produtos de Cuidados com a Pele",
        "Produtos de Higiene Bucal",
        "Produtos de Manicure e Pedicure",
        "Produtos de Proteção do Sol e Bronzeadores",
        "Produtos para Cuidados com o Rosto",
        "Saúde e Cuidados Pessoais",
        "Vitaminas, Minerais e Suplementos"
    ]),
    
    ("pet-shop", [
        "Acessórios para Gatos",
        "Produtos para Aves e Pássaros",
        "Produtos para Cães",
        "Produtos para Roedores e Pequenos Animais",
        "Produtos para Répteis e Anfíbios",
        "Peixes e Animais Aquáticos"
    ]),
    
    ("jogos-e-consoles", [
        "Nintendo Switch, Jogos, Consoles e Acessórios",
        "PlayStation 4, Jogos, Consoles e Acessórios",
        "PlayStation 5, Jogos, Consoles e Acessórios",
        "Xbox One, Jogos, Consoles e Acessórios",
        "Xbox Series X e S, Jogos, Consoles e Acessórios"
    ])
]