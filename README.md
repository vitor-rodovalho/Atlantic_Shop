# Projeto de Programação Orientada à Objetos - Integração Cloud & AI com Django 🚀

Este projeto é uma aplicação Django estruturada para integrar serviços de nuvem e modelos de inteligência artificial da Google Cloud, utilizando dados de produtos extraídos originalmente de datasets do Kaggle, mantendo uma arquitetura baseada nos conceitos e estruturas de POO.


---

## ✨ Colaboradores
<a href="https://github.com/acsamendes"><br /><sub><b>Acsa Mendes dos Santos</b></sub>👩🏽‍💻</a>
<a href="https://github.com/vitor-rodovalho"><br /><sub><b>Vitor Hugo da Costa Rodovalho</b></sub>👨‍💻</a>
<a href="https://github.com/sebastiaocfneto"><br /><sub><b>Sebastião Corrrea Fraga Neto</b></sub>👨‍💻</a>


---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** Django
* **Cloud & IA:**  Vertex AI / Gemini
* **Banco de Dados:** SQLite


---

## 🚀 Como Executar o Projeto

Siga os passos abaixo para configurar o ambiente e rodar a aplicação localmente.

### 1. Preparação do Ambiente

Certifique-se de ter o **Python 3.11+** instalado. Prepare o ambiente virtual:

```bash
# Instalar a ferramenta de ambiente virtual
pip install virtualenv

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente
# No Windows:
.\venv\Scripts\activate

# No MacOS/Linux:
source venv/bin/activate

```

### 2. Instalação de Dependências

```bash
pip install -r requirements.txt
```

### 3. Configuração de Variáveis de Ambiente

O projeto utiliza o `django-environ` para gerenciar configurações sensíveis. Crie um arquivo **.env** na raiz do projeto baseando-se no arquivo `.env.example`.

> [IMPORTANTE]
> **Autenticação Google Cloud:**
> Este projeto requer uma Chave de Serviço (JSON) válida. O caminho definido em `GOOGLE_APPLICATION_CREDENTIALS` deve ser absoluto ou relativo à raiz do projeto.


### 4. Inicialização do Banco de Dados (Migrations & Fixtures)

O arquivo de banco de dados binário (`db.sqlite3`) não é versionado. Para reconstruir a estrutura e carregar os dados:

```bash
# 1. Cria a estrutura das tabelas
python manage.py migrate

# 2. Carrega os dados de produtos (Fixture JSON)
python manage.py loaddata produtos.json

```

### 5. Execução

```bash
python manage.py runserver

```

---

## ⚙️ Notas Técnicas e Boas Práticas

* **Persistência de Dados:** Em vez de versionar arquivos binários, o projeto utiliza **Django Fixtures** (`produtos.json`). Isso garante que os dados sejam portáveis entre diferentes sistemas operacionais e bancos de dados.
* **Integração Vertex AI:** A busca semântica utiliza o modelo Gemini da Google Cloud. A configuração é centralizada no `settings.py` e consumida pelas views via `django.conf.settings`.
* **Segurança:** O arquivo `.gitignore` está configurado para proteger arquivos `.env`, bancos de dados `.sqlite3` e credenciais `.json`.
* **Unicode no Windows:** Se encontrar erros de `charmap` ao exportar ou importar dados no Windows, defina a variável de ambiente `PYTHONUTF8=1` no seu terminal antes da execução.