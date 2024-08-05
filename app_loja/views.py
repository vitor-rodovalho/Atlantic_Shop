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
    return render(request, 'app_loja/lista_produtos.html', {'produtos': produtos})

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
    db_nome = 'C:\\Users\\vitor\\OneDrive\\Área de Trabalho\\Atlantic Shop\\Atlantic_Shop\\db.sqlite3'
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
    model_id = "gemini-1.5-pro-001"  

    generation_config = {
        "max_output_tokens": 35,
        "temperature": 0,
        "top_p": 0,
    }

    produtos = busca_produtos_db()

    prompt = f"""Dada uma pesquisa de produto que informa o nome ou característica dele, me retorne, separado por virgula, apenas o ID e a subcategoria do produto que mais se assemelha à pesquisa do input, sem qualquer informação adicional.
    
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