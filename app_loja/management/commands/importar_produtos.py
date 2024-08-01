# app_loja/management/commands/importar_produtos.py

import csv
from django.core.management.base import BaseCommand
from app_loja.models import Produto

class Command(BaseCommand):
    help = 'Importa produtos de um arquivo CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='O caminho para o arquivo CSV')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        with open(csv_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file, fieldnames=['title', 'imgUrl', 'price', 'categoryName'])
            next(reader)  # Pular o cabeçalho
            for row in reader:
                produto, created = Produto.objects.get_or_create(
                    nome=row['title'],
                    imgUrl=row['imgUrl'],
                    preco=row['price'],
                    categoria=row['categoryName']
                )
                