from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PagamentoForm
from .models import Pagamento
from app_loja.models import Pedido, Produto

@login_required
def processar_pagamento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user.cliente)  # Inclui o cliente no filtro
    
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            metodo_pagamento = form.cleaned_data['metodo_pagamento']
            valor = pedido.calcular_total()  

            # Cria uma instância de Pagamento para cada item no pedido
            for item in pedido.itens.all():
                pagamento = Pagamento(
                    user=request.user,
                    produto=item.produto,
                    valor=item.calcular_subtotal(),
                    metodo_pagamento=metodo_pagamento
                )
                pagamento.save()
            
            pedido.status = 'Pago'
            pedido.save()
            
            messages.success(request, 'Pagamento realizado com sucesso!')
            return redirect('pagamento_concluido')  
    else:
        form = PagamentoForm()
    
    return render(request, 'app_pagamento/processar_pagamento.html', {'form': form, 'pedido': pedido})
