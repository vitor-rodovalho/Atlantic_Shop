from django.shortcuts import render, get_object_or_404, redirect
from . import models
from django.contrib.auth.decorators import login_required

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

