import uuid
from faker import Faker
from app.models.Models import ClientModel
from app.config.Auth import create_access_token, hash_password

fake = Faker()
#função para criar um token para o cliente
def make_token(client_id: uuid.UUID, role: int):
    return create_access_token({"sub": str(client_id), "role": role})

#função para criar um cliente admin
def create_admin(db_session):
    admin = ClientModel(
        id=uuid.uuid4(),
        name="Admin",
        email="admin@example.com",
        password=hash_password("admin123"),
        role=1
    )
    db_session.add(admin)
    db_session.commit()
    return admin

#função para apagar o cliente admin criado para o teste
def delete_admin(db_session, admin):
    db_session.delete(admin)
    db_session.commit()

#função para criar um cliente
def create_client(client, token):
    name = fake.name()
    email = fake.email()
    response = client.post(
        "/client/create",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name, "email": email, "password": "12345", "role": 2}
    )
    print(response)
    assert response.status_code == 201
    return response, name, email

def test_create_client_as_admin(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)

    # Deleção do admin criado para o teste
    delete_admin(db_session, admin)

    # Validações
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name
    assert data["email"] == email
    assert "id" in data

def test_get_clients_open(client):
    # Listagem de clientes
    response = client.get("/client/list_all")

    #validações
    assert response.status_code == 200

def test_update_client_as_logged_user(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']
    token = make_token(client_id, role=2)

    #deleção do admin criado para o teste
    delete_admin(db_session, admin)

    #atualização do cliente criado
    update_name = fake.name()
    response = client.patch(
        f"/client/update?client_id={client_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": update_name},
    )

    #validações
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_name

def test_delete_client_as_admin(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']

    # Deletar cliente
    response = client.delete(
        f"/client/delete?client_id={client_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    #deleção do admin criado para o teste
    delete_admin(db_session, admin)

    #validações
    assert response.status_code == 200
    response = client.get(f"/client/list?client_id={client_id}")
    assert response.status_code == 204


def test_create_client_without_admin(client):
    # Tentativa criação de um cliente, sem passar o token
    response = client.post(
        "/client/create",
        json={"name": "Fake", "email": "fake@example.com", "password": "123456", "role": 2},
    )
    assert response.status_code == 401

def test_create_client_as_user_forbidden(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']
    token = make_token(client_id, role=2)

    # Tentativa criação de um cliente, por um usuário não admin
    response = client.post(
        "/client/create",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Outro", "email": "outro@example.com", "password": "123456", "role": "user"},
    )
    
    #deleção do admin criado para o teste
    delete_admin(db_session, admin)

    #validação
    assert response.status_code == 403

def test_update_client_without_login(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']

    # Tentativa de atualizar um cliente, sem estar logado
    response = client.patch(
        f"/client/update?client_id={client_id}",
        json={"name": "Novo Nome"},
    )

    #deleção do admin criado para o teste
    delete_admin(db_session, admin)

    #validação
    assert response.status_code == 401

def test_duplicate_email_should_fail(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)

    # Tentativa de criação de outro cliente com o mesmo e-mail
    response = client.post(
        "/client/create",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": f"Segundo {name}", "email": email, "password": "123456", "role": 2},
    )
    
    #deleção do admin criado para o teste
    delete_admin(db_session, admin)

    #validação
    assert response.status_code == 400 or response.status_code == 409
