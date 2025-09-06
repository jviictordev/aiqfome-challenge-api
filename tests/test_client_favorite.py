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

def test_add_favorite_success(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']

    #deleção do admin criado para o teste
    delete_admin(db_session, admin)

    # Criar favorito
    token = make_token(client_id, role=2)
    response = client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=1",
        headers={"Authorization": f"Bearer {token}"},
    )

    #validações
    assert response.status_code == 201
    data = response.json()
    assert data["client_id"] == client_id
    assert data["product_id"] == 1

def test_list_favorites(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']

    # Deleção do admin criado para o teste
    delete_admin(db_session, admin)
    
    # Atualização do token, para o token do usuário criado
    token = make_token(client_id, role=2)

    # Adição dos favoritos
    client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )
    client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=2",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Listagem dos favoritos do cliente
    response = client.get(f"/client_favorite/list?client_id={client_id}")

    # Validações
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    product_ids = [fav["id"] for fav in data]
    assert 1 in product_ids and 2 in product_ids

def test_delete_favorite_success(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']

    # Atualização do token, para o token do usuário criado
    token = make_token(client_id, 2)

    # Deleção do admin criado para o teste
    delete_admin(db_session, admin)

    # Criação dos favorito
    client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )

    client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=2",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Remoção de um favorito
    response = client.delete(
        f"/client_favorite/delete?client_id={client_id}&product_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Validações
    assert response.status_code == 200
    assert response.json()["message"] == "Produto favorito excluído com sucesso."
    response = client.get(f"/client_favorite/list?client_id={client_id}")
    data = response.json()
    assert all(fav["id"] != 1 for fav in data)


def test_add_favorite_duplicate(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']
    
    # Atualização do token, para o token do usuário criado
    token = make_token(client_id, 2)

    # Deleção do admin criado para o teste
    delete_admin(db_session, admin)

    # Tentativa de criar favoritos duplicados
    client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.post(
        f"/client_favorite/create?client_id={client_id}&product_id=1",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Validação
    assert response.status_code in (400, 409)

def test_delete_favorite_not_exists(client, db_session):
    # Criar admin no banco
    admin = create_admin(db_session)
    token = make_token(admin.id, role=1)

    # Criação cliente novo
    response, name, email = create_client(client, token)
    client_id = response.json()['id']

    # Atualização do token, para o token do usuário criado
    token = make_token(client_id, 2)

    # Deleção do admin criado para o teste
    delete_admin(db_session, admin)

    # Tentativa de remover um favorito inexistente
    response = client.delete(
        f"/client_favorite/delete?client_id={client_id}&product_id=999",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Validação
    assert response.status_code in (400, 404)

def test_list_favorites_invalid_client(client):
    # Criação de um uuid aleatório
    invalid_id = uuid.uuid4()

    # Tentativa de remover um cliente que não existe
    response = client.get(f"/client_favorite/list?client_id={invalid_id}")

    # Validação
    assert response.status_code in (400, 404)
