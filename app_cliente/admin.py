from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'user', 'email', 'data_criacao')
    search_fields = ('id', 'nome', 'user', 'email')