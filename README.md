🛠️ AIQFome Challenge API

API desenvolvida em FastAPI com SQLAlchemy e Alembic, contendo rotas de clientes, favoritos e integração com a FakeStoreAPI
.
O projeto também inclui autenticação e autorização via JWT, testes automatizados com pytest e suporte a deploy no Railway.

📌 Tecnologias Utilizadas

Python 3.11+
FastAPI
SQLAlchemy
Alembic
PostgreSQL
Passlib
 – para hashing de senhas
Pytest
 – para testes automatizados
Uvicorn
 – servidor ASGI

⚙️ Configuração do Ambiente

1️⃣ Clonar o repositório
git clone https://github.com/seu-usuario/aiqfome-challenge-api.git

-> cd aiqfome-challenge-api

2️⃣ Criar e ativar um ambiente virtual

-> python -m venv venv

-> source venv/bin/activate           # Linux/Mac

-> source venv/Scripts/activate       # Windows

3️⃣ Instalar dependências

pip install -r requirements.txt

4️⃣ Configurar .env

*Para essa etapa, é necessário que tenha o postgresql instalado e configurado na sua máquina.

Crie um arquivo .env na raiz do projeto:

DATABASE_URL=postgresql+psycopg2://postgres_user:sua_senha@localhost:5432/nome_do_banco_principal

DATABASE_URL_TEST=postgresql+psycopg2://postgres_user:sua_senha@localhost:5432/nome_do_banco_teste

SECRET_KEY=uma_chave_super_secreta

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

PRODUCT_API_URL=https://fakestoreapi.com

🗄️ Banco de Dados e Migrations
Criar estrutura inicial

-> alembic upgrade head

Criar uma nova migration

-> alembic revision --autogenerate -m "mensagem_da_migration"

Rodar migrations pendentes

-> alembic upgrade head


▶️ Executando o Projeto
Rodar localmente

-> uvicorn app.main:app --reload


A API estará disponível em:

👉 http://localhost:8000

Documentação automática

Swagger UI: http://localhost:8000/docs

Redoc: http://localhost:8000/redoc

✅ Rodando os Testes

Para rodar todos os testes automatizados:

-> pytest -v

🚀 Deploy no Railway
O deploy desse projeto foi feito pelo Railway, e está disponível para acessar publicamente.

https://aiqfome-challenge-api-production.up.railway.app/docs

Qualquer problema de acesso, pode entrar em contato

via e-mail: contateojoaovictor@gmail.com

via whatsapp: (42)998445953

Por se tratar de uma hospedagem gratuita, o servidor pode sofrer com desligamentos inesperados.

📚 Estrutura de Pastas

app/

├── config/              # Configurações (DB, Auth, etc.)

├── controllers/         # Definição das rotas FastAPI

├── models/              # Modelos do SQLAlchemy

├── repositories/        # Repositórios (acesso a dados)

├── schemas/             # Schemas Pydantic

├── services/            # Regras de negócio

├── main.py              # Ponto de entrada da aplicação

migrations/              # Todas as migrations geradas via alembic

tests/                   # Testes desenvolvidos com pytest


🔐 Autenticação & Autorização

JWT Tokens são utilizados para autenticação.

Endpoints públicos podem ser acessados sem token.

Endpoints protegidos exigem um token válido no header Authorization:

Authorization: Bearer <seu_token>


Existem papéis (roles) diferentes:

admin → essa role é definida no banco de dados pelo número 1.

user → essa role é definida no banco de dados pelo número 2.

👨‍💻 Autor

Desenvolvido por João Victor no Desafio AIQFome - Dev Backend.
