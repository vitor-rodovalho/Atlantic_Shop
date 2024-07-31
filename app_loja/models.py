# Classes e métodos __str__, cálculo de valor total, 

from django.db import models
from datetime import date
from app_cliente.models import Cliente


class Produto(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField()

    def __str__(self):
        return self.nome

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"Item de {self.produto.nome}"

class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    data_pedido = models.DateField(default=date.today)
    status = models.CharField(max_length=20)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    itens = models.ManyToManyField(Item)

    def calcular_total(self):
        return sum(item.calcular_subtotal() for item in self.itens.all())

    def __str__(self):
        return f"Pedido {self.id} de {self.cliente.nome}"
