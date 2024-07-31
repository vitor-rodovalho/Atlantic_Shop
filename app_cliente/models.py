# Modelos que se relacionam com o cliente, usuário, criação de usuário

from django.db import models
from datetime import date
from django.contrib.auth.models import User

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    username = models.CharField(max_length=1, default='')
    data_criacao = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.nome

class PessoaFisica(Cliente):
    cpf = models.CharField(max_length=14)
    rg = models.CharField(max_length=12)
    data_nascimento = models.DateField()

    def __str__(self):
        return f"{self.nome} ({self.cpf})"

class PessoaJuridica(Cliente):
    cnpj = models.CharField(max_length=18)
    razao_social = models.CharField(max_length=100)
    inscricao_estadual = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.razao_social} ({self.cnpj})"