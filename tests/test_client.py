import uuid
from sqlalchemy import select
from app.models.Models import ClientModel
from faker import Faker
fake = Faker()


def test_create_client(client):
    name = fake.name()
    email = fake.email()
    response = client.post(
        "/client/create",
        json={"name": name, "email": email}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == name
    assert data["email"] == email
    assert "id" in data


def test_get_clients(client):
    name = fake.name()
    email = fake.email()
    # Criar cliente antes
    response = client.post("/client/create", json={"name": name, "email": email})
    response = client.get("/client/list_all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert any(c["email"] == email for c in data.get('clients'))


def test_update_client(client):
    name = fake.name()
    email = fake.email()
    update_name = fake.name()
    # Criar cliente antes
    response = client.post("/client/create", json={"name": name, "email": email})
    client_id = response.json()["id"]
    # Atualizar
    response = client.patch(f"/client/update?client_id={client_id}", json={"name": update_name})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_name


def test_delete_client(client):
    name = fake.name()
    email = fake.email()
    # Criar cliente antes
    response = client.post("/client/create", json={"name": name, "email": email})
    client_id = response.json()["id"]

    # Remover
    response = client.delete(f"/client/delete?client_id={client_id}")
    assert response.status_code == 200

    # Verificar que sumiu
    response = client.get(f"/client/list?client_id={client_id}")
    assert response.status_code == 404
