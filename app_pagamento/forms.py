from django import forms

class PagamentoForm(forms.Form):
    metodo_pagamento = forms.ChoiceField(choices=[
        ('credito', 'Cartão de Crédito'),
        ('debito', 'Cartão de Débito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'Pix')])
