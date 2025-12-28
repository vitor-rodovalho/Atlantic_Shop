import vertexai
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from vertexai.generative_models import GenerativeModel

from app_loja import models
from app_loja.constants import CATEGORIAS


PROJECT_ID = settings.VERTEX_PROJECT_ID
LOCATION = settings.VERTEX_LOCATION
MODEL_ID = settings.VERTEX_MODEL_ID

# Cache global simples
produtos_cache = None

def get_produtos_list():
    """Busca ID, Nome e Subcategoria via Django ORM."""
    global produtos_cache
    if produtos_cache is None:
        # values_list é mais performático para prompts de IA
        produtos_cache = list(models.Produto.objects.values_list('id', 'nome', 'subcategoria'))
    return produtos_cache

def generate(input_usuario: str):
    """Integração com Vertex AI para busca semântica."""
    try:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        model = GenerativeModel(MODEL_ID)
        
        produtos = get_produtos_list()
        
        prompt = f"""
        Com base na pesquisa do usuário, identifique o produto mais semelhante.
        Retorne APENAS o ID e a subcategoria no formato: ID, SUBCATEGORIA.
        
        Produtos: {produtos}
        Busca: {input_usuario}
        """

        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 50, "temperature": 0.2}
        )

        if response.text:
            partes = response.text.split(',')
            if len(partes) >= 2:
                return partes[0].strip(), partes[1].strip()
    except Exception as e:
        print(f"Erro Vertex AI: {e}")
    return None, None

# --- Views de Visualização ---

def lista_categorias(request):
    return render(request, 'app_loja/lista_categorias.html', {'categorias': CATEGORIAS})

def lista_produtos(request, categoria_nome):
    subcategorias = next((subs for cat, subs in CATEGORIAS if cat == categoria_nome), [])
    produtos = models.Produto.objects.filter(subcategoria__in=subcategorias)
    return render(request, 'app_loja/produtos.html', {
        'produtos': produtos, 
        'categoria_nome': categoria_nome
    })

def detalhe_produto(request, id):
    produto = get_object_or_404(models.Produto, id=id)
    return render(request, 'app_loja/detalhe_produto.html', {'produto': produto})

# --- Busca por IA ---

def resultado_produto(request):
    query = request.GET.get('query', '')
    if not query:
        messages.error(request, "Por favor, digite algo para buscar.")
        return redirect('categorias')

    p_id, _ = generate(query)
    
    if p_id:
        produto = models.Produto.objects.filter(id=p_id).first()
        if produto:
            # Recomendações: mesma subcategoria, excluindo o atual, em ordem aleatória
            similares = models.Produto.objects.filter(
                subcategoria=produto.subcategoria
            ).exclude(id=produto.id).order_by('?')[:6]

            return render(request, 'app_loja/resultado_produto.html', {
                'produto_selecionado': produto,
                'produtos_similares': similares
            })

    messages.error(request, "Nenhum produto correspondente encontrado.")
    return redirect('categorias')

# --- Fluxo de Carrinho ---

@login_required
def adicionar_ao_carrinho(request, id):
    produto = get_object_or_404(models.Produto, id=id)
    quantidade = int(request.POST.get('quantidade', 1))

    # Cria o item do pedido
    item = models.Item.objects.create(
        produto=produto, 
        quantidade=quantidade, 
        preco_unitario=produto.preco
    )

    # Associa ao pedido aberto do cliente
    pedido, _ = models.Pedido.objects.get_or_create(
        cliente=request.user.cliente, 
        status='Aberto'
    )
    pedido.itens.add(item)
    
    return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    pedido = models.Pedido.objects.filter(cliente=request.user.cliente, status='Aberto').first()
    return render(request, 'app_loja/ver_carrinho.html', {'pedido': pedido})

@login_required
def finalizar_compra(request):
    pedido = models.Pedido.objects.filter(cliente=request.user.cliente, status='Aberto').first()
    if pedido:
        return redirect('processar_pagamento', pedido_id=pedido.id)
    return redirect('ver_carrinho')