from django.shortcuts import render, get_object_or_404, redirect
from app_loja import models
from django.contrib.auth.decorators import login_required
from vertexai.generative_models import GenerativeModel
from django.contrib import messages
import vertexai
import sqlite3
from app_loja.models import Produto

produtos_cache = []

def lista_categorias(request):
    
    context = {
        'categorias': categorias
    }
    
    return render(request, 'app_loja/lista_categorias.html', context)

def lista_produtos(request, categoria_nome):
    subcategoria_lista = []
    for categoria, subcategorias in categorias:
        if categoria == categoria_nome:
            subcategoria_lista = subcategorias
            break

    # Filtra os produtos que pertencem às subcategorias
    produtos = models.Produto.objects.filter(subcategoria__in=subcategoria_lista)
    
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
    

def busca_produtos_db():
    db_nome = 'C:\\Users\\vitor\\OneDrive\\Área de Trabalho\\Atlantic_Shop\\db.sqlite3'
    conexao_db = sqlite3.connect(db_nome)

    global produtos_cache

    # Se os produtos já tiverem sido buscados no banco de dados, os retorna
    if produtos_cache:
        return produtos_cache

    cursor = conexao_db.cursor()

    # Consulta SQL para buscar todos produtos
    query = "SELECT id, nome, subcategoria FROM Produto"
    cursor.execute(query)
    produtos = cursor.fetchall()

    conexao_db.close()

    produtos_cache = produtos
    return produtos_cache

def generate(input_usuario: str):
    # Inicializando o cliente do Vertex AI
    project_id = "atlantic-shop-431022"
    location = "us-central1"  
    model_id = "gemini-1.5-flash-001"  

    generation_config = {
        "max_output_tokens": 35,
        "temperature": 1,
        "top_p": 0.7,
    }

    produtos = busca_produtos_db()

    prompt = f"""Dada uma pesquisa de produto que informa o nome ou característica dele, me retorne, separado por virgula, apenas o ID e a subcategoria do produto que mais se assemelha à pesquisa do input, sem qualquer informação adicional. Por favor, preste atenção ao contexto.
    
    Os produtos estão separados no formato (ID, nome, subcategoria) e são os seguintes:
    {produtos}
        
    Exemplo de busca: {input_usuario}"""

    # Inicializa o cliente do Vertex AI
    vertexai.init(project=project_id, location=location)
    
    # Cria uma instância do modelo
    model = GenerativeModel(model_id)
    
    # Gera o conteúdo com o modelo
    resposta = model.generate_content(
        [prompt],
        generation_config=generation_config,
        stream = False,
    )

    if resposta:
        resposta = resposta.text.split(',')
        produto_selecionado_ID = resposta[0].strip()
        produto_selecionado_Subcategoria = resposta[1].strip()
        return produto_selecionado_ID, produto_selecionado_Subcategoria
    
    return None, None

def resultado_produto(request):
    input_usuario = request.GET.get('query', '')

    if input_usuario:
        produto_selecionado_ID, produto_selecionado_Subcategoria = generate(input_usuario)
        
        # Busca o produto no banco de dados conforme o ID
        if produto_selecionado_ID:
            conexao_db = sqlite3.connect('db.sqlite3')
            cursor = conexao_db.cursor()
            query_produto = "SELECT id, nome, preco, imgUrl, subcategoria FROM Produto WHERE id = ?"
            cursor.execute(query_produto, (produto_selecionado_ID,))
            produto_selecionado_data = cursor.fetchone()
            conexao_db.close()

            if produto_selecionado_data:
                produto_selecionado = Produto(
                    id=produto_selecionado_data[0],
                    nome=produto_selecionado_data[1],
                    preco=produto_selecionado_data[2],
                    imgUrl=produto_selecionado_data[3],
                    subcategoria=produto_selecionado_data[4]
                )
            
                # Busca produtos da mesma subcategoria para serem recomendados
                conexao_db = sqlite3.connect('db.sqlite3')
                cursor = conexao_db.cursor()
                query_similares = "SELECT id, nome, preco, imgUrl, subcategoria FROM Produto WHERE subcategoria = ? AND id != ? ORDER BY RANDOM() LIMIT 6"
                cursor.execute(query_similares, (produto_selecionado.subcategoria, produto_selecionado.id))
                produtos_similares_data = cursor.fetchall()   
                conexao_db.close()

                produtos_similares = [
                    Produto(
                        id=produto[0],
                        nome=produto[1],
                        preco=produto[2],
                        imgUrl=produto[3],
                        subcategoria=produto[4]
                    )
                    for produto in produtos_similares_data
                ]

                context = {
                    'produto_selecionado': produto_selecionado,
                    'produtos_similares': produtos_similares,
                }

                return render(request, 'app_loja/resultado_produto.html', context)
            
        messages.error(request, "Nenhum produto encontrado.")
        return redirect('categorias')
    
    messages.error(request, "Nenhuma consulta recebida.")
    return redirect('categorias')


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