# Arquivo que engloba os modelos que serão coordenados na aba admin, por exemplo adicionar produtos ou visualizar os clientes criados

from django.contrib import admin
from .models import Produto

# Register your models here.

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque')
    search_fields = ('nome',)
