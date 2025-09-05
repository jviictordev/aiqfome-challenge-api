import uuid
from faker import Faker
from app.models.Models import ClientModel, ClientFavoriteModel

fake = Faker()

def test_add_favorite(client):
    # Criar cliente antes
    name = fake.name()
    email = fake.email()
    response = client.post("/client/create", json={"name": name, "email": email})
    client_id = response.json()["id"]

    # Adicionar favorito
    product_id = 1
    response = client.post(f"/client_favorite/create?client_id={client_id}&product_id={product_id}")
    print("client_id", client_id)
    print("product_id", product_id)
    assert response.status_code == 201
    data = response.json()
    assert data["client_id"] == client_id
    assert data["product_id"] == product_id


def test_list_favorites(client):
    # Criar cliente e favoritos
    name = fake.name()
    email = fake.email()
    response = client.post("/client/create", json={"name": name, "email": email})
    client_id = response.json()["id"]

    # Adicionar favoritos
    client.post(f"/client_favorite/create?client_id={client_id}&product_id={1}")
    client.post(f"/client_favorite/create?client_id={client_id}&product_id={2}")

    # Listar favoritos
    response = client.get(f"/client_favorite/list?client_id={client_id}")
    assert response.status_code == 200
    data = response.json()
    product_ids = [f["id"] for f in data.get("client_favorites", data)]
    assert 1 in product_ids
    assert 2 in product_ids


def test_prevent_duplicate_favorite(client):
    # Criar cliente e favorito
    name = fake.name()
    email = fake.email()
    response = client.post("/client/create", json={"name": name, "email": email})
    client_id = response.json()["id"]

    product_id = 1
    client.post(f"/client_favorite/create?client_id={client_id}&product_id={product_id}")

    # Tentar adicionar o mesmo favorito novamente
    response = client.post(f"/client_favorite/create?client_id={client_id}&product_id={product_id}")
    assert response.status_code == 409  # ou 409 conforme implementado


def test_remove_favorite(client):
    # Criar cliente e favorito
    name = fake.name()
    email = fake.email()
    response = client.post("/client/create", json={"name": name, "email": email})
    client_id = response.json()["id"]

    first_product_id = 1
    client.post(f"/client_favorite/create?client_id={client_id}&product_id={first_product_id}")
    second_product_id = 2
    client.post(f"/client_favorite/create?client_id={client_id}&product_id={second_product_id}")

    # Remover favorito
    response = client.delete(f"/client_favorite/delete?client_id={client_id}&product_id={first_product_id}")
    assert response.status_code == 200

    # Verificar que não existe mais
    response = client.get(f"/client_favorite/list?client_id={client_id}")
    data = response.json()
    product_ids = [f["id"] for f in data.get("client_favorites", data)]
    assert first_product_id not in product_ids
    assert second_product_id in product_ids
