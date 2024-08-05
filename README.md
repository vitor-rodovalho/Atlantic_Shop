✨ Colaboradores
<a href="https://github.com/acsamendes"><br /><sub><b>Acsa Mendes dos Santos</b></sub>👩🏽‍💻</a>
<a href="https://github.com/vitor-rodovalho"><br /><sub><b>Vitor Hugo da Costa Rodovalho</b></sub>👨‍💻</a>
<a href="https://github.com/sebastiaocfneto"><br /><sub><b>Sebastião Corrrea Fraga Neto</b></sub>👨‍💻</a>

🚀 Uso
Instruções para usar o projeto após a instalação:

```
# 1. Instalar Python
# Certifique-se de que você tem o Python instalado em sua máquina.

# 2. Instalar Virtualenv
pip install virtualenv

# 3. Criar um Ambiente Virtual
cd /caminho/para/seu/projeto
python -m venv venv

# 4. Ativar o Ambiente Virtual
# No Windows:
.\venv\Scripts\activate

# No MacOS/Linux:
source venv/bin/activate

# 5. Instalar Dependências
# Instale as dependências listadas no arquivo requirements.txt
pip install -r requirements.txt

# 6. Configurar Variáveis de Ambiente e Modificar Constantes
# Crie um arquivo .env na raiz do seu projeto
# Adicione suas variáveis de ambiente no arquivo .env, por exemplo:
# SECRET_KEY=sua-chave-secreta

# Instale o django-environ
pip install django-environ

# Configure seu settings.py para usar django-environ
# No seu settings.py adicione:
# import environ
# env = environ.Env(DEBUG=(bool, False))
# environ.Env.read_env()
# SECRET_KEY = env('SECRET_KEY')
# DEBUG = env('DEBUG')
# DATABASES = {'default': env.db()}

# Em app_loja, views.py, mudar a constante "CAMINHO_DB", "PROJECT_ID", "LOCAL" e "MODEL_ID" conforme sua necessidade

# Criar Chave de Serviço do Google Cloud Console e baixar o arquivo JSON
# Defina a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS que aponta para o caminho do arquivo JSON.

# Em sistemas Unix/Linux/MacOS:
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/seu/arquivo.json"

# Em Windows:
set GOOGLE_APPLICATION_CREDENTIALS=C:\caminho\para\seu\arquivo.json

# 7. Migrar o Banco de Dados
python manage.py makemigrations
python manage.py migrate

# 8. Rodar o Servidor de Desenvolvimento
python manage.py runserver

# 9. Desativar o Ambiente Virtual
deactivate

# 10. Versionamento com Git
# Adicione o ambiente virtual ao seu arquivo .gitignore
echo "venv/" >> .gitignore
```
