# Tutorial de Configuração Inicial

Este guia irá ajudá-lo a configurar o projeto para desenvolvimento local, utilizando Poetry para gerenciamento de dependências, Ruff para linting e pytest como ferramentas de teste.

## Pré-requisitos

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation)
- Git

## 1. Clonando o repositório

```bash
git clone https://github.com/seu-usuario/aiqfome-challenge-api.git
cd aiqfome-challenge-api
```

## 2. Instalando dependências

```bash
poetry install
```

## 3. Ativando o ambiente virtual

```bash
poetry shell
```

## 4. Configurando Ruff (Linting)

Ruff já está configurado no projeto via arquivo `pyproject.toml`. Para rodar o lint:

```bash
poetry run ruff check .
```

Para corrigir automaticamente problemas simples:

```bash
poetry run ruff check . --fix
```

## 5. Executando os testes

Os testes estão configurados (ex: pytest). Para rodar todos os testes:

```bash
poetry run pytest
```

## 6. Outras dicas

- Para adicionar novas dependências:  
    `poetry add nome-do-pacote`
- Para adicionar dependências de desenvolvimento:  
    `poetry add --dev nome-do-pacote`

---