from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Cliente, PessoaFisica, PessoaJuridica

def cadastro(request):
    if request.method == 'POST':
        tipo_cliente = request.POST['tipo_cliente']
        nome = request.POST['nome']
        email = request.POST['email']
        endereco = request.POST['endereco']
        telefone = request.POST['telefone']
        password = request.POST['password']

        # Verificar se o email já está registrado
        if User.objects.filter(email=email).exists():
            return render(request, 'app_cliente/cadastro.html', {
                'error_message': 'Email já cadastrado. Por favor, escolha outro.'
            })

        try:
            # Criação do usuário associado, usando o email como username
            user = User.objects.create_user(username=email, email=email, password=password)
            
            if tipo_cliente == 'fisica':
                cpf = request.POST['cpf']
                rg = request.POST['rg']
                data_nascimento = request.POST['data_nascimento']
                pessoa_fisica = PessoaFisica(
                    nome=nome,
                    email=email,
                    endereco=endereco,
                    telefone=telefone,
                    password=password,
                    user=user,
                    cpf=cpf,
                    rg=rg,
                    data_nascimento=data_nascimento
                )
                pessoa_fisica.save()
            elif tipo_cliente == 'juridica':
                cnpj = request.POST['cnpj']
                razao_social = request.POST['razao_social']
                inscricao_estadual = request.POST['inscricao_estadual']
                pessoa_juridica = PessoaJuridica(
                    nome=nome,
                    email=email,
                    endereco=endereco,
                    telefone=telefone,
                    password=password,
                    user=user,
                    cnpj=cnpj,
                    razao_social=razao_social,
                    inscricao_estadual=inscricao_estadual
                )
                pessoa_juridica.save()

            return redirect('cadastro_concluido')

        except IntegrityError:
            # Redireciona de volta para o formulário de cadastro com uma mensagem de erro
            return render(request, 'app_cliente/cadastro.html', {
               'error_message': 'Erro ao criar o usuário. Tente novamente.'
            })

    return render(request, 'app_cliente/cadastro.html')

@login_required(login_url = 'login')
def visualizar(request):
    try:
        cliente = Cliente.objects.get(user=request.user)
        if hasattr(cliente, 'pessoafisica'):
            cliente = cliente.pessoafisica
        elif hasattr(cliente, 'pessoajuridica'):
            cliente = cliente.pessoajuridica
        else:
            cliente = None
    except Cliente.DoesNotExist:
        return redirect('cadastro_cliente')

    return render(request, 'app_cliente/visualizar.html', {'cliente': cliente})
