from http import HTTPStatus


def test_create_client(client):
    response = client.post(
        '/client',
        json={
            'name': 'Alice',
            'email': 'alice@example.com'
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    client_id = response.json().get('id')
    assert response.json() == {
        'name': 'Alice',
        'email': 'alice@example.com',
        'id': client_id,
    }
