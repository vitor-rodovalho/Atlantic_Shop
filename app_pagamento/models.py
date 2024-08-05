from django.db import models
from django.contrib.auth.models import User
from app_loja.models import Produto

class Pagamento(models.Model):
    METODOS_PAGAMENTO = [
        ('credito', 'Cartão de Crédito'),
        ('debito', 'Cartão de Débito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'Pix'),  
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    metodo_pagamento = models.CharField(max_length=50, choices=METODOS_PAGAMENTO)

    def __str__(self):
        return f'Pagamento de {self.user.username} - {self.produto.nome}'
